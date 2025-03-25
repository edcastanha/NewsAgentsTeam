import pickle
from collections import defaultdict
from simpleclassifier import processText

class Model:
    def __init__(self, acceptable:float = 0.55, dir:str = "model.pkl"):
        """A model of learned patterns to be classified.

        Args:
            acceptable (float, optional): The acceptable value to understand as similar. Defaults to 0.55.
            dir (str, optional): The model directory. Defaults to "model.pkl".
        """
        self.patterns = defaultdict(list)
        self.acceptable = acceptable
        self.dir = dir
    
    def __str__(self) -> str:
        return f"Model(patterns= {self.getAmount()}, acceptable= {self.acceptable}, dir= '{self.dir}')"
    
    def getAmount(self) -> int:
        """Returns the amount of patterns

        Returns:
            int: Amount
        """
        return sum(len(patterns) for patterns in self.patterns.values())
    
    def setPattern(self, entity:str, pattern:str):
        """Defines a new pattern for an entity

        Args:
            entity (str): Responsible entity
            pattern (str): New pattern
        """
        self.patterns[entity].append(processText(pattern))
    
    def save(self):
        """Save the model in a pickle document.
        """
        with open(self.dir, "wb+") as f:
            pickle.dump(self, f)

    def read(dir: str):
        """Read the model in a pickle document.
        """
        with open(dir, "rb") as f:
            return pickle.load(f)