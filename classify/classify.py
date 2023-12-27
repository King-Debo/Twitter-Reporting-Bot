# Import the scikit-learn and tensorflow libraries
import sklearn
import tensorflow as tf

# Load the features and labels from the CSV file
with open("features.csv", "r") as f:
    features = f.readlines()[1:] # Skip the header

# Create lists to store the features and labels
X = []
y = []

# Loop through each feature
for feature in features:
    # Extract the feature and label
    feature, label = feature.split(",") # The feature and label are separated by a comma
    feature = eval(feature) # Convert the feature from string to list
    label = int(label) # Convert the label from string to integer
    # Append the feature and label to the lists
    X.append(feature)
    y.append(label)

# Convert the features and labels to numpy arrays
X = np.array(X)
y = np.array(y)

# Choose a machine learning algorithm
# For this project, we will use a neural network, which is a powerful and flexible algorithm that can learn complex patterns and relationships from the data
# Define the neural network architecture
model = tf.keras.models.Sequential() # Create a sequential model
model.add(tf.keras.layers.Dense(64, activation="relu", input_shape=(X.shape[1],))) # Add a dense layer with 64 units and relu activation, and specify the input shape
model.add(tf.keras.layers.Dropout(0.2)) # Add a dropout layer with 0.2 rate to prevent overfitting
model.add(tf.keras.layers.Dense(32, activation="relu")) # Add another dense layer with 32 units and relu activation
model.add(tf.keras.layers.Dense(3, activation="softmax")) # Add the output layer with 3 units and softmax activation, corresponding to the 3 classes (fake, real, unknown)

# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]) # Use the adam optimizer, the sparse categorical crossentropy loss, and the accuracy metric

# Train the model
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2) # Fit the model on the training data, using 10 epochs, 32 batch size, and 20% validation split

# Save the model
model.save("model.h5") # Save the model as a HDF5 file named model.h5

# Predict the labels for the testing set
y_pred = model.predict(X_test) # Predict the probabilities for each class
y_pred = np.argmax(y_pred, axis=1) # Convert the probabilities to the class with the highest probability

# Save the predictions in a CSV file
with open("predictions.csv", "w") as f:
    f.write("predictions\n") # Write the header
    for pred in y_pred:
        # Write the prediction in the CSV file
        f.write(f"{pred}\n")
