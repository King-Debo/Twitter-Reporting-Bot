# Import the scikit-learn and tensorflow libraries
import sklearn
import tensorflow as tf

# Load the preprocessed data and labels from the CSV file
with open("preprocessed_data.csv", "r") as f:
    preprocessed_data = f.readlines()[1:] # Skip the header

# Create lists to store the features and labels
features = []
labels = []

# Loop through each preprocessed data
for data in preprocessed_data:
    # Extract the tokens and label
    tokens, label = data.split(",") # The tokens and label are separated by a comma
    tokens = eval(tokens) # Convert the tokens from string to list
    label = label.strip() # Remove the newline character
    # Append the tokens and label to the lists
    features.append(tokens)
    labels.append(label)

# Convert the labels to numerical values
label_dict = {"Fake": 0, "Real": 1, "Unknown": 2} # Define a dictionary to map the labels to numbers
labels = [label_dict[label] for label in labels] # Convert the labels using the dictionary

# Convert the features and labels to numpy arrays
features = np.array(features)
labels = np.array(labels)

# Split the features and labels into training and testing sets
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(features, labels, test_size=0.2, random_state=42) # Use 80% of the data for training and 20% for testing

# Define the feature extraction function
def feature_extraction(tokens):
    # Initialize an empty list to store the features
    features = []
    # Extract the word embeddings using tensorflow
    embeddings = tf.keras.layers.Embedding(input_dim=10000, output_dim=16, mask_zero=True) # Define an embedding layer with input dimension of 10000, output dimension of 16, and masking of zero values
    embeddings = embeddings(tokens) # Apply the embedding layer to the tokens
    embeddings = tf.reduce_mean(embeddings, axis=1) # Reduce the embeddings to a mean vector
    # Extract the bag-of-words using sklearn
    bow = sklearn.feature_extraction.text.CountVectorizer(max_features=1000) # Define a count vectorizer with maximum features of 1000
    bow = bow.fit_transform(tokens) # Fit and transform the tokens to a sparse matrix
    bow = bow.toarray() # Convert the sparse matrix to a dense array
    # Extract the TF-IDF using sklearn
    tfidf = sklearn.feature_extraction.text.TfidfVectorizer(max_features=1000) # Define a TF-IDF vectorizer with maximum features of 1000
    tfidf = tfidf.fit_transform(tokens) # Fit and transform the tokens to a sparse matrix
    tfidf = tfidf.toarray() # Convert the sparse matrix to a dense array
    # Extract the n-grams using sklearn
    ngrams = sklearn.feature_extraction.text.CountVectorizer(ngram_range=(2,3), max_features=1000) # Define a count vectorizer with n-gram range of 2 to 3 and maximum features of 1000
    ngrams = ngrams.fit_transform(tokens) # Fit and transform the tokens to a sparse matrix
    ngrams = ngrams.toarray() # Convert the sparse matrix to a dense array
    # Concatenate the features
    features = np.concatenate([embeddings, bow, tfidf, ngrams], axis=1) # Concatenate the features along the second axis
    # Return the features
    return features

# Apply the feature extraction function to the training and testing sets
X_train = feature_extraction(X_train)
X_test = feature_extraction(X_test)

# Save the features in a CSV file
with open("features.csv", "w") as f:
    f.write("features,label\n") # Write the header
    for feature, label in zip(X_train, y_train):
        # Write the feature and label in the CSV file
        f.write(f"{feature},{label}\n")
