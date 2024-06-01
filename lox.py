import dataclasses
import enum
import sys
from typing import Any


class TokenType(enum.Enum):
    # Single character tokens
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    LEFT_BRACE = enum.auto()
    RIGHT_BRACE = enum.auto()
    COMMA = enum.auto()
    DOT = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    SEMICOLON = enum.auto()
    SLASH = enum.auto()
    STAR = enum.auto()

    # One or two character tokens
    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS = enum.auto()
    LESS_EQUAL = enum.auto()

    # Literals
    IDENTIFIER = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()

    # Keywords
    AND = enum.auto()
    CLASS = enum.auto()
    ELSE = enum.auto()
    FALSE = enum.auto()
    FUN = enum.auto()
    FOR = enum.auto()
    IF = enum.auto()
    NIL = enum.auto()
    OR = enum.auto()
    PRINT = enum.auto()
    RETURN = enum.auto()
    SUPER = enum.auto()
    THIS = enum.auto()
    TRUE = enum.auto()
    VAR = enum.auto()
    WHILE = enum.auto()

    EOD = enum.auto()


@dataclasses.dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self) -> None:
        pass


class Lox:
    def __init__(self) -> None:
        self._had_error = False

    def _report(self, line: int, where: str, message: str):
        print(f"[Line {line}] Error {where}: {message}", file=sys.stderr)
        self._had_error = True

    def error(self, line: int, message: str):
        self._report(line, "", message)

    def _run(self, source: str):
        scanner = Scanner()
        tokens = scanner.scan_tokens()

        # for now, just print tokens
        for token in tokens:
            print(token)

    def run_file(self, path: str) -> None:
        with open(path, "r") as f:
            text = f.read()
        self._run(text)
        if self._had_error:
            sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            print("> ", end="", flush=True)
            try:
                line = next(sys.stdin)
            except StopIteration:
                print()
                break
            self._run(line)
            self._had_error = False


def main():
    args = sys.argv
    if len(args) > 2:
        print("Usage: python3 lox.py [script]")
        sys.exit(64)
    lox = Lox()
    if len(args) == 2:
        lox.run_file(args[1])
    else:
        lox.run_prompt()


main()
