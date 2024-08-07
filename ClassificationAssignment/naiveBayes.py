# naiveBayes.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#

import util
import classificationMethod
import math
import random


class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels):
        super().__init__(legalLabels)
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1
        self.automaticTuning = False

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([f for datum in trainingData for f in datum.keys()]))

        if self.automaticTuning:
            kgrid = [0.0005, 0.001, 0.005, 0.01, 0.02, 0.05, 0.5, 1, 5, 10, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        bestAccuracyCount = -1
        commonPrior = util.Counter()
        commonConditionalProb = util.Counter()
        commonCounts = util.Counter()

        bestParams = (commonPrior, commonConditionalProb, kgrid[0])

        for i in range(len(trainingData)):
            datum = trainingData[i]
            label = trainingLabels[i]
            "*** YOUR CODE HERE to complete populating commonPrior, commonCounts, and commonConditionalProb ***"
            commonPrior[label] += 1
            for feat, value in datum.items():
                commonCounts[(feat, label)] += 1
                if value > 0:
                    commonConditionalProb[(feat, label)] += 1

        for k in kgrid:
            prior = util.Counter()
            conditionalProb = util.Counter()
            counts = util.Counter()

            for key, val in commonPrior.items():
                prior[key] += val
            for key, val in commonCounts.items():
                counts[key] += val
            for key, val in commonConditionalProb.items():
                conditionalProb[key] += val

            # smoothing:
            for label in self.legalLabels:
                for feat in self.features:
                    "*** YOUR CODE HERE to update conditionalProb and counts using Laplace smoothing ***"
                    conditionalProb[(feat, label)] = (conditionalProb[(feat, label)] + k) / (
                                counts[(feat, label)] + 2 * k)

            # normalizing:
            prior.normalize()
            self.prior = prior
            self.conditionalProb = conditionalProb
            self.k = k

            predictions = self.classify(validationData)
            accuracyCount = sum([pred == true for pred, true in zip(predictions, validationLabels)])

            print(
                "Performance on validation set for k=%f: (%.1f%%)" % (k, 100.0 * accuracyCount / len(validationLabels)))
            if accuracyCount > bestAccuracyCount:
                bestParams = (prior, conditionalProb, k)
                bestAccuracyCount = accuracyCount

        self.prior, self.conditionalProb, self.k = bestParams
        print("Best Performance on validation set for k=%f: (%.1f%%)" % (
        self.k, 100.0 * bestAccuracyCount / len(validationLabels)))

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.
        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = []
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()

        for label in self.legalLabels:
            "*** YOUR CODE HERE, to populate logJoint() list ***"
            logJoint[label] = math.log(self.prior[label])

            for feature, value in datum.items():
                if value > 0:
                    logJoint[label] += math.log(self.conditionalProb[(feature, label)])
                else:
                    logJoint[label] += math.log(1 - self.conditionalProb[(feature, label)])

        return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = []

        "*** YOUR CODE HERE, to populate featureOdds based on above formula. ***"
        for feature in self.features:
            p1 = self.conditionalProb.get((feature, label1), 1e-10)
            p2 = self.conditionalProb.get((feature, label2), 1e-10)
            ratio = p1 / p2
            featuresOdds.append((feature, ratio))

        featuresOdds.sort(key=lambda x: x[1], reverse=True)

        return [feature for feature, _ in featuresOdds[:100]]
