# Import the scikit-learn and tensorflow libraries
import sklearn
import tensorflow as tf

# Load the model from the HDF5 file
model = tf.keras.models.load_model("model.h5") # Load the model as a keras model

# Load the predictions from the CSV file
with open("predictions.csv", "r") as f:
    predictions = f.readlines()[1:] # Skip the header

# Convert the predictions to numpy array
predictions = np.array(predictions)

# Evaluate the model on the testing set
score = model.evaluate(X_test, y_test) # Evaluate the model and get the score
print(f"Test loss: {score[0]}") # Print the test loss
print(f"Test accuracy: {score[1]}") # Print the test accuracy

# Calculate the precision, recall, and F1-score
precision = sklearn.metrics.precision_score(y_test, predictions, average="macro") # Calculate the precision using sklearn
recall = sklearn.metrics.recall_score(y_test, predictions, average="macro") # Calculate the recall using sklearn
f1_score = sklearn.metrics.f1_score(y_test, predictions, average="macro") # Calculate the F1-score using sklearn
print(f"Precision: {precision}") # Print the precision
print(f"Recall: {recall}") # Print the recall
print(f"F1-score: {f1_score}") # Print the F1-score

# Plot the ROC curve
fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_test, predictions, pos_label=1) # Calculate the false positive rate, true positive rate, and thresholds using sklearn
auc = sklearn.metrics.auc(fpr, tpr) # Calculate the area under the curve using sklearn
plt.plot(fpr, tpr, label=f"ROC curve (area = {auc})") # Plot the ROC curve using matplotlib
plt.plot([0, 1], [0, 1], linestyle="--", label="Random guess") # Plot the random guess line using matplotlib
plt.xlabel("False Positive Rate") # Set the x-axis label
plt.ylabel("True Positive Rate") # Set the y-axis label
plt.title("Receiver Operating Characteristic Curve") # Set the title
plt.legend() # Show the legend
plt.show() # Show the plot

# Optimize the model using cross-validation, grid search, and hyperparameter tuning
# Define the parameters to tune
parameters = {"optimizer": ["adam", "sgd"], # The optimizer
              "batch_size": [16, 32, 64], # The batch size
              "epochs": [10, 20, 30], # The number of epochs
              "dropout_rate": [0.1, 0.2, 0.3]} # The dropout rate

# Define the model builder function
def build_model(optimizer, dropout_rate):
    # Build the same neural network architecture as before
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(64, activation="relu", input_shape=(X.shape[1],)))
    model.add(tf.keras.layers.Dropout(dropout_rate))
    model.add(tf.keras.layers.Dense(32, activation="relu"))
    model.add(tf.keras.layers.Dense(3, activation="softmax"))
    # Compile the model with the given optimizer
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    # Return the model
    return model

# Wrap the model builder function in a keras classifier
model = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=build_model)

# Perform the grid search using sklearn
grid_search = sklearn.model_selection.GridSearchCV(model, parameters, cv=3, scoring="accuracy") # Define the grid search with 3-fold cross-validation and accuracy as the scoring metric
grid_search.fit(X, y) # Fit the grid search on the whole data
print(f"Best parameters: {grid_search.best_params_}") # Print the best parameters
print(f"Best score: {grid_search.best_score_}") # Print the best score
