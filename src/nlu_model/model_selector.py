from __future__ import annotations
from .CADOCS import LanguageModel
from typing import List

# The structure of the strategy has been created following: https://refactoring.guru/design-patterns/strategy/python/example

# this is the context for our strategy pattern
class ModelSelector():
    def __init__(self, strategy: LanguageModel) -> None:
        self._strategy = strategy

    # The Context maintains a reference to one of the Strategy objects. 
    # The Context does not know the concrete class of a strategy. 
    # It should work with all strategies via the Strategy interface
    @property
    def strategy(self) -> LanguageModel:
        return self._strategy
    
    # we could change the strategy, even at runtime
    @strategy.setter
    def strategy(self, strategy: LanguageModel) -> None:
        self._strategy = strategy

    # we run whichever tool has been selected as the strategy
    def run(self, message) -> dict:
        result = self._strategy.give_prediction(message)
        return result
