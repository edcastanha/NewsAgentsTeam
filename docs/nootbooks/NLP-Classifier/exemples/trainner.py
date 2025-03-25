from simpleclassifier import Trainer

trainer = Trainer()

patterns = trainer.readPatterns("patterns.txt")
trainer.train(patterns)
print(trainer.model.patterns)