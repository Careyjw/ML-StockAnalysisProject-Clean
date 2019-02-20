'''
    :author: Colton Freitas
    :as-of: February 7th, 2019
'''

from AI.AbsAIModel import Abs_AIModel
from Data.ModelDataProcessing.SCDataGeneration import translateDataRetrievalMethod
from Data.Structures.ClusteredStockStorage import ClusteredStockStorage


import numpy as np
import math
import random
from typing import List

def softmax(x):
    x = np.exp(x)
    divisor = np.sum((x))
    x /= divisor
    return x

def registerModel(cls):
    Abs_AIModel.registerModel("SC", cls)

#The annotation below actually calls the method registerModel at the time that the
#class is being first created
#Called once per thread
@registerModel
class SingleDataCategoryRNN (Abs_AIModel):

    def __parseConfiguration(self, modelConfiguration):
        self.modelID = modelConfiguration['General']['sModelID']
        self.hiddenStateSize = int(modelConfiguration[self.modelID]['iHiddenStateSize'])
        self.inputSize = int(modelConfiguration[self.modelID]['iInputSize'])
        self.backPropTruncateAmount = int(modelConfiguration[self.modelID]['iBackpropagationTruncationAmount'])
        #Clustered stocks don't include the primary ticker, so add one to account
        self.numInputsPerStep = len(modelConfiguration['General']['lsClusteredStocks']) + 1
        self.evalLossAfter = int(modelConfiguration[self.modelID]['iLossEvalEpochs'])
        self.numEpochs = int(modelConfiguration[self.modelID]['iNumEpochs'])
        self.learningRate = float(modelConfiguration[self.modelID]['fLearningRate'])
    
    def __init__ (self, modelConfiguration):
        ''' Initializes the RNN
        :param hiddenStateSize: Size of the hidden state, which will be [hiddenStateSize, hiddenStateSize]
            Larger can be more accurate, but will be more complex
        :param inputSize: Number of discrete unique inputs
            So for [-5 ... 5], inputSize = 11
        :param numInputsPerStep: Number of inputs per training step
        :param backPropTruncateAmount: Number of training steps to back propogate through before stopping during backpropogation
        :param learningRate: Learning Rate for the ML Model
        '''
        self.__parseConfiguration(modelConfiguration)
        self.inputWeights = np.random.uniform( -(1/math.sqrt(20)), (1/math.sqrt(20)), (self.numInputsPerStep, self.inputSize) )
        self.U = np.random.uniform( -(1/math.sqrt(self.inputSize)), (1/math.sqrt(self.inputSize)), (self.inputSize, self.hiddenStateSize))
        self.V = np.random.uniform( -(1/math.sqrt(self.hiddenStateSize)), (1/math.sqrt(self.hiddenStateSize)), (self.inputSize, self.hiddenStateSize))
        self.W = np.random.uniform( -(1 / math.sqrt(self.hiddenStateSize)), (1 / math.sqrt(self.hiddenStateSize)), (self.hiddenStateSize, self.hiddenStateSize))
        self.losses = []


    def Save(self, fileHandle):        
        self.__storeMatrix(self.U, fileHandle)
        self.__storeMatrix(self.W, fileHandle)
        self.__storeMatrix(self.V, fileHandle)
                                
        self.__storeMatrix(self.inputWeights, fileHandle)

    @classmethod
    def Load(cls, fileHandle, modelConfiguration):
        rnn = cls(modelConfiguration)

        U = (cls.__loadMatrix(fileHandle))
        W = (cls.__loadMatrix(fileHandle))
        V = (cls.__loadMatrix(fileHandle))
        inputWeights = (cls.__loadMatrix(fileHandle))
        
        rnn.U = U
        rnn.W = W
        rnn.V = V
        rnn.inputWeights = inputWeights
        
        return rnn    

    def __getData(self, modelConfiguration):
        dataRetrievalMethod, argHelper = translateDataRetrievalMethod(self.modelID)
        argHelper.fillFromModelConfiguration(modelConfiguration)
        return dataRetrievalMethod(argHelper)
    
    def Train(self, modelConfiguration):
        dataStorage = self.__getData(modelConfiguration)
        self.trainEpoch_BatchGradientDescent(dataStorage, self.numEpochs)

    def Evaluate(self, modelConfiguration):
        '''Evaluates the model using the stock list provided in modelConfiguration
        Returns a percentage accuracy (float)'''
        raise NotImplementedError

    def Predict (self, clusteredStocks : 'ClusteredStockStorage'):
        '''Makes a prediction using the most recent data stored in the database
        :return: Denormalized prediction
        '''
        raise NotImplementedError

    def forward_prop (self, x):
        '''

        :format x:
            len(x) = number of days to predict from
            len(x[0]) = numInputsPerStep
        '''
        #assuming x is in unexpanded form (aka x is in form [0, 2, 1, 3, 1, ...] where each number corresponds to a unique input state
        #this unexpanded form will then be transformed into a one-hot vector where the number is the index of the hot data point
        
        s = np.zeros((len(x) + 1, self.hiddenStateSize))
        o = np.zeros((len(x), self.inputSize))
        a = np.zeros((len(x), self.inputSize))
        
        for time_step in np.arange(len(x)):
            
            #setup transformation for unexpanded x vector into a series of one-hot vectors
            transformed_x = np.zeros((self.numInputsPerStep, self.inputSize))
            for i in range(len(x[time_step])):
                transformed_x[i][x[time_step][i]] = 1
            
            #Average the inputs
            weighted_inputs = np.multiply(transformed_x, self.inputWeights);
            average_input = np.sum(weighted_inputs, axis=0) / self.numInputsPerStep
            a[time_step] = average_input
            
            #Calculate the hidden state
            current_z = ( (average_input.dot(self.U)) + (self.W.dot(s[time_step-1])) )
            s[time_step] = np.tanh(current_z)
            
            #Calculate output
            toSoftmax = self.V.dot(s[time_step])
            o[time_step] = softmax(toSoftmax)
            
        return [o, s, a]
    
    def __calculate_total_loss(self, x, y):
        '''Calculates the loss value for training evaluation
        :param x: Training values
        :type x: List of List of Num
        :param y: Target values
        :type y: List of Num
        '''
        num_training_examples = np.sum((len(y_i) for y_i in y))
        
        return self.__calculate_loss(x, y) / num_training_examples
    
    def __calculate_loss (self, x, y):
        '''Calculates the loss value for training evaluation
        :param x: Current Training Example
        :type x: List of Num
        :param y: Current Target Value
        :type y: Num
        '''
        L = 0
        
        for i in np.arange(len(y)):
            o,s,a = self.forward_prop(x[i])
            
            correct_word_predictions = o[np.arange(len(y[i])), y[i]]
            
            L += -1 * np.sum(np.log(correct_word_predictions))
        return L

    def __backPropogation (self, x, y):
        '''Performs forward and truncated backpropogation on the RNN
        :param x: Training example to use
        :type x: List of Num
        :param y: Target examples to use
        :type y: List of Num

        TODO: Clean function by splitting into sub functions
        '''
        
        time_steps = len(y)
        o,s,a = self.forward_prop(x)
        dLdU = np.zeros(self.U.shape)
        dLdV = np.zeros(self.V.shape)
        dLdW = np.zeros(self.W.shape)
        dLdWeights = np.zeros(self.inputWeights.shape)
        
        #for each time step in the output,
        #does the equivalent of subtracting the correct one-hot vector
        #from the prediction to calculate the partial derivative for
        #the cross entropy and softmax functions
        o[np.arange(len(y)), y] -= 1 
        delta_o = o #Alias for clarity

        #transform the inputs for all steps for use in calculations
        #aka encode all x values into one-hot vectors
        transformed_x = np.zeros((len(x), self.numInputsPerStep, self.inputSize))
        for t in np.arange(time_steps)[::-1]:
            for i in range(len(x[t])):
                transformed_x[t][i][x[t][i]] = 1
        
        #np.arange(time_steps)[::-1] is a range from time_steps to 0
        for t in np.arange(time_steps)[::-1]:
            #Partial previously calculated multiplied by s[t]
            dLdV += np.outer(delta_o[t], s[t])
            current_partial_base = self.V.T.dot(delta_o[t].T)
            current_partial_base = current_partial_base.T * (1 - s[t] ** 2)
            for (back_prop_step) in np.arange(max(0, t-self.backPropTruncateAmount), t+1)[::-1]:
                dLdW += np.outer(s[back_prop_step-1], current_partial_base)
                
                dLdU += np.outer(a[back_prop_step], current_partial_base)
                
                current_transformed_x = transformed_x[back_prop_step] / 3;
                                    
                partial_temp_storage = self.U.dot(current_partial_base)
                
                for i in range(len(x[back_prop_step])):
                    dLdWeights[i] += partial_temp_storage * current_transformed_x[i]

                current_partial_base = self.W.T.dot(current_partial_base) *  (1 - s[back_prop_step] ** 2)
        self.V -= dLdV * self.learningRate
        self.W -= dLdW * self.learningRate
        self.U -= dLdU * self.learningRate
        self.inputWeights -= dLdWeights * self.learningRate
        
        return [dLdV, dLdW, dLdU, dLdWeights]
    
    def trainEpoch_BatchGradientDescent(self, trainingStorage : "RNNTrainingDataStorage", numEpochs : int = 20, verbose : bool = False, batchGradientSize : int = 100):
        x, y = trainingStorage.extractData()
        epochs = 0
        while not epochs == numEpochs:
            self.__batch_step(x, y, batchGradientSize)
            epochs += 1
            if (epochs % self.evalLossAfter == 0):
                self.losses.append(self.__calculate_total_loss(x, y))
                if (len(self.losses) > 1):
                    if (self.losses[-1] > self.losses[-2]):
                        self.learningRate *= .5
                        if(verbose):
                            print("Adjusting learning rate to {0}".format(self.learningRate))
                            
                if (verbose):
                    print("Loss after {0} epochs: {1}".format(epochs, self.losses[-1]))
        
    def __batch_step(self, x, y, batch_size):
        batch_indices = []
        batch_indices.extend(range(len(y)))
        random.shuffle(batch_indices)
        batch_indices = batch_indices[:batch_size]
        
        for index in batch_indices:
            self.__backPropogation(x[index], y[index])
    
    def __storeMatrix(self, mat, file_handle):
        '''Stores the matrix specified by mat in the file specified by file_handle
        :param mat: Rectangular, two dimensional numpy matrix
        :param file_handle: open file handle to the file to write the matrix to
        Designed to be used with __loadMatrix to handle model I/O
        '''
        #assumes matrix is 2 dimensional and is rectangular
        file_handle.write("%d %d\n" % (len(mat), len(mat[0])))
        for row in mat:
            
            format_string = ""
            for col in row:
                format_string += "%f "
            format_string = format_string[:len(format_string)-1]
            format_string += "\n"
            file_handle.write(format_string % tuple([x for x in row]))
    
    @classmethod
    def __loadMatrix(cls, file_handle):
        '''Loads a matrix from the file specified by file_handle and returns it
        :param file_handle: open file handle to read the matrix from
        :return: Numpy matrix containing the rectangular, two dimensional matrix read from file_handle
        Designed to be used with __storeMatrix to handle model I/O            
        '''
        
        rows, cols = file_handle.readline().split(" ")
        ret = np.zeros( (int(rows), int(cols)) )
        for row in range(int(rows)):
            currRow = file_handle.readline().split(" ")
            currRow = [float(x) for x in currRow]
            ret[row] = currRow
        return ret