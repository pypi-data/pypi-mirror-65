import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class NeuralNetwork:
    def __init__(self, inputnotes,hiddennodes,layers,outputnodes,learningrate,output_type):
        self.inodes = inputnotes
        self.hnodes = hiddennodes
        self.layers = layers
        self.onodes= outputnodes
        self.lr = learningrate
        self.individual_epoch_errors = []
        self.mean_errors = []
        self.original_epoch=0
        self.output_type = output_type


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

    def train(self,inputs,targets,epoch):




        outputs = self.feed_forward(inputs)
        targets = np.array(targets,ndmin=2).T


        output_errors = (targets-outputs)

        self.individual_epoch_errors.append(np.linalg.norm(output_errors))

        if self.original_epoch != epoch:
            #print(np.mean(self.individual_epoch_errors))
            self.mean_errors.append(1-np.mean(self.individual_epoch_errors*1))
            self.individual_epoch_errors = []
            self.original_epoch +=1

            #plt.plot(self.mean_errors)






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
                if np.linalg.norm(gradient)>10:
                    gradient = 10*(gradient/np.linalg.norm(gradient))
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
                if np.linalg.norm(gradient)>10:
                    gradient = 10*(gradient/np.linalg.norm(gradient))
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
                if np.linalg.norm(gradient)>10:
                    gradient = 10*(gradient/np.linalg.norm(gradient))
                first_errors = gradient

                gradient = self.lr*gradient
                prev_hidden_t = self.ff['a'+str(layer-1)].T

                deltas = gradient@prev_hidden_t
                self.iw[layer]+= deltas
                self.iw['bias'+str(layer)] += gradient
