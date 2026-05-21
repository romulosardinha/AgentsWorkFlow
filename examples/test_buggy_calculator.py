"""Testes que validam o contrato declarado nas docstrings de buggy_calculator.

Rode com: pytest examples/test_buggy_calculator.py -v

Antes do /quality-check: 3 falhas.
Depois do /quality-check: tudo verde.
"""

from buggy_calculator import add, average, divide, sum_range


def test_add_basico():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_divide_normal():
    assert divide(10, 2) == 5.0


def test_divide_por_zero_retorna_none():
    # Docstring promete: "Retorna None se b for zero"
    assert divide(10, 0) is None


def test_sum_range_inclui_n():
    # Docstring promete: sum_range(5) == 15 (soma 1+2+3+4+5)
    assert sum_range(5) == 15
    assert sum_range(1) == 1
    assert sum_range(10) == 55


def test_average_retorna_float():
    # "Média aritmética" implica divisão real, não inteira
    assert average([1, 2, 3, 4]) == 2.5
    assert average([10, 20]) == 15.0
