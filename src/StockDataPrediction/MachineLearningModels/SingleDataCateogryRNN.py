import numpy as np
import math
import random

'''
Created on Jun 7, 2018

@author: Colton Freitas
'''

class RNNNormal:
        
        def __init__ (self, hiddenStateSize, inputSize, numInputsPerStep, dataNormalizationFunction, dataDenormalizationFunction, backPropTruncateAmount=4, learning_rate = 0.01):
            ''' Initializes the RNN
            :param hiddenStateSize: Size of the hidden state, which will be [hiddenStateSize, hiddenStateSize]
                Larger can be more accurate, but will be more complex
            :param inputSize: Number of discrete unique inputs
                So for [-5 ... 5], inputSize = 11
            :param numInputsPerStep: Number of inputs per training step
            :param dataNormalizationFunction: Function to normalize the data into the range 0-inputSize
            :param dataDenormalizationFunction: Function to transform the data from the range 0-inputSize into the original data mapping
                Both denormalization and normalization functions have the same argument list, defined in :argumentList:
            :param backPropTruncateAmount: Number of training steps to back propogate through before stopping during backpropogation
            :param learningRate: Learning Rate for the ML Model

            :argumentList:
                (x)
                :param x: Data point to normalize/denormalize
            '''
            self.hiddenStateSize = hiddenStateSize
            self.inputSize = inputSize
            self.backPropTruncateAmount = backPropTruncateAmount
            self.numInputsPerStep = numInputsPerStep
            self.normFunc = dataNormalizationFunction
            self.deNormFunc = dataDenormalizationFunction
            
            self.inputWeights = np.random.uniform( -(1/math.sqrt(20)), (1/math.sqrt(20)), (numInputsPerStep, inputSize) )
            self.U = np.random.uniform( -(1/math.sqrt(inputSize)), (1/math.sqrt(inputSize)), (inputSize, hiddenStateSize))
            self.V = np.random.uniform( -(1/math.sqrt(hiddenStateSize)), (1/math.sqrt(hiddenStateSize)), (inputSize, hiddenStateSize))
            self.W = np.random.uniform( -(1 / math.sqrt(hiddenStateSize)), (1 / math.sqrt(hiddenStateSize)), (hiddenStateSize, hiddenStateSize));
            self.learning_rate = learning_rate
            self.losses = []
            
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

                    transformed_x[i][self.normFunc(x[time_step][i])] = 1
                
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
        
        def predict (self, x):
            '''Makes a prediction based off of the given training example
            :param x: Data to make prediction from
            :type x: List of Num
            '''
            o,s,a = self.forward_prop(x)
            return self.deNormFunc(np.argmax(o, axis=1)[0])
            
        def __backPropogation (self, x, y):
            '''Performs forward and truncated backpropogation on the RNN
            :param x: Training example to use
            :type x: List of Num
            :param y: Target examples to use
            :type y: List of Num

            TODO: Clean function by splitting into sub functions
            '''
            y = [self.normFunc(v) for v in y]
            time_steps = len(y)
            o,s,a = self.forward_prop(x);
            dLdU = np.zeros(self.U.shape)
            dLdV = np.zeros(self.V.shape)
            dLdW = np.zeros(self.W.shape)
            dLdWeights = np.zeros(self.inputWeights.shape)
            
            # (predicted - actual) for partial of cross entropy and softmax
            o[np.arange(len(y)), y] -= 1 
            delta_o = o #Alias for clarity

            #transform the inputs for all steps for use in calculations
            transformed_x = np.zeros((len(x), self.numInputsPerStep, self.inputSize))
            for t in np.arange(time_steps)[::-1]:
                for i in range(len(x[t])):
                    transformed_x[t][i][x[t][i]] = 1
    
            
            
            
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
            self.V -= dLdV * self.learning_rate
            self.W -= dLdW * self.learning_rate
            self.U -= dLdU * self.learning_rate
            self.inputWeights -= dLdWeights * self.learning_rate
            
            return [dLdV, dLdW, dLdU, dLdWeights]
        
        def train(self, x, y, verbose=False, batch_gradient_descent = False, batch_gradient_size = 100, eval_loss_after = 5, train_until_convergence = True, num_epochs = 20):
            
            bgd = True if batch_gradient_descent else False; 
                #This takes care of the case when batch_gradient_descent is neither True nor False (aka 5, None, etc.)
            verbose = True if verbose else False
                
            if (train_until_convergence):
                if (bgd):
                    self.__complete_training(self.__batch_step, x, y, verbose, eval_loss_after, (batch_gradient_size))
                else:
                    self.__complete_training(self.__full_step, x, y, verbose, eval_loss_after, ())
            else:
                if (bgd):
                    self.__epoch_training(self.__batch_step, x, y, verbose, eval_loss_after, num_epochs, (batch_gradient_size))
                else:
                    self.__epoch_training(self.__full_step, x, y, verbose, eval_loss_after, num_epochs, ())
            
        def __batch_step(self, x, y, batch_size):
            batch_indices = []
            batch_indices.extend(range(len(y)))
            random.shuffle(batch_indices)
            batch_indices = batch_indices[:batch_size]
            
            for index in batch_indices:
                self.__backPropogation(x[index], y[index])
                
        def __full_step(self, x, y):
            for index in range(len(y)):
                self.__backPropogation(x[index], y[index])
                
        def __complete_training(self, step_method, x, y, verbose, eval_loss_after, step_args):
            epochs = 0
            while not ( len(self.losses) > 1 and (self.losses[-1] == self.losses[-2]) ):
                step_method(x, y, step_args)
                epochs += 1
                if (epochs % eval_loss_after == 0):
                    self.losses.extend([self.__calculate_total_loss(x, y)])
                    if (len(self.losses) > 1):
                        if (self.losses[-1] > self.losses[-2]):
                            self.learning_rate *= .5
                            if (verbose):
                                print("Adjusting learning rate to %f" % (self.learning_rate))
                                print("Current Learning Rate:", self.learning_rate)
                    if (verbose):
                        print("Loss after %d epochs: %f" % (epochs, self.losses[-1]))    
        
        def __epoch_training(self, step_method, x, y, verbose, eval_loss_after, epochs, step_args):
            curr_epoch = 0
            while not (epochs == curr_epoch):
                step_method(x, y, step_args)
                curr_epoch += 1
                if (curr_epoch % eval_loss_after == 0):
                    self.losses.extend([self.__calculate_total_loss(x, y)])
                    if (len(self.losses) > 1):
                        if (self.losses[-1] > self.losses[-2]):
                            self.learning_rate *= .5
                            if (verbose):
                                print("Adjusting learning rate to %f" % (self.learning_rate))
                                print("Current Learning Rate:", self.learning_rate)
                    if (verbose):
                        print("Loss after %d epochs: %f" % (curr_epoch, self.losses[-1]))
            
        def store(self, filePath):
            open_file = open(filePath, "w")
            open_file.write("%f\n" % (self.learning_rate))
            open_file.write("%d\n" % (self.hiddenStateSize))
            open_file.write("%d\n" % (self.inputSize))
            open_file.write("%d\n" % (self.numInputsPerStep))
            
            self.__storeMatrix(self.U, open_file)
            self.__storeMatrix(self.W, open_file)
            self.__storeMatrix(self.V, open_file)
                                    
            self.__storeMatrix(self.inputWeights, open_file)
            
            open_file.close()
        
        def load(self, filePath):
            open_file = open(filePath, "r")

            self.learning_rate = float( open_file.readline() )
            self.hiddenStateSize = int( open_file.readline() )
            self.inputSize = int( open_file.readline() )
            self.numInputsPerStep = int( open_file.readline() )
            
            self.U = (self.__loadMatrix(open_file))
            self.W = (self.__loadMatrix(open_file))
            self.V = (self.__loadMatrix(open_file))
            self.inputWeights = (self.__loadMatrix(open_file))
            
            open_file.close()
        
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
        
        def __loadMatrix(self, file_handle):
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
def softmax(x):
    x = np.exp(x)
    divisor = np.sum((x))
    x /= divisor
    return x
            