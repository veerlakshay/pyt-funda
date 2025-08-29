def add(a: float, b: float) -> float:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero not allowed")
    return a / b

def mul(a, b):
    return a * b

def safe_sub(a , b, * , non_negative = False):
    if non_negative and a - b < 0:
        raise ValueError("Result would be negative")
    else:
        return a -b

