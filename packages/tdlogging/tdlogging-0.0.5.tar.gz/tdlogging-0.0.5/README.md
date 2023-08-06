Class Based Logger for Python

# Installation

```bash
pip install tdlogging
```

# Doc

## Configuration File
#### tdlogger.txt
A config text file for TDLogger
- `exception` log exceptions
- `count` log count
- `time` log time elapsed
- `return` log return value
- `exec` log all
- `poll` whether to poll for tdlogger.txt changes
- `poll_period` seconds between each poll

## TDLogger.py

#### TDLogger
**Python Class**   

**`__init__`** 
 
Constructor
- `file_path` path of tdlogger.txt
- `config` custom config in python dict that overrides tdlogger.txt
- `alias` a name for your logger    


**`.config()`**  

Get the Logger decorator from its Configuration


#### ApplyDecorators

**Python Function**

Parameters
- `target_dir` Directory that is affected
- `import_root` Python import name of your tdlogger instance
- `var_name` Variable name of the TDLogger instance in your file
- `force` Whether to ignore applying at the current file level
- `verbose` Whether to log changes

DANGEROUS, use with caution  
Apply decorators to every python file in the Directory, and also marking the file

#### RemoveDecorators

**Python Function**

Parameters
- `target_dir` Directory that is affected
- `import_root` Python import name of your tdlogger instance
- `var_name` Variable name of the TDLogger instance in your file
- `force` Apply Changes without confirmation
- `verbose` Whether to log changes

DANGEROUS, use with caution  
Remove decorators to every python file in the Directory, and also removing the mark headings

# Usage

## Example  

📦example  
 ┣ 📂cool  
 ┃ ┣ 📂cooler  
 ┃ ┃ ┣ 📜sleep.py  
 ┃ ┃ ┗ 📜__init__.py  
 ┃ ┣ 📜fib.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📜logger_instance.py  
 ┣ 📜playground.py  
 ┣ 📜tdlogger.txt  
 ┗ 📜__init__.py  


```text
# example/tdlogger.txt

exception = False
count = False
exec = True
time = False
return = False
poll = False
poll_period = 5
```

```python
# example/cool/fib.py

class Fib:

    @staticmethod
    def get_n(n):
        a = 0
        b = 1

        if n == 0:
            return a
        elif n == 1:
            return b
        else:
            for i in range(2, n):
                c = a + b
                a = b
                b = c
            return b
```

```python
# example/cool/cooler/sleep.py

import time

class Sleep:
    @staticmethod
    def sleep(n):
        time.sleep(n)
```

```python
# example/logger_instance.py

from tdlogging.tdlogger import TDLogger

logger = TDLogger(alias="My Custom Logger").config()
```

```python
# example/playground.py

from tdlogging.tdlogger import ApplyDecorators, RemoveDecorators

ApplyDecorators(target_dir="cool", import_root="example.logger_instance", var_name="logger", force=True)

for i in range(12):
    from example.cool.cooler.sleep import Sleep
    from example.cool.fib import Fib

    print(Fib.get_n(i))
    Sleep.sleep(1)

RemoveDecorators(target_dir="cool", import_root="example.logger_instance", var_name="logger", force=True)
```

```bash
> python example/playground.py

Added 6 lines to 2 file(s) .
┎────────────────────────────┒
┃    --Method Execution--    ┃
┃ Alias: My Custom Logger    ┃
┃ Class: Fib                 ┃
┃ Method: get_n              ┃
┃ Count: 1                   ┃
┃ Exec Time: 0.000s          ┃
┃ Return Value: 0            ┃
┃ Return Type: <class 'int'> ┃
┃ Arguments: {               ┃
┃     'n': 0                 ┃
┃ }                          ┃
┃                   tdlogger ┃
┖────────────────────────────┚

0
┎─────────────────────────────────┒
┃      --Method Execution--       ┃
┃ Alias: My Custom Logger         ┃
┃ Class: Sleep                    ┃
┃ Method: sleep                   ┃
┃ Count: 1                        ┃
┃ Exec Time: 1.001s               ┃
┃ Return Value: None              ┃
┃ Return Type: <class 'NoneType'> ┃
┃ Arguments: {                    ┃
┃     'n': 1                      ┃
┃ }                               ┃
┃                        tdlogger ┃
┖─────────────────────────────────┚
3

.
.
.

┎─────────────────────────────────┒
┃      --Method Execution--       ┃
┃ Alias: My Custom Logger         ┃
┃ Class: Sleep                    ┃
┃ Method: sleep                   ┃
┃ Count: 12                       ┃
┃ Exec Time: 1.000s               ┃
┃ Return Value: None              ┃
┃ Return Type: <class 'NoneType'> ┃
┃ Arguments: {                    ┃
┃     'n': 1                      ┃
┃ }                               ┃
┃                        tdlogger ┃
┖─────────────────────────────────┚

Removed 6 lines from 2 file(s) .

Process finished with exit code 0



```