# mlp.py
# -------------

# mlp implementation
import util
from random import random
from random import seed
import math
PRINT = True

class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations

  # Initialize a network
  def initialize_network(self,n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights': [random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights': [random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network

  # Calculate neuron activation for an input
  def activate(self,weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
      activation += weights[i] * inputs[i]
    return activation

  # Transfer neuron activation
  def transfer(self,activation):
    return 1.0 / (1.0 + math.exp(-activation))

  # Forward propagate input to a network output
  def forward_propagate(self,network, row):
    inputs = row
    for layer in network:
      new_inputs = []
      for neuron in layer:
        activation = self.activate(neuron['weights'], inputs)
        if abs(activation) > 100: activation=abs(activation)/activation*100
        neuron['output'] = self.transfer(activation)
        new_inputs.append(neuron['output'])
      inputs = new_inputs
    return inputs

  # Calculate the derivative of an neuron output
  def transfer_derivative(self,output):
    return output * (1.0 - output)

  # Backpropagate error and store in neurons
  def backward_propagate_error(self,network, expected):
    for i in reversed(range(len(network))):
      layer = network[i]
      errors = list()
      if i != len(network) - 1:
        for j in range(len(layer)):
          error = 0.0
          for neuron in network[i + 1]:
            error += (neuron['weights'][j] * neuron['delta'])
          errors.append(error)
      else:
        for j in range(len(layer)):
          neuron = layer[j]
          errors.append(expected[j] - neuron['output'])
      for j in range(len(layer)):
        neuron = layer[j]
        neuron['delta'] = errors[j] * self.transfer_derivative(neuron['output'])


      # Update network weights with error
  def update_weights(self,network, row, l_rate):
    for i in range(len(network)):
      inputs = row[:-1]
      if i != 0:
        inputs = [neuron['output'] for neuron in network[i - 1]]
      for neuron in network[i]:
        for j in range(len(inputs)):
          neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
        neuron['weights'][-1] += l_rate * neuron['delta']*10**6
        print neuron['weights'][-1]
  # Train a network for a fixed number of epochs
  def train_network(self,network, train, l_rate, n_outputs):
      sum_error = 0
      outputs = self.forward_propagate(network, train)
      expected = [0 for i in range(n_outputs)]
      expected[train[-1]] = 1
      sum_error += sum([(expected[i] - outputs[i]) ** 2 for i in range(len(expected))])
      self.backward_propagate_error(network, expected)
      self.update_weights(network, train, l_rate)
      print('lrate=%.3f, error=%.3f' % (l_rate, sum_error))



  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      n_inputs = len(trainingData[0])
      n_outputs = len(self.legalLabels)
      network = self.initialize_network(n_inputs, 28, n_outputs)
      for i in range(len(trainingData)):

        # Test training backprop algorithm
        seed(3)
        trainingCluster=list()
        trainingCluster.extend(trainingData[i].values())
        trueLabel = trainingLabels[i]
        trainingCluster.append(trueLabel)
        self.train_network(network, trainingCluster, 0.5, n_outputs)
        prediction = self.predict(network, trainingCluster)
        print('Expected=%d, Got=%d' % (trainingCluster[-1], prediction))

  # Make a prediction with a network
  def predict(self,network, row):
    outputs = self.forward_propagate(network, row)
    return outputs.index(max(outputs))

  def classify(self, data ):
    guesses = []
    for datum in data:
      # fill predictions in the guesses list
      "*** YOUR CODE HERE ***"
      util.raiseNotDefined()
    return guesses