import pytest
from src.agents.tools.python_interpreter_tool import safe_calculate

def test_safe_calculator():
    assert safe_calculate("2 + 3 * 4") == 14.0

def test_safe_calculator_rejects_code():
    with pytest.raises(ValueError):
        safe_calculate("__import__('os').system('echo nope')")
