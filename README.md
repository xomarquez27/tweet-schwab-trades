# tweet-schwab-trades.

Tweets option trades from Schwab trade notification emails. The code uses both Gmail and Twitter APIs to scrap option trade notifications from Charles Schwab on Gmail and tweet out their contents in the following format:  

Date of trade: 09/06/2019  
Action:                 Bought  
Quantity:               10  
Symbol:                 $AMZN 09/13/2019 1900.00 C  
Unit Price:             $2.00.

## Purpose
The reason for this project creation is wanting to be transparent as an option trader without having to commit the time to sharing everything I trade. This project saves me time, and it was a great challenge to work on, so hopefully it will also be useful to you. It is important to note that currently the project only works with Gmail and Charles Schwab. 

The code does not require any personal or private information from Charles Schwab as it only accesses the Gmail inbox and grabs the Charles Schwab trade notification email message. The code only works with the Gmail API and Charles Schwab emails messages, the reasons for that being that Charles Schwab email messages do include all necessary info about a trade whereas TD Ameritrade and other brokers (to my knowledge) do not include trade information in the trade confirmation emails they sends to their clients; Charles Schwab trade notification emails also arrive fairly quickly after a trade has been made.  

Other email clients could be added in the future as well as other brokers depending on whether the relevant information can be extracted from just the email message without having to access private account info.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Read below for notes on how to deploy the project on a live system.

### Prerequisites
Needless to say, in order for this program to be useful to you, you must trade with Charles Schwab, get trade notification  emails to a Gmail account, and also have a Twitter account to tweet those trades. This program was also developed for Mac/Linux systems although Windows support might come in the near future.  

There are a few imports on this project since we are using two separate APIs and some of the modules imported are not part of the python standard library, so you will want to create a virtual environment on your project folder to keep these imports from interfering with system Python. For more info on Python virtual environments go [here](https://docs.python.org/3/library/venv.html). Once a virtual environment has been set and it is activated, install the following libraries:  
> httplib2  
> tweepy  
> base64

### Installing
1. For the Gmail API, follow steps 1-2 [here](https://developers.google.com/gmail/api/quickstart/python).  
2. Go to Google developer console and create a new project. Along with that, you must enable the Gmail API and create credentials for it. 
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

We will also create a shell script so that the program will run everytime the .sh script is run. Alternatively you can type the steps from the .sh file manually in the terminal, however the point of this program is to save time, and having to run the program manually does not fulfill that mission. The best option is to create a crontab so that the .sh file runs at set intervals throughout the day i.e. during market hours.  
On your terminal type the following if you have never dealt with vim:  
`export VISUAL=nano; crontab -e`
if you do use vim or nano is default on your system then just open a crontab and insert this line into the file:  
`30 7-13 * * 1-5 ~/Location/of/sh/file.sh`

For those not familiar with cron, cron is a time-based job scheduler that works on both Mac and Linux.
The format is something like this `* * * * * ~/Address/of/jobfile.ext` where each asterisk denotes a time period from min, hour, day, month, and day of the week in that order. In the above example cron will run the script at minute 30 on every hour from 7am to 1pm (including 1:30pm) every day of every month, but from day of the week 1 (Monday) to day of the week 5 (Friday). 

I chose this time because there's no need to check every 5 minutes since I do not trade that much, also I live in the West Coast so my market hours are from 6:30am to 1pm. If you live in another timezone, then choose the market hours that are appropriate to you, as well as the frequency that the cronjob runs. Keep in mind that both Gmail and Twitter APIs will have restrictions on how many times you can make requests to them.


### Authors
* Xavier Otero Marquez
