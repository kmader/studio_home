import sys

try:
    from keras.layers.core import Dense
    from keras.layers import Input
    from keras.models import Model
    import numpy as np


    def get_model():
        Input_1 = Input(shape=(1,), name='Input_1')
        Dense_1 = Dense(name='Dense_1',output_dim= 1,activation= 'sigmoid' )(Input_1)
        model = Model([Input_1],[Dense_1])
        return model
    
    model = get_model()
    print ("Checking GPU support...", end='')
    model.compile(loss='binary_crossentropy', optimizer='Adadelta', context=["gpu(0)"])
    X=np.random.randint(2, size=10)
    Y=np.random.randint(2, size=10)
    model.train_on_batch(X,Y)
    print ("GPU supported")
    sys.exit(0)
except Exception as e:
    print ("Not supported")
    print (str(e))
    sys.exit(-1)

