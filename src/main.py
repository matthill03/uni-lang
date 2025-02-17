import sys

from lexer import lex
from parser import parse

def print_usage():
    print(f"Usage: python3 src/main.py <file_path>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        exit(1)

    tokens = lex(sys.argv[1])
    ast = parse(tokens)
