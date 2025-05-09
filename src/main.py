import sys

from lexer import lex
from parser import parse
from interpreter import interpret

def get_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    return content

def print_usage():
    print("USAGE: python src/main.py <file_to_run>")

def process(src):
    tokens = lex(src)
    ast_root = parse(tokens)
    interpret(ast_root)

def run_file(file_path):
    src = get_file_content(file_path)
    process(src)

def run_interactive():
    print("Welcome to the world of qwrk (0.0.1)...")
    usr_input = ""

    while True:
        usr_input = input('> ')
        if usr_input == "exit":
            break

        process(usr_input)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        exit(0)

    run_file(sys.argv[1])
