from dataclasses import dataclass

from lox_token import Token, TokenType


class Expr:
    pass


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __str__(self) -> str:
        return f"({self.operator.lexeme} {self.left} {self.right})"


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

    def __str__(self) -> str:
        return f"(group {self.expression})"


@dataclass(frozen=True)
class Literal(Expr):
    value: object

    def __str__(self) -> str:
        if self.value is None:
            return "nil"
        return str(self.value)


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def __str__(self) -> str:
        return f"({self.operator.lexeme} {self.right})"


def main():
    expr = Binary(
        Unary(
            Token(type=TokenType.MINUS, lexeme="-", literal=None, line=1),
            Literal(123)
        ),
        Token(type=TokenType.STAR, lexeme="*", literal=None, line=1),
        Grouping(Literal(45.67))
    )
    print(expr)


if __name__ == '__main__':
    main()
