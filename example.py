import autoparse

@autoparse.program
def main(host, port=1234, *, verbose=False, lol: [1, 2, 3] = 1):
    """Do something.

    Positional arguments:
      host          The hostname to connect to.
      port          The port to connect to.

    Optional arguments:
      --verbose     Print more status messages.
      --lol         One of 1, 2 or 3.
    """
    print('host:', repr(host))
    print('port:', repr(port))
    print('verbose:', repr(verbose))
    print('lol:', repr(lol))

if __name__ == '__main__':
    main()
