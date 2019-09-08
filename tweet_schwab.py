from __future__ import print_function
import pickle
import os.path
import email
import httplib2
import tweepy
import json
from base64 import urlsafe_b64decode
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

user_id = "xomarquez27@gmail.com" # Replace with your email address
query = "From: Schwab Alerts"
file_location = '/home/xavier/Desktop/Python/Schwab_Tweets/email_ids.txt' # Replace with path/to/your/folder/email_ids.txt


def authorization():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    # print 'Message snippet: %s' % message['snippet']

    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def checker(encodedb64):
    """Checks if base64 string is a multiple of 4 and returns it
    unchanged if so, otherwise it will trim the tail end by the
    digits necessary to make the string a multiple of 4

    Args:
      encodedb64: Base64 string.

    Returns:
      decoded Base64 string.  
    """
    overflow = (len(encodedb64) % 4)
    if (overflow != 0):
        trimmed = encodedb64[: len(encodedb64) - overflow]
        return trimmed
    else:
        return encodedb64


def parser(raw_string):
    """Removes unnecessary characters from decoded base64 email content.

    Args: raw_string: Python string containing the email's content.

    Returns: Python string containing the email's formatted content ready to be tweeted.
    """
    content = str(urlsafe_b64decode(raw_string))
    date = content[content.find("ending") + 17 : content.find("ending") + 27] + "\n"
    relevant = content[content.find("Action") : content.find("Unit Price")+30]
    stripped = relevant.replace("\\r\\n", "\n").replace("\\r", " ").replace("\\", ".")
    return "Date of trade: " + date + stripped
    

def hashtag(message):
    """Adds the $ sign to the symbol in the tweet so that the tweet appears
    on searches for that particular symbol, e.g. $AMZN, $SPY, etc.

    Args: String to be tweeted.

    Returns: String with $ sign before the ticker.
    """ 
    ticker = message.find("Symbol:") + 24
    tweet_ready = message[:ticker] + '$' + message[ticker:]
    return tweet_ready


def twitter_auth():

    """Twitter session authorization"""

    config_file = '.tweepy.json'
    with open(config_file) as fh:
        config = json.load(fh)

    auth = tweepy.OAuthHandler(
        config['consumer_key'], config['consumer_secret']
    )
    auth.set_access_token(
        config['access_token'], config['access_token_secret']
    )

    return tweepy.API(auth)


def main():
    """Puts the previous functions into work by combining them to extract the email, parse it and tweet it."""
    # If email_ids.txt file does not exist i.e. first time running the program
    if not os.path.exists(file_location):    
        with open("email_ids.txt", "w") as file:
            for msg_id in batch[0:6]:
                message = GetMessage(key, "me", msg_id['id'])
                if "Trade Notification" in message['snippet']:
                    b64_string = message["payload"]["parts"][0]["body"]["data"]
                    valid_b64 = checker(b64_string)
                    content = parser(valid_b64)
                    tweet = hashtag(content)
                    # Send to Twitter
                    twitter.update_status(tweet)
                    print(tweet)
                else:
                    pass
                file.write(msg_id["id"] + "\n")
    else:
        old_batch = []
        with open("email_ids.txt", "r") as file:
            for msg_id in file:
                old_batch.append(msg_id)    
            for msg_id in batch[4::-1]:
                if msg_id in old_batch:
                    pass
                else:
                    message = GetMessage(key, "me", msg_id['id'])
                    if "Trade Notification" in message['snippet']:
                        b64_string = message["payload"]["parts"][0]["body"]["data"]
                        valid_b64 = checker(b64_string)
                        content = parser(valid_b64)
                        tweet = hashtag(content)
                        # Send to Twitter
                        twitter.update_status(tweet)
                        print(tweet)
                        old_batch.insert(0, msg_id)
                        del old_batch[-1]
                    else:
                        pass
        with open("email_ids.txt", "w") as file:
            for msg in old_batch:
                file.write(msg_id["id"] + "\n")


if __name__ == '__main__':
    key = authorization()
    batch = ListMessagesMatchingQuery(key, "me", query)
    twitter = twitter_auth()
    main()