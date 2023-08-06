# Usage
```python
import os
from enterdir import EnterDir

def print_cwd():
    print(os.getcwd())

print_cwd()
with EnterDir('path/to/dir') as d:
    print_cwd()
print_cwd()
```