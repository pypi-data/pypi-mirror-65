# gdbundle-gdb-dashboard

This is a [gdbundle](https://github.com/memfault/gdbundle) plugin for [cyrus-and/gdb-dashboard](https://github.com/cyrus-and/gdb-dashboard)

## Compatibility

- GDB

## Installation

After setting up [gdbundle](https://github.com/memfault/gdbundle), install the package from PyPi. 

```
$ pip install gdbundle-gdb-dashboard
```

If you've decided to manually manage your packages using the `gdbundle(include=[])` argument,
add it to the list of plugins.

```
# .gdbinit

[...]
import gdbundle
plugins = ["gdb-dashboard"]
gdbundle.init(include=plugins)
```

## Building

To build this package, it requires calling `make` first as we need to download the `.gdbinit` file from the actual repository since it isn't packaged as a Python package.

```
$ make
$ poetry build
$ poetry publish
```
