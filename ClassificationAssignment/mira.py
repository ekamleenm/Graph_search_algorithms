# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 


# Mira implementation
import util

PRINT = True


class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter()  # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels)
        self.weights = weights

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys()  # this could be useful for your code later...

        if (self.automaticTuning):
            cGrid = [0.001, 0.002, 0.004, 0.008]
        else:
            cGrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, cGrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, cGrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        bestWeights = None
        bestAccuracyCount = -1  # best accuracy so far on validation set
        cGrid.sort(reverse=True)
        bestParams = cGrid[0]

        "*** YOUR CODE HERE ***"
        for C in cGrid:
            # Copy the current weights for training with this specific C value
            weights = self.weights.copy()

            for iteration in range(self.max_iterations):
                for i, datum in enumerate(trainingData):
                    # Compute the scores for each label
                    scores = util.Counter()
                    for label in self.legalLabels:
                        scores[label] = weights[label] * datum

                    # Predict the label with the highest score
                    predicted_label = scores.argMax()

                    actual_label = trainingLabels[i]

                    # If the prediction is wrong, update weights
                    if predicted_label != actual_label:
                        # Compute tau for the weight update
                        tau = min(C, ((weights[predicted_label] - weights[actual_label]) * datum + 1.0) / (
                                    2.0 * (datum * datum)))

                        # Scale datum by tau
                        scaledDatum = datum.copy()
                        for key in scaledDatum:
                            scaledDatum[key] *= tau

                        # Update weights
                        weights[actual_label] += scaledDatum
                        weights[predicted_label] -= scaledDatum

            # Evaluate accuracy on validation data
            self.weights = weights  # temporarily set weights to current C's weights
            validationGuesses = self.classify(validationData)
            correctCount = sum(int(validationGuesses[i] == validationLabels[i]) for i in range(len(validationLabels)))

            # Check if the current C value gives the best accuracy
            if correctCount > bestAccuracyCount:
                bestAccuracyCount = correctCount
                bestWeights = weights.copy()
                bestParams = C

        # Set the best weights found
        self.weights = bestWeights
        print("finished training. Best cGrid param = ", bestParams)

    def classify(self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        "*** YOUR CODE HERE ***"
        for datum in data:
            scores = util.Counter()
            for label in self.legalLabels:
                scores[label] = self.weights[label] * datum
            guesses.append(scores.argMax())
        return guesses

    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        # Sort features by weight in descending order
        sorted_features = self.weights[label].sortedKeys()

        # Select the top 100 features
        featuresWeights = sorted_features[:100]

        return featuresWeights
