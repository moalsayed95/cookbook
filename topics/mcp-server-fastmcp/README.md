# Build Your First MCP Server with FastMCP

An LLM can explain how to query a database, but it cannot touch your database by itself.
It can describe how to send an email, but it cannot press Send by itself.

It needs a safe, structured way to discover and call real software.
That is the problem the **Model Context Protocol (MCP)** solves.

In this guide, you will turn one ordinary Python function into an MCP tool, inspect it in a browser, and connect it to an AI application.

## MCP in One Minute

Think of MCP as **USB-C for AI applications**.

USB-C gives devices one standard way to connect.
MCP gives AI applications one standard way to connect to external tools and data.

Instead of writing a custom integration for every AI app, an MCP server can expose capabilities using the same protocol.
Compatible apps can then discover those capabilities and use them.

MCP servers can expose three main building blocks:

| Building block | What it provides | Example |
|---|---|---|
| **Tools** | Actions the AI can request | Send an email, query an API, create a ticket |
| **Resources** | Data the AI can read as context | A file, database record, or API response |
| **Prompts** | Reusable interaction templates | A code-review or incident-response workflow |

This tutorial focuses on **tools**.

## Where FastMCP Fits

MCP is the protocol.
**FastMCP** is a Python framework that handles much of that protocol for you.

You write a normal Python function.
FastMCP turns its name, docstring, parameters, and type hints into a tool definition that an MCP client can understand.
It also validates arguments, runs the function, and sends the result back in MCP format.

Here is the full mental model:

| Part | Job | Example |
|---|---|---|
| **MCP host** | The AI application the user interacts with | Claude Desktop, VS Code, ChatGPT |
| **MCP client** | Maintains the protocol connection for the host | Created and managed inside the AI app |
| **MCP server** | Exposes tools, resources, and prompts | The Python server in this guide |
| **FastMCP** | Helps you build the server in Python | `FastMCP`, `@mcp.tool`, validation, transports |

The LLM does not import your Python function directly.
The host connects to the MCP server, discovers the tool schema, gives that schema to the model, and routes approved tool calls back to the server.

## What We Are Building

The finished flow looks like this:

```text
You: "Greet Ada"
        |
        v
AI application discovers a tool named "greet"
        |
        v
LLM chooses greet(name="Ada")
        |
        v
MCP client calls your FastMCP server
        |
        v
Python returns "Hello, Ada!"
        |
        v
AI application shows the result
```

## 1. Create the Project

This guide uses [uv](https://docs.astral.sh/uv/) to create the project and manage Python dependencies.

```bash
uv init hello-mcp
cd hello-mcp
uv add fastmcp
```

You can verify the installation with:

```bash
uv run fastmcp version
```

## 2. Create the Server

Create a file named `server.py`:

```python
from fastmcp import FastMCP

mcp = FastMCP("Greeting Server")


@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
```

That small file has four important pieces:

1. `FastMCP("Greeting Server")` creates the MCP server.
2. `@mcp.tool` registers the next Python function as an MCP tool.
3. `name: str` describes and validates the tool input.
4. The docstring tells the AI what the tool does.

The return annotation matters too.
FastMCP can use `-> str` to describe and validate the tool's structured output.

## What FastMCP Generates

FastMCP turns the function into a tool definition similar to this simplified schema:

```json
{
  "name": "greet",
  "description": "Greet a person by name.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string"
      }
    },
    "required": ["name"]
  }
}
```

The schema is the contract between the AI application and your code.

- The **function name** becomes the tool name.
- The **docstring** explains when the tool is useful.
- The **type hints** become JSON Schema and drive input validation.
- The **return type** can become an output schema.

Clear names and docstrings are not decoration.
They help the model choose the right tool and provide the right arguments.

## 3. Test It with MCP Inspector

Run the server in the official browser-based MCP Inspector:

```bash
uv run fastmcp dev inspector server.py
```

The Inspector starts the server over the local `stdio` transport and opens a testing interface.
If it does not connect automatically, select **STDIO** and click **Connect**.

Then:

1. Open **Tools**.
2. Click **List Tools**.
3. Select `greet`.
4. Enter a name.
5. Click **Run Tool**.

You should receive:

```text
Hello, Ada!
```

You can also inspect and call the tool directly from the terminal:

```bash
uv run fastmcp inspect server.py
uv run fastmcp call server.py greet name=Ada
```

## 4. Run the Server

Run it with FastMCP's CLI:

```bash
uv run fastmcp run server.py
```

The default transport is `stdio`.
Local MCP hosts commonly launch a `stdio` server as a child process and communicate through its standard input and output streams.

You can also run the file directly because it contains the `__main__` block:

```bash
uv run server.py
```

The process may look like it is waiting silently.
That is normal because it is waiting for an MCP client, not for keyboard input.

For a remote server, FastMCP can use Streamable HTTP instead:

```bash
uv run fastmcp run server.py --transport http --port 8000
```

The local endpoint is then:

```text
http://127.0.0.1:8000/mcp
```

Use authentication and HTTPS before exposing an HTTP MCP server outside your machine.

## 5. Connect an AI Application

For example, FastMCP can register this local server with Claude Desktop:

```bash
uv run fastmcp install claude-desktop server.py
```

Fully quit and reopen Claude Desktop after changing its MCP configuration.
Then try asking:

```text
Please greet Mo.
```

The application can show the `greet` tool call and ask for approval, depending on the client's settings.
After approval, the MCP server runs the Python function and returns the result.

FastMCP also supports install targets for clients such as Claude Code, Cursor, Gemini CLI, and Goose.
Client support and approval behavior vary, so check the documentation for the AI application you use.

## What Happens Under the Hood

When you send the prompt, the flow is roughly:

1. The MCP host creates a client connection to your server.
2. The client discovers the server's capabilities and available tools.
3. Your server returns the `greet` tool definition and its schema.
4. The host makes that tool definition available to the LLM.
5. The LLM may decide that `greet` is useful and proposes `{"name": "Mo"}`.
6. The host routes the call through the MCP client, applying its approval policy.
7. FastMCP validates the arguments and calls `greet(name="Mo")`.
8. The result travels back to the host and becomes part of the model's response.

The important word is **may**.
MCP makes tools discoverable and callable, but it does not guarantee that a model will choose the correct tool.
Good descriptions, focused tool design, client policy, and testing still matter.

## A Tool Is Still an API

The friendly decorator does not remove normal backend responsibilities.
Treat every tool like an API endpoint:

- Validate values, not only types.
- Enforce authentication and authorization in server code.
- Give the process the minimum permissions it needs.
- Require confirmation for destructive or expensive actions.
- Keep secrets in environment variables or a secret manager.
- Add timeouts and careful error handling around network calls.
- Do not expose internal exception details to untrusted clients.
- Treat tool results and external content as untrusted input.

MCP annotations such as `readOnlyHint` and `destructiveHint` can help clients present safer controls, but they are advisory metadata.
They are not a security boundary.

## One Important `stdio` Rule

Do not use `print()` for logging in a `stdio` MCP server.

MCP protocol messages travel over standard output.
Extra text written there can corrupt the message stream and break the connection.

Use Python's `logging` module, which writes to standard error by default:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Greeting a user")
```

This restriction does not apply in the same way to an HTTP transport because protocol messages travel in HTTP responses.

## Common Mistakes

### Using the Wrong Import

For the standalone FastMCP package used in this guide, the import is lowercase:

```python
from fastmcp import FastMCP
```

You may find older MCP Python SDK tutorials with a different import path.
Do not combine code from different FastMCP or MCP SDK generations without checking their versioned documentation.

### Expecting the Server to Be a Chatbot

The MCP server does not contain the LLM or the chat interface.
It exposes capabilities to an MCP host that contains or connects to the model.

### Writing Vague Tool Descriptions

`"Does stuff"` gives the model almost no useful routing information.
Explain what the tool does, when to use it, and what each argument means.

### Giving One Tool Too Many Jobs

A tool named `manage_everything` is difficult to describe, authorize, test, and use reliably.
Prefer small tools with clear boundaries, such as `get_order`, `cancel_order`, and `create_refund`.

### Trusting Model-Generated Arguments

Type validation catches malformed inputs.
It does not decide whether a user is allowed to delete an account or transfer money.
Authorization and business rules still belong in your code.

## Local vs Remote MCP Servers

| Local server | Remote server |
|---|---|
| Usually uses `stdio` | Usually uses Streamable HTTP |
| Runs on the same machine as the host | Runs behind a network endpoint |
| Host commonly starts the process | Server runs independently |
| Useful for files and local developer tools | Useful for shared APIs and services |
| Inherits local process permissions | Needs network authentication and authorization |

Start with `stdio` while learning.
Move to HTTP when multiple users or machines need to reach the server.

## Try These Next

Once `greet` works, replace it with a tool that does something useful:

- Look up an order by ID.
- Search your documentation.
- Create an issue in a project tracker.
- Query a read-only analytics database.
- Check the health of a deployed API.

Keep the first version read-only when possible.
It is easier to test the protocol when a mistaken call cannot change real data.

## TL;DR

- **MCP** is an open standard for connecting AI applications to external systems.
- An MCP server can expose **tools**, **resources**, and **prompts**.
- **FastMCP** turns typed Python functions into MCP capabilities.
- `@mcp.tool` registers a function as a tool.
- Function names, docstrings, and type hints become the schema the AI application sees.
- `uv run fastmcp dev inspector server.py` lets you test the server visually.
- The AI application discovers and routes tools; the LLM does not connect directly to your Python process.
- MCP standardizes the connection, but your code must still enforce security and business rules.

## Version Note

This guide was checked against the official MCP and FastMCP documentation in August 2026.
FastMCP's documentation can include prerelease features from its main branch, so this tutorial intentionally uses stable core APIs.
For production deployments, commit your lockfile and pin exact dependency versions.

## Resources

### MCP

- [What is the Model Context Protocol?](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
- [Build an MCP Server](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

### FastMCP

- [FastMCP Documentation](https://gofastmcp.com/getting-started/welcome)
- [FastMCP Installation](https://gofastmcp.com/getting-started/installation)
- [FastMCP Quickstart](https://gofastmcp.com/getting-started/quickstart)
- [FastMCP Tools](https://gofastmcp.com/servers/tools)
- [FastMCP CLI and Inspector](https://gofastmcp.com/cli/running)
- [Install Servers into MCP Clients](https://gofastmcp.com/cli/install-mcp)