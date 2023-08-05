# Out Of ~~Mana~~ Memory

Provides a function that keeps an eye on your RAM and stops executing of the process if you are running out of memory.

## Installation

To install oom enter this in your terminal.

```bash
pip install oom
```

## Usage

### Example 1: The simplest

```python
from oom import exit_on_out_of_ram

one_gigabyte = 1 << 30
exit_on_out_of_ram(one_gigabyte)

# explode your RAM
extremely_big_number = 1 << 9999999
_ = [i for i in range(extremely_big_number)]
```

### Example 2: Full

```python
from oom import exit_on_out_of_ram

one_gigabyte = 1 << 30
exit_on_out_of_ram(
    terminate_on=one_gigabyte,
    warn_on = 2 * one_gigabyte,
    sleep_time=1,
    notify_about_using=True
)

# explode your RAM
extremely_big_number = 1 << 9999999
_ = [i for i in range(extremely_big_number)]
```

### Example 3: Script wrapper

```bash
python3 -m oom -t 1024 examples/for_example_3.py
```
