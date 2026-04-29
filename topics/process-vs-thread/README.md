# Process vs Thread

## The Interview Question

> "Explain the difference between a process and a thread."

It's one of the most common interview questions, and it sounds basic — until you have to actually say it out loud. The cleanest way to answer is with an analogy.

## The Escape Room Analogy

Think of an **escape room**.

- A **process** is the physical escape room you just rented. It has its own locked doors, its own puzzles, its own timer, and its own four walls.
- A **thread** is a player inside that room. You and your friends are the threads.

One room can have multiple players. A single process can have multiple threads working through puzzles at the same time.

Why does this matter? Because you and your friends inside the same room **share everything** — the same clues, the same table, the same physical space. If you find a key, you just hand it to your friend. Communication is instant.

But there's a catch: if one of your friends loses it and smashes a puzzle box, the staff kicks **everyone** out. The game is over for the whole room.

That's the entire mental model. Now let's translate it.

## What's Actually Happening

### Program vs Process

A **program** is just a file on disk — an executable. It's a set of instructions sitting there doing nothing.

When that program is loaded into memory and the CPU starts running it, it becomes a **process**. A process isn't just code — it's the code *plus* everything the OS gives it to run: its own memory address space, its heap, its stack, file handles, and so on.

The most important property:

> **Each process has its own memory address space. One process cannot corrupt the memory of another process.**

This is why Chrome runs each tab as its own process. If one tab crashes from a bug or a malicious site, the others keep running. That's process isolation in action.

### What a Thread Actually Is

A **thread** is the unit of execution *inside* a process. Every process has at least one thread — the **main thread** — and most non-trivial programs have many.

Each thread has:

- Its own **stack**
- Its own **registers** and **program counter**

But all threads inside the same process **share the same memory address space** — the heap, the global variables, open files, everything.

That's why threads can talk to each other just by reading and writing shared variables. No network call, no IPC, no serialization. It's the "hand your friend the key" moment from the analogy.

The downside is the same as the analogy too: if one thread hits a fatal error and the process dies, **every other thread in that process dies with it**.

## Quick Comparison

| | Process | Thread |
|---|---|---|
| **Memory** | Own isolated address space | Shares memory with other threads in the same process |
| **Communication** | Needs IPC (pipes, sockets, shared memory) | Just read/write shared variables |
| **Isolation** | Crash in one ≠ crash in others | One bad thread can kill the whole process |
| **Creation cost** | Heavy | Light |
| **Context switch cost** | Expensive | Cheaper |

## Context Switching (the Bonus Round)

Only one thing actually runs on a CPU core at a time. The OS fakes concurrency by rapidly swapping work in and out — that swap is called a **context switch**.

During a context switch the OS has to:

1. Save the current thread's registers, program counter, and stack pointer
2. Update kernel bookkeeping
3. Possibly swap out memory pages
4. Restore all of that for the next thread

Switching between **threads** of the same process is **cheaper** than switching between **processes**, because threads share the same memory map — the OS doesn't have to swap out virtual memory pages, which is one of the most expensive parts of a context switch.

Context switching is so expensive that languages and runtimes invented even lighter-weight alternatives — **fibers** and **coroutines** — that are scheduled by the application itself instead of the OS. They cost almost nothing to switch between, but the program has to **cooperatively yield** to give others a turn. Go's goroutines, Python's `async`/`await`, and Kotlin coroutines all live in this world.

## The One-Sentence Answer

> A **process** is an isolated program running in memory with its own address space. A **thread** is an execution unit inside a process — multiple threads share the same memory, which makes communication fast but means one bad thread can take the whole process down.

## TL;DR

- **Program** = file on disk. **Process** = program running in memory. **Thread** = a worker inside a process.
- Processes are **isolated** — safer, but communication is expensive.
- Threads **share memory** — fast communication, but one crash takes them all down.
- Switching threads is cheaper than switching processes because the memory map stays the same.
- When even thread switching is too slow, reach for **coroutines** or **fibers**.
