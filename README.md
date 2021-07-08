
# linyP

Progress display for threaded tasks in python

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSE)


## Installation

Installation using pip3

```bash
pip3 install git+git://github.com/furrygem/linyP
```

Installation using ``setup.py`` file

```bash
git clone git://github.com/furrygem/linyP
cd linyP
python3 setup.py install
```
## Usage/Examples

```python
from linyP import LinyProgresses
import time
from threading import Thread
a = [0.3, 0.08, 0.1, 0.01] 
lp = LinyProgresses(4,[("Running", "Done", "Error", 100)]*4, "${CV} / ${MV} ${ST}") # initializing LinyProgress
def Process(tid):
    
    for i in range(100):
        lp.add(1, tid) # continuously adding 1 to total progress.
        time.sleep(a[tid]) # sleeping for some time
        
def Progress():
    while lp.checkIfDone() != True: #checkIfDone() returnes True if all progresses completed
        time.sleep(0.05) # waiting some time before re-render
        lp.display_all() # display_all() displays all progresses
threads = []
for i in range(4):
    threads.append(Thread(target=Process, args=(i,)))

lp.prepare()
lp.display_all()
for thread in threads:
    thread.start()
Progress()
print('\n')
```


  
## Screenshots
The output of code above

![Screenshot](https://raw.githubusercontent.com/furrygem/linyP/main/progress.gif)
