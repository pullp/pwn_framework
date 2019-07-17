# pwn_framework


## usage

### add to python path

```bash
export PYTHONPATH=path/to/this/dir
```

### generate exp template

```python
import pwn_framework.utils as pu
pu.template("file name", "host", port)
```

then you can find a `exp.py` in current dir

### change ld of a elf file

```python
import pwn_framework.utils as pu
pu.change_ld("file name", "version") # such as 2.23
```

ps: you should modify `change_ld()` in `utils.py` to tell the framework where the `libc.so`s and `ld.so`s are.

as for how to get multiple version of `glibc`s and `ld`s you can search with google or refer to this [post](https://www.jianshu.com/p/ee1ad4044ef7)

