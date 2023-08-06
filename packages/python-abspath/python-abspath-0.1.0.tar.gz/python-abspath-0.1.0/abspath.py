import click
import os
import json


@click.command()
@click.option("-q", "--with-quotes", is_flag=True)
@click.argument("path", nargs=-1, required=False)
def print_abspath(with_quotes, path):
    if path:
        paths = path
    else:
        paths = [x.strip() for x in os.sys.stdin.readlines() if x.strip()]
    for path in paths:
        path = os.path.abspath(path)
        if with_quotes:
            print(json.dumps(path, ensure_ascii=False))
        else:
            print(path)

if __name__ == "__main__":
    print_abspath()
