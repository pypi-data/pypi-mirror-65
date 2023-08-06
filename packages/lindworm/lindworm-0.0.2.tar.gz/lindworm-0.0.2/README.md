# lindworm

lindworm is a pure python package.

## dependencies

Python 3 is required  
use of anaconda recommended.

packages used:

+ [pandas](https://pandas.pydata.org/)
+ [pysimplegui](https://pypi.org/project/PySimpleGUI/)
+ [wxPython](https://www.wxpython.org/)

## install

run `setup.py` in project root folder,
e.g. following line to create binary wheel file.

```shell
python setup.py bdist_wheel
```

generated wheel file reside in folder `./dist`:  
`lindworm-x.y.z-py3-none-any.whl`
assuming `lindworm/__init__.py` has variable `__version__` set.

```python
__version__ = "x.y.z"
```

```shell
pip install ./dist/lindworm-x.y.z-py3-none-any.whl
```

source install

```shell
python setup.py install
```

## unistall

in case version number is not changed, pip will not install
update, therefore package can be uninstalled.

```shell
pip uninstall ./dist/lindworm-x.y.z-py3-none-any.whl
```

## setup

+ vscode
  set `Python: Env File` to `${workspaceFolder}/dlp.env`
  ![vscode settings](./e_scr/vscode_20191230_094105.png)

`dlp.env` add current workspace folder to python search path,
therefore enable package import without having to install in advance.
Very useful for performing unit tests.

```shell
PYTHONPATH=${workspaceFolder}:${PYTHONPATH}
```

## markdown

some manual found online

+ [cheat](d_man/markdown-cheatsheet-online.pdf)
+ [guide](d_man/markdown-guide.pdf)

## pandoc

[pandoc][pandoc_home] is a flexible document converter.
see [manual][pandoc_man]  

[example](d_howto/pandoc_tut.md)

[mdSyntax]: https://sourceforge.net/p/scintilla/wiki/markdown_syntax/

[pandas]: https://pandas.pydata.org/

[pysimplegui]: https://pypi.org/project/PySimpleGUI/

[pandoc_home]: https://pandoc.org/index.html
[pandoc_man]: https://pandoc.org/MANUAL.html
[pandoc_github]: https://github.com/jgm/pandoc
[pandoc_wiki]: https://github.com/jgm/pandoc/wiki
[pandoc_tricks]: https://github.com/jgm/pandoc/wiki/Pandoc-Tricks
