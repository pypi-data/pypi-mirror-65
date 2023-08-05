# Description  

Quantcore's implementation of a deep neural network. Used for classification and regression.

#Usage

The class takes a few requirements, # input nodes,  # hidden nodes, # layers, # output nodes, # learning rate, # number of epochs, # output type (specified with r for regression, c for classification), # train test split = 0.8 (percentage you would like to train on), # test = True (turn it off if you don't want to test), split = True (turn it off if you don't want the data split)

The train function takes one input, which is a DATAFRAME with the inputs and the outputs on the right side, e.g.
```
inputs = dataframe[:-1]
outputs = dataframe[-1]
```
Do not separate inputs from outputs, just have the outputs as the righter most column in your df

The call to train the function is class_.train(input)

The call to test is class_.feed_forward(input)

#Installation

```
pip install QCNN
```

#Sample Code
```

from QCNN import NeuralNetwork
import pandas as pd


nn= NeuralNetwork(2,2,3,1,.1,100000, train_test_split =1, split=False)

data_dict = {0:{'input1':0,'input2':0,'output':0},
            1:{'input1':1,'input2':0,'output':1},
            2:{'input1':0,'input2':1,'output':1},
            3:{'input1':1,'input2':1,'output':0}
            }

df = pd.DataFrame.from_dict(data_dict, orient = 'index')



nn.train(df)

```
