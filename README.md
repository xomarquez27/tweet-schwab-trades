# tweet-schwab-trades
Tweets option trades from Schwab trade notification emails. The code uses both Gmail and Twitter APIs to scrap option trade notifications
from Charles Schwab on Gmail and tweet out their contents in the following format:  

Date of trade: 09/06/2019  
Action:                 Bought  
Quantity:               10  
Symbol:                 $AMZN 09/13/2019 1900.00 C  
Unit Price:             $2.00.

## Purpose
The reason for this project creation is wanting to be transparent as an option trader without having to commit the time to sharing everything I trade. This project saves me time, and it was a great challenge to work on, so hopefully it will also be useful to you. It is important to note that currently the project only works with Gmail and Charles Schwab. 

The code does not require any personal or private information from Charles Schwab as it only accesses the Gmail inbox and grabs the Charles Schwab trade notification email message. The code only works with the Gmail API and Charles Schwab emails messages, the reasons for that being that Charles Schwab email messages do include all necessary info about a trade whereas TD Ameritrade and other brokers (to my knowledge) do not include trade information in the trade confirmation emails they sends to their clients, Charles Schwab trade notification emails also arrive fairly quickly after a trade has been made.  

Other email clients could be added in the future as well as other brokers depending on whether the relevant information can be extracted from just the email message without having to access private account info.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
There are a few imports on this project since we are using two separate APIs and some of the modules imported are not part of the python standard library, so you will want to create a virtual environment on your project folder to keep these imports from interfering with system Python. For more info on Python virtual environments go [here](https://docs.python.org/3/library/venv.html). Once a virtual environment has been set and it is activated, install the following libraries:  
> httplib2  
> tweepy  
> base64

### Installing
1. For the Gmail API, follow steps 1-2 [here](https://developers.google.com/gmail/api/quickstart/python).  
2. Go to Google developer conosle and create a new project. Along with that, you must enable the Gmail API and create credentials for it. 
3. Download the credentials file onto the project's folder and rename the file client_secret.json as the program require it to access Gmail.
4. For the Twitter part, visit [Twitter's Developers Site](https://developer.twitter.com/) and sign in with your twitter account.
5. Create an app and name it as appropriate, fill out the basic info and description, do not worry about website if you do not have one, a fake url will work.
6. Create the access token and choose the access required "read and write" in this case.
7. Create a json file on your project folder with the following contents:  
>{    
    "consumer_key": "randomstringhere",  
    "consumer_secret": "randomstringhere",  
    "access_token": "randomstringhere",  
    "access_token_secret": "randomstringhere"  
>}  

 and replace every randomstringhere with the respective value from Twitter. I named this file tweepy.json and you can see it referenced in the code, however you can name it differently just remember to change the part of the code where tweepy.json is referenced to whichever name you chose.

### Deployment
Copy the code on tweet_schwab.py to your main python file. 
Your project folder should contain the client_secret.json file which contains your keys to access Gmail, tweepy.json file or equivalent file, the main python file containing the program's code, and finally the virtual environment folder.

### Authors
* Xavier Otero Marquez
