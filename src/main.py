import sys

from lexer import lex
from parser import parse

def get_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    return content

def process(src):
    tokens = lex(src)
    ast = parse(tokens)

def run_file(file_path):
    src = get_file_content(file_path)
    process(src)

def run_interactive():
    print("Welcome to the world of qwrk (0.0.1)...")
    usr_input = ""

    while usr_input != "exit":
        usr_input = input('> ')
        process(usr_input)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        run_interactive()

    run_file(sys.argv[1])
