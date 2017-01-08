# Autoparse

Autoparse is a small module for simple command-line argument parsing in
Python inspired by [this](https://github.com/simonw/optfunc/).

Advanced argument parsers like argparse and click can be a pain to use
when all you want to do is to parse a few simple arguments. With
autoparse, all you need to do is to write a Python function and call it.

## Example

Here's `example.py`:

```py
import autoparse

@autoparse.program
def main(host, port=1234, *, verbose=False, lol: [1, 2, 3] = 1):
    """Do something.

    Positional arguments:
      host          The hostname to connect to.
      port          The port to connect to, defaults to 1234.

    Optional arguments:
      --verbose     Print more status messages.
      --lol         An optional lol.
    """
    print('host:', repr(host))
    print('port:', repr(port))
    print('verbose:', repr(verbose))
    print('lol:', repr(lol))

if __name__ == '__main__':
    main()
```

The code is really short. The help message comes directly from the
docstring, so you have full control over how it looks and you don't need
to worry about how a parsing library happens to format it. Autoparse is
meant for simple things like this, there's so little arguments that
writing the help message by hand is not a problem.

Let's run our example:

```
$ python3 example.py localhost
host: 'localhost'
port: 1234
verbose: False
lol: 1
$ python3 example.py localhost 80
host: 'localhost'
port: 80
verbose: False
lol: 1
$ python3 example.py localhost 80 --verbose
host: 'localhost'
port: 80
verbose: True
lol: 1
$ python3 example.py localhost 80 --verbose --lol 3
host: 'localhost'
port: 80
verbose: True
lol: 3
$ python3 example.py --help
usage: example.py [-h] [--verbose] [--lol {1,2,3}] host [port]

Do something.

Positional arguments:
  host          The hostname to connect to.
  port          The port to connect to, defaults to 1234.

Optional arguments:
  --verbose     Print more status messages.
  --lol         An optional lol.
```

Autoparse is implemented using
[argparse](https://docs.python.org/3/library/argparse.html), so the
example program also produces informative error messages. Unlike plain
argparse, it also asks the user to try `--help`:

```
$ python3 example.py
example.py: error: the following arguments are required: host
Run 'example.py --help' for more info.
$ python3 example.py localhost asdf
example.py: error: argument port: invalid int value: 'asdf'
Run 'example.py --help' for more info.
$ python3 example.py localhost --verbose=lul
example.py: error: argument --verbose: ignored explicit argument 'lul'
Run 'example.py --help' for more info.
$ python3 example.py localhost --lol=4
example.py: error: argument --lol: invalid choice: 4 (choose from 1, 2, 3)
Run 'example.py --help' for more info.
```
