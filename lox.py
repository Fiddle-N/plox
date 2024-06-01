import string
import sys
from typing import NamedTuple

from lox_token import Token, TokenType


class ErrorHandler:

    def __init__(self) -> None:
        self._had_error = False

    def error(self, line: int, message: str, where: str = ''):
        print(f"[Line {line}] Error {where}: {message}", file=sys.stderr)
        self._had_error = True

    @property
    def had_error(self):
        return self._had_error


def _is_ascii_digit(char: str) -> bool:
    if len(char) != 1:
        raise ValueError
    return char in string.digits


def _is_ascii_alpha(char: str) -> bool:
    if len(char) != 1:
        raise ValueError
    return char in (string.ascii_letters + '_')


def _is_ascii_alphanum(char: str) -> bool:
    return _is_ascii_alpha(char) or _is_ascii_digit(char)


class Scanner:

    SINGLE_CHAR_TOKENS = {
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '-': TokenType.MINUS,
        '+': TokenType.PLUS,
        ';': TokenType.SEMICOLON,
        '*': TokenType.STAR,
    }

    class OpTokenPair(NamedTuple):
        with_equal: TokenType
        single: TokenType

    OP_TOKENS = {
        '!': OpTokenPair(with_equal=TokenType.BANG_EQUAL, single=TokenType.BANG),
        '=': OpTokenPair(with_equal=TokenType.EQUAL_EQUAL, single=TokenType.EQUAL),
        '<': OpTokenPair(with_equal=TokenType.LESS_EQUAL, single=TokenType.LESS),
        '>': OpTokenPair(with_equal=TokenType.BANG_EQUAL, single=TokenType.BANG),
    }

    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS, 
        "else": TokenType.ELSE,
        "false": TokenType.FALSE, 
        "fun": TokenType.FUN, 
        "for": TokenType.FOR, 
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT, 
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE, 
    }

    def __init__(self, source: str, error_handler: ErrorHandler) -> None:
        self._source = source
        self._error_handler = error_handler
        self._tokens: list[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)
    
    def _advance(self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char
    
    def _match(self, exp: str) -> bool:
        # conditional advance
        if self._is_at_end() or self._source[self._current] != exp:
            return False
        self._current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self._source[self._current]
    
    def _peek_next(self) -> str:
        if (self._current + 1) >= len(self._source):
            return '\0'
        return self._source[self._current + 1]
    
    def _add_token(self, type_: TokenType, literal: object = None) -> None:
        text = self._source[self._start: self._current]
        self._tokens.append(Token(type=type_, lexeme=text, literal=literal, line=self._line))
    
    def _scan_token(self):
        c = self._advance()

        match c:
            case c if c in self.SINGLE_CHAR_TOKENS:
                self._add_token(self.SINGLE_CHAR_TOKENS[c])

            case c if c in self.OP_TOKENS:
                op_token = self.OP_TOKENS[c]
                self._add_token(op_token.with_equal if self._match("=") else op_token.single)

            case '/' if self._match('/'):
                # within a comment
                while (self._peek() != '\n' and not self._is_at_end()):
                    self._advance()

            case '/':
                self._add_token(TokenType.SLASH)

            case ' ' | '\t' | '\n':
                pass
            
            case '"':
                # scan string
                while (self._peek() != '"' and not self._is_at_end()):
                    if self._peek() == '\n':
                        self._line += 1
                    self._advance()
                
                if self._is_at_end():
                    self._error_handler.error(line=self._line, message="Unterminated string.")
                    return
                
                # consume closing "
                self._advance()

                # get value with trimmed quotes
                value = self._source[self._start + 1: self._current - 1]
                self._add_token(TokenType.STRING, value)

            case c if _is_ascii_digit(c):
                # scan number
                while _is_ascii_digit(self._peek()):
                    self._advance()
                
                if self._peek() == '.' and _is_ascii_digit(self._peek_next()):
                    # Consume .
                    self._advance()

                    while _is_ascii_digit(self._peek()):
                        self._advance()

                self._add_token(TokenType.NUMBER, float(self._source[self._start: self._current]))

            case c if _is_ascii_alpha(c):
                # scan identifier
                while _is_ascii_alphanum(self._peek()):
                    self._advance()

                text = self._source[self._start: self._current]
                type_ = self.KEYWORDS.get(text)
                if type_ is None:
                    type_ = TokenType.IDENTIFIER
                self._add_token(type_=type_)

            case _:
                self._error_handler.error(line=self._line, message="Unexpected character")

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()
        
        self._tokens.append(Token(type=TokenType.EOF, lexeme="", literal=None, line=self._line))
        return self._tokens


def _run(source: str) -> bool:
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler=error_handler)
    tokens = scanner.scan_tokens()

    # for now, just print tokens
    for token in tokens:
        print(token)

    return error_handler.had_error


def run_file(path: str) -> None:
    with open(path, "r") as f:
        text = f.read()
    had_error = _run(text)
    if had_error:
        sys.exit(65)


def run_prompt() -> None:
    while True:
        print("> ", end="", flush=True)
        try:
            line = next(sys.stdin)
        except StopIteration:
            print()
            break
        _run(line)


def main():
    args = sys.argv
    if len(args) > 2:
        print("Usage: python3 lox.py [script]")
        sys.exit(64)
    if len(args) == 2:
        run_file(args[1])
    else:
        run_prompt()


main()
