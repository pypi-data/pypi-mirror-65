# python-abspath

python-abspath provides a command line tool that prints the absolute paths of all given files. File names can be piped via STDIN or given as arguments. Work for both Windows and Linux.

## Install

```shell
pip install python-abspath
```

## Installed Command Line Tools

- abspath

## Usage

```shell
C:\Code\python-abspath>abspath --help
Usage: abspath.py [OPTIONS] [PATH]...

Options:
  -q, --with-quotes
  --help             Show this message and exit.
```

## Example

**Example 1:** 

Show the absolute path of requirements.txt. requirements.txt is given as a parameter.

```shell
C:\Code\python-abspath>abspath requirements.txt
C:\Code\python-abspath\requirements.txt
```

**Example 2:**

Show the absolute path of a.txt and b.txt. a.txt and b.txt are given as parameters.

```shell
C:\Code\python-abspath>abspath a.txt b.txt
C:\Code\python-abspath\a.txt
C:\Code\python-abspath\b.txt
```

**Example 3:**

Filename or filenames can be piped via STDIN.

```shell

C:\Code\python-abspath>echo a.txt | abspath
C:\Code\python-abspath\a.txt

C:\Code\python-abspath>type filenames.txt
a.txt
b.txt
c.txt

C:\Code\python-abspath>type filenames.txt | abspath
C:\Code\python-abspath\a.txt
C:\Code\python-abspath\b.txt
C:\Code\python-abspath\c.txt
```

**Example 4:** 

In window the filename seperator is "\\", so you can NOT just copy the output and paste as a const value to your code. You have to add -q option, so that the output will be quoted and you can use it in you code.

```shell
C:\Code\python-abspath>abspath -q requirements.txt
"C:\\Code\\python-abspath\\requirements.txt"
```

## Releases

### v0.1.0 2020/04/09

- First release.