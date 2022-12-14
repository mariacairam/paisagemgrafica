#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cv2
from PIL import Image


# In[4]:


img = image.load_img('basedata/train/pessoas/4-4-4-4_14276556097_o.jpg')
plt.imshow(img)
cv2.imread('basedata/train/pessoas/4-4-4-4_14276556097_o.jpg')
print(img.size)


# In[51]:


validation = ImageDataGenerator(rescale=1/225)
generator = ImageDataGenerator(rescale = 1/255,
                               rotation_range = 7,
                               horizontal_flip = True,
                               shear_range = 0.2,
                               height_shift_range = 0.07,
                               zoom_range = 0.2)


# In[52]:


## fazendo dataset de treinamento e validação, batch será a leitura de grupos de dataset

train_dataset = generator.flow_from_directory('basedata/train/', target_size=(200, 200), 
                                               batch_size=32, class_mode='categorical')
validation_dataset = validation.flow_from_directory('basedata/validation/', target_size=(200, 200), 
                                               batch_size=32, class_mode='categorical')

train_dataset.class_indices


# In[53]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
# Creating a Sequential Model and adding the layers
model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), input_shape=(200,200, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, kernel_size=(3,3), input_shape=(200,200, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation= 'relu'))
model.add(Dropout(0.2))
model.add(Dense(5,activation= 'sigmoid'))


# In[57]:


model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(16, (3,3), activation = 'relu', input_shape=(200,200, 3)), 
                                    ## operador
                                    ## feature detector
                                    ## detectar as características da imagem a partir de uma multiplicação de matrizes (imagemXkernel)
                                    ## mapa de características
                                    ## função relu = valores negativos -> 0
                                  tf.keras.layers.MaxPool2D(2,2),
                                    ## enfatizar as características principais
                                  tf.keras.layers.Conv2D(32, (3,3), activation = 'relu'), 
                                  tf.keras.layers.MaxPool2D(2,2),
                                  tf.keras.layers.Conv2D(64, (3,3), activation = 'relu'), 
                                  tf.keras.layers.MaxPool2D(2,2), 
                                  tf.keras.layers.Flatten(),
                                    ## transformar a matriz em um vetor para fazer na rede neural densa
                                  tf.keras.layers.Dense(512, activation = 'relu'),
                                  tf.keras.layers.Dense(4, activation = 'sigmoid')
                                    ## função de ativação utilizada, lembrando q a função de ativação dita a resposta
                                  ])


# In[58]:


model.compile(optimizer=RMSprop(learning_rate=0.001), 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])
model_fit = model.fit(train_dataset, epochs=100, validation_data=validation_dataset)


# In[61]:


current = os.getcwd()
print(current)

try:
    os.mkdir(os.path.join(current, 'fotos insta'))
except FileExistsError:
    pass
    

photos = current + '/' + 'fotos insta'
print(photos)

arquivos = os.listdir(photos)

for i in arquivos:
    print(i)
    im = image.load_img(photos+'/'+i, target_size=(200,200))
    
    plt.imshow(im)
    plt.show()
    x = image.img_to_array(im)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    val = model.predict(images)
    print(val)

