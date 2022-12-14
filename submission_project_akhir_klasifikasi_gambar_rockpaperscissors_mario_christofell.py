# -*- coding: utf-8 -*-
"""Submission Project Akhir Klasifikasi Gambar_RockPaperScissors_Mario Christofell.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/194CKTLpbYSKutGxk9VPxygTks5ktAFpD

# **Mario Christofell L.Tobing**

*   Project Akhir Dicoding Modul Belajar Machine Learning untuk Pemula Klasifikasi Gambar RockPaperScissors

# **List Library yang diimport untuk digunakan**
"""

# Import Library yang digunakan
import numpy as np
import zipfile
import os
import shutil
import splitfolders
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

"""# **Menimport/Mendownload Dataset RockPaperScissort dengan wget dari github**"""

# Mengimport/Download Dataset RockPaperScissors dengan wget
!wget https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip \-O /images/rockpaperscissors.zip

"""# **Ekstraksi File Zip RockPaperScissors dan Membuat Direktori Data Train dan Validation**"""

# Ekstrasi file zip rockpaperscissors dan Membuat direktori
dataset = 'rockpaperscissors.zip'
un_zip = zipfile.ZipFile(dataset, 'r')
un_zip.extractall('/images')
un_zip.close()

"""# **Split** **folder** **untuk** **data** **training** **dan** **validation** **dan** **membuat** **direktori** **masing** - **masing** **tiap** **jenis** **gambar**"""

local_dir = '/images/rockpaperscissors/rps-cv-images/' # direktori pertama
if ('dataset' in os.listdir(local_dir)):
  shutil.rmtree(os.path.join(local_dir, 'dataset'))

splitfolders.ratio('/images/rockpaperscissors/rps-cv-images/', output ='/images/rockpaperscissors/rps-cv-images/dataset',
                    seed=None, ratio=(.6,.4)) # pembagian untuk ukuran data training sebesar 60% dan validation 40%

# Direktori masing -masing jenis gambar rock, paper, scissors
rock = os.path.join('/images/rockpaperscissors/rps-cv-images/rock') # banyaknya jenis gambar rock
paper = os.path.join('/images/rockpaperscissors/rps-cv-images/paper') # banyaknya jenis gambar paper
scissors = os.path.join('/images/rockpaperscissors/rps-cv-images/scissors') # banyaknya jenis gambar scissors

# Direktori pada Data Training dari tiap jenis gambar (60%)
rock_train = os.path.join('/images/rockpaperscissors/rps-cv-images/dataset/train/rock') # banyaknya jenis gambar rock pada data training
paper_train = os.path.join('/images/rockpaperscissors/rps-cv-images/dataset/train/paper') # banyaknya jenis gambar paper pada data training
scissors_train = os.path.join('/images/rockpaperscissors/rps-cv-images/dataset/train/scissors') # banyaknya jenis gambar scissors pada data training

# Direktori pada Data Validation dari tiap jenis gambar (40%)
rock_val = os.path.join('/images/rockpaperscissors/rps-cv-images/dataset/val/rock') # banyaknya jenis gambar rock pada data validation
paper_val = os.path.join('/images/rockpaperscissors/rps-cv-images/dataset/val/paper') # banyaknya jenis gambar paper pada data validation 
scissors_val = os.path.join('/images/rockpaperscissors/rps-cv-images/dataset/val/scissors') # banyaknya jenis gambar scissors pada data validation

"""# **Hirarki** **bentuk** **data** **yang** **telah** **dibuat**"""

# Melihat hirarki bentuk dari isi foler "dataset" yang telah dibuat
!tree -d /images/rockpaperscissors/rps-cv-images/dataset

"""# **Melakukan augmentasi gambar dengan ImgaeDataGenerator**"""

train_dir = "/images/rockpaperscissors/rps-cv-images/dataset/train"
train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'nearest')

val_dir = "/images/rockpaperscissors/rps-cv-images/dataset/val"
val_datagen = ImageDataGenerator(
                    rescale=1./255)

train_generator = train_datagen.flow_from_directory(
	train_dir, # direktori data training
	target_size=(150,150), # ukuran reolusi gambar diubah menjadi 150x150 pixel
  batch_size=10,
	class_mode='categorical' # klasifikasi yang akan dilakukan adalah multi kelas maka menggunakan categorical
)

validation_generator = val_datagen.flow_from_directory(
	val_dir, # direktori data validasi
	target_size=(150,150), # ukuran reolusi gambar diubah menjadi 150x150 pixel
  batch_size=10,
	class_mode='categorical' # klasifikasi yang akan dilakukan adalah multi kelas maka menggunakan categorcial
)

"""# **Membentuk model Sequential**"""

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)), # konvulusi 1
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'), # konvulusi 2
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'), # konvulusi 3
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(512, (3,3), activation='relu'), # konvulusi 4
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax') # menggunakan fungsi aktivasi 'softmax' karena klasifikasi yang dilakukan merupakan multi kelas 
])

model.summary()

"""# **Optimizer dan Pelatihan Model**"""

model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, name="Adamax"),
              metrics=['accuracy'])

history = model.fit(
      train_generator,
      steps_per_epoch=20,
      epochs=20,
      validation_data=validation_generator,
      validation_steps=5,
      verbose=1)

"""# **Prediksi gambar dari dataset baru**"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

uploaded = files.upload()

for fn in uploaded.keys():

  path = fn 
  img = image.load_img(path, target_size =(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size=15)

  print('Hasil Prediksi : ',classes[0])

  print(fn)
  if classes[0,0]!=0:
    print('Jenis Gambar : Paper')
  elif classes[0,1]!=0:
    print('Jenis Gambar : Rock')
  else:
    print('Jenis Gambar : scissors')