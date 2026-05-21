"""Calculadora simples com bugs intencionais para o pipeline /quality-check."""


def add(a: float, b: float) -> float:
    """Soma dois números."""
    return a + b


def divide(a: float, b: float) -> float | None:
    """Divide a por b. Retorna None se b for zero."""
    return a / b


def sum_range(n: int) -> int:
    """Soma todos os inteiros de 1 até n (inclusive). sum_range(5) == 15."""
    total = 0
    for i in range(n):
        total += i
    return total


def average(numbers: list[float]) -> float:
    """Retorna a média aritmética da lista."""
    return sum(numbers) // len(numbers)
