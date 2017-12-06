# brainfuck-import
Allows importing brainfuck files as python modules. Imported modules expose two similar public functions, each optionally accepting
a string or iterable of ints as input: `get_ints` which yields "printed" integers, and `get_string` which interprets the integer stream
as characters of a string.

```brainfuck
doubler dot bf
,[..,]
```

```python
import bf_import.magic

import doubler

print(doubler.get_string('abc'))  # outputs "aabbcc"
```


Inspired by kragniz's [json-sempai](https://github.com/kragniz/json-sempai).
