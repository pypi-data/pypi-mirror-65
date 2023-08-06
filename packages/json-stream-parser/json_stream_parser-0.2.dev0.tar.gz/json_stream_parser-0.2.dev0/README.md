Parsing a stream of json objects without loading the whole stream into memory.
Solution to https://stackoverflow.com/questions/6886283/how-i-can-i-lazily-read-multiple-json-values-from-a-file-stream-in-python

```python
import sys
from json_stream_parser import load_iter
for obj in load_iter(sys.stdin):
    print(obj)
```
