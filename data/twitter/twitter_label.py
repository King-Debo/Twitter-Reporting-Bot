# Import the requests and BeautifulSoup libraries
import requests
from bs4 import BeautifulSoup

# Define the source URL
source_url = "https://www.snopes.com/fact-check/" # The URL of the fact-checking website

# Load the tweet data from the CSV file
with open("twitter_data.csv", "r") as f:
    tweet_data = f.readlines()[1:] # Skip the header

# Create a list to store the labels
labels = []

# Loop through each tweet
for tweet in tweet_data:
    # Extract the tweet text
    tweet_text = tweet.split(",")[1] # The tweet text is the second column
    # Search for the tweet text on the source website
    response = requests.get(source_url, params={"s": tweet_text}) # Use the tweet text as the search query
    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the first fact-check article that matches the tweet text
    article = soup.find("article", class_="search-result") # The fact-check articles have the class "search-result"
    # Check if the article exists
    if article:
        # Extract the article title and link
        article_title = article.find("h2").text # The article title is inside a h2 tag
        article_link = article.find("a")["href"] # The article link is inside a a tag
        # Extract the article rating
        article_rating = article.find("div", class_="media rating") # The article rating is inside a div tag with the class "media rating"
        # Check if the rating exists
        if article_rating:
            # Extract the rating text and image
            rating_text = article_rating.find("span", class_="rating-label").text # The rating text is inside a span tag with the class "rating-label"
            rating_image = article_rating.find("img")["src"] # The rating image is inside a img tag
            # Assign a label based on the rating text
            if rating_text == "True":
                label = "Real" # The tweet is real if the rating is true
            elif rating_text == "False":
                label = "Fake" # The tweet is fake if the rating is false
            else:
                label = "Unknown" # The tweet is unknown if the rating is neither true nor false
        else:
            # If the rating does not exist, assign an unknown label
            label = "Unknown"
    else:
        # If the article does not exist, assign an unknown label
        label = "Unknown"
    # Append the label to the list
    labels.append(label)

# Save the labels in a CSV file
with open("twitter_label.csv", "w") as f:
    f.write("label\n") # Write the header
    for label in labels:
        # Write the label in the CSV file
        f.write(f"{label}\n")
