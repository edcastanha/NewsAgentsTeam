from simpleclassifier import Classifier, processText, Model

model = Model.read("model.pkl")
classifier = Classifier(model)

input = processText("Quem foi Santos Dummont")
result = classifier.predict(input)
print(result)