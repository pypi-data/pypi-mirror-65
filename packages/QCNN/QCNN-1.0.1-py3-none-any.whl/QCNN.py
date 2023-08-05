import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




class NeuralNetwork:
    def __init__(self, inputnotes,hiddennodes,layers,outputnodes,learningrate,number_of_epochs=1000,output_type = 'c',train_test_split = 0.8,test = True, split = True):
        """
        inputnodes
        hiddennodes
        layers
        outputnodes
        learningrate
        number_of_epochs=1000
        output_type = 'c' (choice between c for classification and r for regression)
        train_test_split = 0.8 (percentage you would like to train)
        test = True (turn if off if you don't want to test)
        split = True (split the data)

        """
        self.inodes = inputnotes
        self.hnodes = hiddennodes
        self.layers = layers
        self.onodes= outputnodes
        self.lr = learningrate
        self.epochs = number_of_epochs
        self.individual_epoch_errors = []
        self.mean_errors = []
        self.original_epoch=0
        self.output_type = output_type
        self.tts = train_test_split
        self.test = test
        self.split = split


        """Initialize the weights and the biases"""

        self.iw = {} #The initial Weights dictionary

        for layer in range(self.layers):
            if layer == 0:
                self.iw[layer] = (np.random.rand(self.hnodes,self.inodes)-.5)
                self.iw['bias' +str(layer)] = np.random.rand(self.hnodes)
                self.iw['bias' + str(layer)] = np.array(self.iw['bias' +str(layer)],ndmin = 2).T
            elif layer == self.layers-1:
                self.iw[layer] = (np.random.rand(self.onodes,self.hnodes)-.5)
                self.iw['bias' +str(layer)] = np.random.rand(self.onodes)
                self.iw['bias' + str(layer)] = np.array(self.iw['bias' +str(layer)],ndmin = 2).T
            else:
                self.iw[layer] = (np.random.rand(self.hnodes, self.hnodes)-.5)
                self.iw['bias'+str(layer)] = np.random.rand(self.hnodes)
                self.iw['bias' + str(layer)] = np.array(self.iw['bias'+str(layer)],ndmin = 2).T

    def sigmoid(self,x):
        return (1/(1+np.e**(-x)))
    def dsigmoid(self,x):
        return (self.sigmoid(x)*(1-self.sigmoid(x)))

    def relu(self,x):

        return np.maximum(x,x*.0001)
    def drelu(self,x):
        positive =  1.*(x>0)
        negative = .0001*(x<0)

        return positive+negative

    # def sigmoid(self,x):
    #     overall_array = []
    #
    #     for row in x:
    #         new_array = []
    #         for value in row:
    #             if value >0:
    #                 new_array.append(value)
    #             else:
    #                 new_array.append(0)
    #         overall_array.append(new_array)
    #     return np.array(overall_array,ndmin=2)
    # def dsigmoid(self,x):
    #     overall_array = []
    #     for row in x:
    #         new_array = []
    #         for value in row:
    #             if value >0:
    #                 new_array.append(1)
    #             else:
    #                 new_array.append(0)
    #         overall_array.append(new_array)
    #     return np.array(overall_array,ndmin=1)





    def feed_forward(self,input_array):
        input_array = np.array(input_array,ndmin=2).T
        self.input_array = input_array





        """Run feedword algorithm"""

        self.ff = {} #Dictionary to hold the feedforward weights

        for layer in range(self.layers):
            if layer ==0:
                self.ff['z'+str(layer)] = self.iw[layer]@input_array
                self.ff['z'+str(layer)]+= self.iw['bias'+str(layer)]
                self.ff['a'+str(layer)] = self.sigmoid(self.ff['z'+str(layer)])

            elif layer == self.layers -1:
                self.ff['z'+str(layer)] = self.iw[layer]@self.ff['a'+str(layer-1)]
                self.ff['z'+str(layer)]+= self.iw['bias'+str(layer)]
                if self.output_type.lower().startswith('c'):
                    self.ff['a'+str(layer)] = self.sigmoid(self.ff['z'+str(layer)])
                elif self.output_type.lower().startswith('r'):
                    self.ff['a'+str(layer)] = self.ff['z'+str(layer)]

            else:
                self.ff['z'+str(layer)] = self.iw[layer]@self.ff['a'+str(layer-1)]
                self.ff['z'+str(layer)]+= self.iw['bias'+str(layer)]
                self.ff['a'+str(layer)] = self.sigmoid(self.ff['z'+str(layer)])

        outputs = self.ff['a'+str(self.layers-1)]

        return outputs

    def clean_data(func):
        def wrapper(*args, **kwargs):
            test_outcomes = []
            test_answers = []

            self = args[0]
            data = args[1]

            train_data = data.iloc[:int(len(data)*(self.tts))].sample(frac=1)
            print(train_data)
            test_data = data.iloc[int(len(data)*self.tts):]

            if not self.split:
                test_data = data.iloc[:int(len(data)*self.tts)]


            train_inputs = train_data[data.columns[:-1]].values
            train_outputs = train_data[data.columns[-1]].values

            test_inputs = test_data[data.columns[:-1]].values
            test_outputs = test_data[data.columns[-1]].values



            for epoch in range(self.epochs):
                for i in range(len(train_inputs)):
                    func(args[0],train_inputs[i],train_outputs[i],epoch)
            plt.plot(self.mean_errors)
            plt.show()
            if not self.test:
                return
            else:
                for index,point in enumerate(test_inputs):
                    print(point)
                    print(self.feed_forward(point))
                    test_outcomes.append(self.feed_forward(point)[0])
                    test_answers.append(test_outputs[index])
                plt.plot(test_outcomes,'*', label = 'test')
                plt.plot(test_answers,'*',label = 'answer')
                plt.legend()
                plt.show()
                return

        return wrapper

    @clean_data
    def train(self,inputs,targets="None",epoch = 0):

        outputs = self.feed_forward(inputs)
        targets = np.array(targets,ndmin=2).T
        output_errors = (targets-outputs)
        self.individual_epoch_errors.append(np.linalg.norm(output_errors))

        if self.original_epoch != epoch:

            self.mean_errors.append(1-np.mean(self.individual_epoch_errors*1))
            self.individual_epoch_errors = []
            self.original_epoch +=1


        for layer in range(self.layers-1,-1,-1):

            if layer == self.layers -1:
                #δL=(aL−y)⊙σ′(zL).
                """Check to see what the output type is"""
                if self.output_type.lower().startswith('c'):
                    """Classification output, using sigmoid run it through the dsigmoid"""

                    gradient = self.dsigmoid(self.ff['z'+str(self.layers-1)])
                elif self.output_type.lower().startswith('r'):
                    """regression. The function is linear, therefore has derivative of 1 everywhere"""

                    gradient = np.ones(np.shape(self.ff['z'+str(self.layers-1)]))

                gradient = np.multiply(output_errors,gradient)
                # if np.linalg.norm(gradient)>10:
                #     gradient = 10*(gradient/np.linalg.norm(gradient))
                first_errors = gradient
                gradient = self.lr*gradient



                hidden_t = self.ff['a'+str(layer-1)].T
                deltas = gradient@hidden_t

                self.iw[layer] += deltas
                self.iw['bias' + str(layer)]+= gradient

            elif layer ==0:
                #δl=((wl+1)Tδl+1)⊙σ′(zl),
                first_errors = np.transpose(self.iw[layer+1])@first_errors
                gradient = self.dsigmoid(self.ff['z'+str(layer)])
                gradient = np.multiply(first_errors,gradient)
                # if np.linalg.norm(gradient)>10:
                #     gradient = 10*(gradient/np.linalg.norm(gradient))
                first_errors = gradient
                gradient = self.lr*gradient


                inputs_t = self.input_array.T

                deltas = gradient@inputs_t

                self.iw[layer]+=deltas

                self.iw['bias'+str(layer)]+= gradient
            else:
                #δl=((wl+1)Tδl+1)⊙σ′(zl),
                first_errors = np.transpose(self.iw[layer+1])@first_errors

                gradient = self.dsigmoid(self.ff['z'+str(layer)])

                gradient = np.multiply(first_errors,gradient)
                # if np.linalg.norm(gradient)>10:
                #     gradient = 10*(gradient/np.linalg.norm(gradient))
                first_errors = gradient

                gradient = self.lr*gradient
                prev_hidden_t = self.ff['a'+str(layer-1)].T

                deltas = gradient@prev_hidden_t
                self.iw[layer]+= deltas
                self.iw['bias'+str(layer)] += gradient
