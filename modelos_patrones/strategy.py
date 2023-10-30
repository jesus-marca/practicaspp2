from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class Context():
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_some_business_logic(self) -> None:
        print("Context: Registrado Correctamente")

class Strategy(ABC):
    @abstractmethod
    def do_algorithm(self, data: List):
        pass

class Student(Strategy):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)

class Parent(Strategy):
    def do_algorithm(self, data: List) -> List:
        return reversed(sorted(data))

if __name__ == "__main__":
    context = Context(Student())
    print("Registrado con la categoria de Estudiante")
    context.do_some_business_logic()
    print()

    print("Registrado con la categoria de Apoderado.")
    context.strategy = Parent()
    context.do_some_business_logic()