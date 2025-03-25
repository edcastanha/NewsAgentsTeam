PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

processText = lambda text: {word.lower() for word in text.split() if not word in PUNCTUATION}
getSimilarity = lambda input, pattern: len(pattern.intersection(input)) / len(pattern)
getContext = lambda input, pattern: input.difference(pattern)