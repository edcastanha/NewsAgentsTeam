from simpleclassifier.utils import *
from simpleclassifier.model import Model, defaultdict

class Classifier:
    def __init__(self, model:Model):
        """A simple text classifier that uses similarities between the text and the database to tell which entity is responsible.

        Args:
            model (Model): The model that will be used for classify.
        """
        self.model = model
    
    def getSimilarities(self, input: set) -> list:
        """Performs the process of filtering patterns similarities

        Args:
            input (set): Input processed by method `simpleclassifier.processText`.

        Returns:
            list: Result of similarities filtering.
        """
        similarities = []
        
        for entity in self.model.patterns:
            highest_similarity = 0
            context = None
            for pattern in self.model.patterns[entity]:
                similarity = getSimilarity(input, pattern)
                context = getContext(input, pattern)
                if similarity >= self.model.acceptable and similarity > highest_similarity:
                    highest_similarity = similarity
                if similarity == 1.0:
                    break
            if highest_similarity >= self.model.acceptable:
                similarities.append((entity, highest_similarity, context))
        
        return similarities

    def predict(self, input: set) -> bool | tuple:
        """Predict the entity responsible for the input by comparing the patterns

        Args:
            input (set): Input processed by method `simpleclassifier.processText`

        Returns:
            bool | tuple: False for when there is no similarity or a tuple with the responsible entity and its similarity
        """
        similarities = self.getSimilarities(input)

        if similarities:
            return max(similarities, key=lambda _similarity: _similarity[1])
        return False

class Trainer:
    def __init__(self, model:Model = Model()):
        """A simple trainer to store the patterns in your model.

        Args:
            model (Model, optional): The model that will be used for training, which may or may not exist. Defaults to Model().
        """
        self.model = model

    def train(self, entities: defaultdict | dict):
        """Trains the model using the inserted patterns

        Args:
            entities (defaultdict | dict): All patterns linked to each entity
        """
        for entity, patterns in entities.items():
            for pattern in patterns:
                self.model.setPattern(entity, pattern)
        self.model.save()
    
    def readPatterns(self, path: str, marker: str = "*"):
        """Reads a .txt document with training patterns.

        Args:
            path (str): Directory of document.
        """
        patterns = defaultdict(list)
        with open(path, "r", encoding="utf8") as file:
            current_entity = ""
            for row in file.readlines():
                row = row.strip("\n")
                if row.startswith(marker):
                    current_entity = row[1:]
                else:
                    patterns[current_entity].append(row)
        return patterns