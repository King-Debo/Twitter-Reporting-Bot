# Import the smtplib, email, requests, and flask libraries
import smtplib
from email.message import EmailMessage
import requests
from flask import Flask, render_template

# Define the email credentials
email_user = "YOUR_EMAIL_ADDRESS" # The email address of the sender
email_password = "YOUR_EMAIL_PASSWORD" # The email password of the sender
email_receiver = "YOUR_EMAIL_ADDRESS" # The email address of the receiver

# Define the email function
def send_email(text, prediction):
    # Create an email message
    email = EmailMessage() # Create an email message object
    email["Subject"] = "Web Bot Alert" # Set the subject of the email
    email["From"] = email_user # Set the sender of the email
    email["To"] = email_receiver # Set the receiver of the email
    # Set the content of the email
    email.set_content(f"""Hello,

This is an alert from the web bot.

The web bot has detected a tweet with the following text:

{text}

The web bot has classified this tweet as {prediction}.

Please verify the accuracy of this classification and take appropriate action.

Thank you.""")
    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: # Create a SMTP_SSL object with the Gmail server and port
        smtp.login(email_user, email_password) # Login to the Gmail server with the email credentials
        smtp.send_message(email) # Send the email message

# Define the SMS credentials
sms_url = "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json" # The Twilio API URL
sms_user = "YOUR_ACCOUNT_SID" # The Twilio account SID
sms_password = "YOUR_AUTH_TOKEN" # The Twilio auth token
sms_sender = "YOUR_TWILIO_NUMBER" # The Twilio phone number of the sender
sms_receiver = "YOUR_PHONE_NUMBER" # The phone number of the receiver

# Define the SMS function
def send_sms(text, prediction):
    # Create an SMS message
    sms = {"From": sms_sender, # Set the sender of the SMS
           "To": sms_receiver, # Set the receiver of the SMS
           "Body": f"Web Bot Alert: The web bot has detected and classified a tweet as {prediction}. Please check your email for more details."} # Set the body of the SMS
    # Send the SMS
    requests.post(sms_url, auth=(sms_user, sms_password), data=sms) # Make a POST request to the Twilio API URL with the SMS message and the SMS credentials

# Define the web credentials
web_app = Flask(__name__) # Create a Flask app object
web_port = 5000 # The port number for the web app

# Define the web function
def send_web(text, prediction):
    # Create a web page
    @web_app.route("/") # Define the route for the web page
    def web_page():
        # Render the web page using a template
        return render_template("web_page.html", text=text, prediction=prediction) # Render the web page using the web_page.html template and pass the text and prediction as variables
    # Run the web app
    web_app.run(port=web_port) # Run the web app on the specified port

# Load the predictions from the CSV file
with open("predictions.csv", "r") as f:
    predictions = f.readlines()[1:] # Skip the header

# Load the tweet data from the CSV file
with open("twitter_data.csv", "r") as f:
    tweet_data = f.readlines()[1:] # Skip the header

# Loop through each prediction and tweet
for prediction, tweet in zip(predictions, tweet_data):
    # Extract the prediction and tweet text
    prediction = prediction.strip() # Remove the newline character
    tweet_text = tweet.split(",")[1] # The tweet text is the second column
    # Check if the prediction is fake
    if prediction == "Fake":
        # Generate and send an alert or report
        send_email(tweet_text, prediction) # Send an email
        send_sms(tweet_text, prediction) # Send an SMS
        send_web(tweet_text, prediction) # Send a web page
