from langchain_core.tools import tool

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        The sum of a and b
    """
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number.
    
    Args:
        a: Number to subtract from
        b: Number to subtract
        
    Returns:
        The result of a minus b
    """
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.
    
    Args:
        a: First number to multiply
        b: Second number to multiply
        
    Returns:
        The product of a and b
    """
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number.
    
    Args:
        a: Number to be divided (dividend)
        b: Number to divide by (divisor)
        
    Returns:
        The result of a divided by b
        
    Raises:
        ValueError: If attempting to divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def get_calculator_tools():
    """Get all calculator tools as a list.
    
    Returns:
        List of calculator tool functions
    """
    return [add, subtract, multiply, divide]