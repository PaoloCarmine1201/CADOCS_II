from typing import List
from abc import ABC, abstractmethod

# The Strategy interface declares operations common to all supported versions of some algorithm.
# The Context uses this interface to call the algorithm defined by Concrete Strategies.
# ABC stands for Abstract Base Classes
class Tool(ABC):
    @abstractmethod
    def execute_tool(self, data: List):
        pass
