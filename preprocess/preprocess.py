# Import the nltk and spacy libraries
import nltk
import spacy

# Download the nltk data
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load the spacy model
nlp = spacy.load("en_core_web_sm")

# Define the stop words
stop_words = nltk.corpus.stopwords.words("english")

# Define the stemmer
stemmer = nltk.stem.PorterStemmer()

# Define the lemmatizer
lemmatizer = nltk.stem.WordNetLemmatizer()

# Define the preprocess function
def preprocess(text):
    # Convert the text to lower case
    text = text.lower()
    # Remove punctuation and special characters
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    # Tokenize the text using nltk
    tokens = nltk.word_tokenize(text)
    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    # Stem the tokens using nltk
    tokens = [stemmer.stem(token) for token in tokens]
    # Lemmatize the tokens using spacy
    tokens = [nlp(token)[0].lemma_ for token in tokens]
    # Return the tokens
    return tokens

# Load the tweet data and labels from the CSV files
with open("twitter_data.csv", "r") as f1, open("twitter_label.csv", "r") as f2:
    tweet_data = f1.readlines()[1:] # Skip the header
    tweet_label = f2.readlines()[1:] # Skip the header

# Create a list to store the preprocessed data
preprocessed_data = []

# Loop through each tweet
for tweet, label in zip(tweet_data, tweet_label):
    # Extract the tweet text and label
    tweet_text = tweet.split(",")[1] # The tweet text is the second column
    tweet_label = label.strip() # Remove the newline character
    # Preprocess the tweet text
    tweet_tokens = preprocess(tweet_text)
    # Append the preprocessed data to the list
    preprocessed_data.append((tweet_tokens, tweet_label))

# Save the preprocessed data in a CSV file
with open("preprocessed_data.csv", "w") as f:
    f.write("tokens,label\n") # Write the header
    for tokens, label in preprocessed_data:
        # Write the tokens and label in the CSV file
        f.write(f"{tokens},{label}\n")
