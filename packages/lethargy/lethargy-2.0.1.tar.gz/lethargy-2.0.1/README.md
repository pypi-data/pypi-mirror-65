# Lethargy — Declarative option parsing, for developers

[![Released version (shield)]][Version URL]
[![Size (shield)]][Size URL]

[Released version (shield)]: https://img.shields.io/pypi/v/lethargy?color=blue
[Version URL]: https://pypi.org/project/lethargy

[Size (shield)]: https://img.shields.io/badge/size-14%20kB-blue
[Size URL]: https://github.com/SeparateRecords/lethargy/tree/master/lethargy
<!-- Size correct as at e4db57f (March 16, 2020) -->

Lethargy takes care of option parsing in your scripts, so you can be more productive when writing the important stuff. It's simple, concise, explicit, and Pythonic.

Unlike [Click](https://click.palletsprojects.com/en/7.x/) and [Argparse](https://docs.python.org/3/library/argparse.html), Lethargy is succinct, can be implemented without changing the structure of a program, and requires no boilerplate code. This makes it especially suited to scripting and prototyping.

By design, it is not a full argument parser. If you're building a complete CLI application, you're probably better off using Click.

<a name="installation"></a>

## Installation

Lethargy only depends on the standard library. You can use [pip](https://pip.pypa.io/en/stable/) to install lethargy.

```bash
pip install lethargy
```

<a name="usage"></a>

## Usage

```python
from lethargy import Opt

# --use-headers
headers = Opt("use headers").take_flag()

# -f|--file <value>
output_file = Opt("f", "file").takes(1).take_args()
```

Lethargy returns values appropriate to the option, safely mutating the argument list.

<a name="getting-started"></a>

## Getting Started

<a name="argv"></a>

### The default `argv`

To save you an additional import, lethargy provides `lethargy.argv` - a clone of the original argument list. Mutating it will not affect `sys.argv`.

**Important note:** `lethargy.argv` is used as a mutable default argument for `lethargy.Opt.take_args` and `lethargy.Opt.take_flag`. Examples below override this value to demonstrate mutation, but in real-world usage, omitting the argument list is recommended (see example in [Usage](#usage)).

<a name="options"></a>

### Options

Options will automatically convert their names to the appropriate format (`-o` or `--option`). Casing will be preserved.

```python
>>> from lethargy import Opt
>>> args = ["-", "--debug", "file.txt"]
>>> Opt("debug").take_flag(args)
True
>>> args
['-', 'file.txt']
```

To set the number of arguments to take, use the `Opt.takes` method.

```python
>>> args = ["-", "--height", "185cm", "people.csv"]
>>> Opt("height").takes(1).take_args(args)
'185cm'
>>> args
['-', 'people.csv']
```

Taking 1 argument will return a single value. Taking multiple will return a list (see the [Argument unpacking](#unpacking) section for details).

You can also use a "greedy" value, to take every remaining argument. The canonical way to do this is using the Ellipsis literal (`...`).

```python
>>> args = ["--exclude", ".zshrc", ".bashrc"]
>>> Opt("exclude").takes(...).take_args(args)
['.zshrc', '.bashrc']
```

<a name="unpacking"></a>

### Argument unpacking

`lethargy.Opt` makes sure it's safe to unpack a returned list of values, unless you override the `default` parameter.

```python
>>> Opt("x").takes(2).take_args(["-x", "1", "2"])
['1', '2']
>>> Opt("y").takes(2).take_args([])
[None, None]
```

If there are fewer arguments than expected, `lethargy.ArgsError` will be raised and no mutation will occur. Lethargy has clear and readable error messages.

```python
>>> args = ["-z", "bad"]
>>> Opt("z").takes(2).take_args(args)
Traceback (most recent call last):
...
lethargy.ArgsError: expected 2 arguments for '-z <value> <value>', found 1 ('bad')
>>> args
['-z', 'bad']
```

<a name="debug-and-verbose"></a>

### `--debug` and `-v`/`--verbose` flags

As these are such common options, lethargy includes functions out of the box to take these options.

```python
>>> import lethargy
>>> args = ["-", "--debug", "--verbose", "sheet.csv"]
>>> lethargy.take_verbose(args)  # -v or --verbose
True
>>> lethargy.take_debug(args)
True
>>> args
["-", "sheet.csv"]
```

By convention, passing `--verbose` will cause a program to output more information. To make implementing this behaviour easier, lethargy has the `print_if` function, which will return `print` if its input is true and a dummy function if not.

```python
from lethargy import take_verbose, print_if

verbose_print = print_if(take_verbose())

verbose_print("This will only print if `--verbose` or `-v` were used!")
```

<a name="str-and-repr"></a>

### Using `str` and `repr`

`Opt` instances provide a logical and consistent string form.

```python
>>> str(Opt("flag"))
'--flag'
>>> str(Opt("e", "example").takes(1))
'-e|--example <value>'
>>> str(Opt("xyz").takes(...))
'--xyz [value]...'
```

The `repr` form makes debugging easy. Note that the order of the names is not guaranteed.

```python
>>> Opt("f", "flag")
<Opt('-f', '--flag') at 0x106d73f70>
>>> Opt("example").takes(2)
<Opt('--example').takes(2) at 0x106ce35e0>
>>> Opt("test").takes(1, int)
<Opt('--test').takes(1, int) at 0x106d73f70>
>>> Opt("x").takes(..., lambda s: s.split())
<Opt('-x').takes(Ellipsis, <function <lambda> at 0x106ddd9d0>) at 0x106ec0a30>
```

<a name="raising"></a>

### Raising instead of defaulting

If `Opt.take_args` is called with `raises=True`, `lethargy.MissingOption` will be raised instead of returning a default, even if the default is set explicitly.

This behaviour makes it easy to implement mandatory options.

```python
from lethargy import Opt, MissingOption

opt = Opt('example').takes(1)

try:
    value = opt.take_args(raises=True)
except MissingOption:
    print(f'Missing required option: {opt}')
    exit(1)
```

<a name="conversion"></a>

### Value conversion

`Opt.takes` can optionally take a callable, which will be used to convert the result of `Opt.take_args`. No additional error handling is performed, and the default value will not be converted.

```python
>>> Opt('n').takes(1, int).take_args(['-n', '28980'])
28980
>>> Opt('f').takes(2, float).take_args(['-f', '1', '3.1415'])
[1.0, 3.1415]
>>> Opt('chars').takes(1, set).take_args([])
None
>>> Opt('chars').takes(1, set).take_args([], d='Default')
'Default'
```

<a name="mutation"></a>

### Disabling mutation

`Opt.take_args` and `Opt.take_flag` both take the optional keyword argument `mut`. Setting `mut` to False disables mutation.

```python
>>> lst = ["--name", "test",  "example"]
>>> Opt("name").takes(2).take_args(lst, mut=False)
['test', 'example']
>>> lst  # It hasn't changed!
['--name', 'test', 'example']
```

<a name="contributing"></a>

## Contributing

Any contributions and feedback are welcome! I'd appreciate it if you could open an issue to discuss changes before submitting a PR, but it's not enforced.

<a name="license"></a>

## License

Lethargy is released under the [MIT license](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE).
