# test.py
from crewai_tools import tool

@tool
def hello(name: str):
    return f"Hello, {name}!"

print(hello("Rohan"))
