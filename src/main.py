from lexer import lex
from parser import parse

if __name__ == "__main__":
    tokens = lex("examples/maths.qk")
    ast = parse(tokens)
