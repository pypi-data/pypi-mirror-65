# Htpbs

Htpbs is a Python library that creates horizontal progress bars to keep 
track of the progress of threaded jobs. Bars in htpbs are completely customizable. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install htpbs.

```bash
pip install htpbs
```

## Usage

The following are examples about how to use this library for threaded and non threaded bars

### Threaded horizontal bars

```python
from htpbs import *
import time # required for demostration purposes only


# Note: users can create any configuration or function to be passed to the Work object below.
def work(progressbars, bar_index, work_value, work_name):
    """

    :param progressbars: the progressbar obkect
    :param bar_index: a integer representing the index of the bae
    :param work_value: a value for time.sleep() to simulate different progress bars rates
    :param work_name: the name of the work
    :return: VOID
    """
    progressbars.set_bar_prefix(bar_index=bar_index, prefix=work_name)
    for i in range(101):
             # your work here. we use the time.sleep() as example
             # Real work could be downloading a file and show progress
             time.sleep(work_value)
             progressbars.update(bar_index=bar_index, value=i)
    progressbars.finish()

# start with 3 bars
progressbars = ProgressBars(num_bars=3)
# set bar #3 to be the total progress
progressbars.set_last_bar_as_total_progress(prefix="Total: ")

# start all the threaded works
Work.start(work, (progressbars, 0, 0.1, "w1: "))
Work.start(work, (progressbars, 1, 0.01, "w2: "))

# output after works finished
# w1: |██████████| 100% completed   w2: |██████████| 100% completed    Total: |██████████| 100% completed
    
```

### Using the same thread

```python
from htpbs import *
import time # required for demostration purposes only

progressbars = ProgressBars(num_bars=5)
progressbars.set_last_bar_as_total_progress(prefix="Total Progress: ")

# set total progress bar at any index 
# progressbars.set_total_bar(index=3, prefix="total: ")

# using the same thread 
for i in range(101):
    time.sleep(0.1)
    values = [i, i+5, i+10, i+15, 0] # zero for init total progress 
    progressbars.update_all(values) # update bars in the same thread
progressbars.finish_all() # avoid memory leaks. 
```
### Remove bars when job is done and init the next bar
```python
# clearing and initializing new progress bars:
from htpbs import *
import time # required for demostration purposes only

progressbars = ProgressBars(num_bars=3)
progressbars.set_last_bar_as_total_progress(prefix="Total Progress: ")

# hide the bars that are not being used at the moment
# multiple bars can be hidden at the same time
progressbars.set_hidden_bars([1]) 

# non threaded work 1 starts
for i in range(101):
    time.sleep(0.1)
    progressbars.update(bar_index=0, value=i)
progressbars.finish()

# clears the bar that was completed from screen
progressbars.clear_bar(bar_index=0) 
# resets the new bar that will appear in screen
progressbars.reset_bar(index=1, prefix="new bar: ")   

# non threaded work 2 starts
for i in range(101):
    time.sleep(0.1)
    progressbars.update(bar_index=1, value=i)
progressbars.finish()

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/joseortizcostadev/hprogressbars/blob/master/LICENSE.txt)