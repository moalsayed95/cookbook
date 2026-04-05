# Regular Expressions (Regex)

## Resources

### YouTube Videos
- [Regular Expressions (RegEx) in 100 Seconds — Fireship](https://www.youtube.com/watch?v=sXQxhojSdZM)
- [How Regex Works — ArjanCodes](https://www.youtube.com/watch?v=piKVBupALek)
- [[5 Minute Tutorial] Regular Expressions (Regex) in Python — Kite](https://www.youtube.com/watch?v=UQQsYXa1EHs)

### Cheatsheets
- [Python Regular Expression (Regex) Cheatsheet — Cheatography](https://cheatography.com/mutanclan/cheat-sheets/python-regular-expression-regex/)

### Docs
- [re — Regular Expression Operations — Python Docs](https://docs.python.org/3/library/re.html)
- [Regular Expressions — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)

---

## What is Regex?

A Regular Expression (regex) is a sequence of characters that defines a search pattern. It's used to match, find, or replace text inside strings.

It looks like this:

```
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

That pattern matches an email address. Ugly? Yes. Powerful? Absolutely.

## Why Regex?

Any time you need to work with text — validating input, extracting data, searching logs, cleaning datasets — regex is the tool that gets it done in one line instead of twenty.

Common use cases:
- **Validation** — check if a string matches a format (emails, phone numbers, passwords)
- **Search & Replace** — find patterns in text and transform them
- **Data Extraction** — pull specific pieces out of unstructured text (scraping, log parsing)
- **Text Cleaning** — remove unwanted characters, normalize whitespace, strip HTML tags

## Quick Example

Check if a string is a valid email:

```python
import re

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email = "test@example.com"

if re.match(pattern, email):
    print("Valid email")
else:
    print("Invalid email")
```

Extract all hashtags from a tweet:

```python
import re

tweet = "Learning #regex is fun! #python #coding"
hashtags = re.findall(r'#\w+', tweet)
print(hashtags)  # ['#regex', '#python', '#coding']
```

## Core Syntax

| Symbol | Meaning | Example |
|--------|---------|---------|
| `.` | Any character (except newline) | `a.c` → "abc", "a1c" |
| `*` | 0 or more of the previous | `ab*c` → "ac", "abc", "abbc" |
| `+` | 1 or more of the previous | `ab+c` → "abc", "abbc" (not "ac") |
| `?` | 0 or 1 of the previous | `colou?r` → "color", "colour" |
| `^` | Start of string | `^Hello` → matches "Hello world" |
| `$` | End of string | `world$` → matches "Hello world" |
| `\d` | Any digit (0–9) | `\d{3}` → "123", "456" |
| `\w` | Any word character (letter, digit, underscore) | `\w+` → "hello_42" |
| `\s` | Any whitespace | `\s+` → spaces, tabs, newlines |
| `[abc]` | Any one of a, b, or c | `[aeiou]` → matches a vowel |
| `[^abc]` | Any character except a, b, or c | `[^0-9]` → matches non-digits |
| `(...)` | Capture group | `(\d{3})-(\d{4})` → captures parts of "123-4567" |
| `{n,m}` | Between n and m repetitions | `\d{2,4}` → "12", "123", "1234" |
| `\|` | OR | `cat\|dog` → "cat" or "dog" |

## Python's `re` Module

The most commonly used functions:

```python
import re

# re.match()  — match at the BEGINNING of the string
re.match(r'\d+', '123abc')  # Match: '123'

# re.search() — find the FIRST match anywhere in the string
re.search(r'\d+', 'abc123def')  # Match: '123'

# re.findall() — find ALL matches, return as list
re.findall(r'\d+', 'a1b2c3')  # ['1', '2', '3']

# re.sub() — search and replace
re.sub(r'\s+', '-', 'hello   world')  # 'hello-world'

# re.split() — split string by pattern
re.split(r'[,;]\s*', 'one, two; three')  # ['one', 'two', 'three']
```

## When NOT to Use Regex

Regex is powerful, but it's not always the right tool:

- **Parsing HTML/XML** — use a proper parser like BeautifulSoup or lxml instead. Regex can't handle nested structures reliably.
- **Complex validation** — if the pattern gets unreadable, break it into smaller checks or use a validation library.
- **Performance-critical paths** — poorly written regex can cause catastrophic backtracking, where the engine gets stuck trying exponentially many possibilities. This can freeze your program or even crash it.

> ArjanCodes has a great video on [when to be careful with regex](https://www.youtube.com/watch?v=piKVBupALek) — worth watching before you use regex in production.

## Real-World Use Cases

1. **Log Parsing** — extract timestamps, error codes, and IPs from server logs
2. **Form Validation** — check emails, phone numbers, zip codes on the frontend or backend
3. **Web Scraping** — pull data out of raw HTML when a full parser is overkill
4. **Data Cleaning** — normalize messy CSV data, strip special characters, fix formatting
5. **Search Tools** — grep, ripgrep, IDE find-and-replace all use regex under the hood
6. **URL Routing** — frameworks like Django use regex to match URL patterns to views
