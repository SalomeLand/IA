import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

model = Sequential([
    Flatten(input_shape=(28, 28)),         # Aplanar imágenes 28x28
    Dense(128, activation='relu'),         # Capa oculta con 128 neuronas y ReLU
    Dense(10, activation='softmax')       
])


model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

loss, accuracy = model.evaluate(x_test, y_test)
print(f"Precisión en test: {accuracy:.2f}")
