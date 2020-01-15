from __future__ import print_function
import pickle
import os.path
import email
import httplib2
import logging
import tweepy
import json
from base64 import urlsafe_b64decode
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from time import strftime


logging.basicConfig(filename="app.log", filemode="a", format="%(asctime)s)"
                    " - %(name)s - %(levelname)s - %(message)s")


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

    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
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


class Status(object):
    """docstring for Status"""

    def __init__(self, date, action, quantity, asset, price):
        self.date = date
        self.action = action
        self.quantity = quantity
        self.asset = "$" + asset
        self.price = price
        self.message = message = "This tweet was automated. Check out my pinned tweet to learn how."


    def __str__(self):
        return f"{self.action} {self.quantity} {self.asset}\n"\
        		f"on{self.date}\n"\
        		f"at {self.price} per contract. \n\n"\
        		f"{self.message}"


def extractor(msg):
    trade_time = msg["payload"]["headers"][1]["value"][-32:]
    b64_string = msg["payload"]["parts"][0]["body"]["data"]

    return (trade_time, b64_string)


def b64_validator(*payload):
    """Checks if base64 string is a multiple of 4 and returns it
    unchanged if so, otherwise it will trim the tail end by the
    digits necessary to make the string a multiple of 4

    Args:
      encodedb64: Base64 string.

    Returns:
      decoded Base64 string.
    """
    date, encodedb64 = payload

    overflow = (len(encodedb64) % 4)
    if (overflow != 0):
        trimmed = encodedb64[: len(encodedb64) - overflow]
        return trimmed
    else:
        return (date, encodedb64)


def parser(*raw_string):
    """Removes unnecessary characters from decoded base64 email content.

    Args: raw_string: Python string containing the email's content.

    Returns: Python tuple of strings containing the email's formatted content for object creation.
    """
    date = raw_string[0]
    content = str(urlsafe_b64decode(raw_string[1]))
    relevant = content[content.find("Action") : content.find("Unit Price")+30]
    stripped = relevant.replace("\\r\\n", "\n").replace("\\r", " ").replace("\\", ".")
    data = ["Action:", "Quantity:", "Symbol:", "Unit Price:"]
    raw_attributes = []
    attributes = []

    for item in data:
        raw_attributes.append(stripped[stripped.find(item) + 24 : stripped.find(item) + 50])

    # Clean attributes by removing '\n' and any other irrelevant text following after
    for string in raw_attributes:
        if "\n" in string:
            attributes.append(string[:string.find("\n")])
        else:
            attributes.append(string)

    return (date, *attributes)


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
        with open("email_ids.txt", "w") as local:
            for msg_id in inbox[19::-1]:
                message = GetMessage(key, "me", msg_id['id'])
                if "Trade Notification" in message['snippet']:
                    raw_data = extractor(message)
                    valid_b64 = b64_validator(*raw_data)
                    content = parser(*valid_b64)
                    tweet = Status(*content)
                    # Send to Twitter
                    try:
                    	# print(tweet)
                        twitter.update_status(tweet)
                    except tweepy.error.TweepError:
                        logging.error(f"{strftime('%Y-%m-%d %H:%M')}: The following tweet failed {tweet}", exc_info=True)
                    finally:
                        print(tweet)
                        local.write(f'{msg_id["id"]}\n')
                else:
                    pass

    else:
        sent = []
        with open("email_ids.txt", "r") as local:
            for msg in local:
                sent.append(msg)
        for msg_id in inbox[19::-1]:
            if msg_id["id"] in sent:
            	pass
            else:
                message = GetMessage(key, "me", msg_id['id'])
                if "Trade Notification" in message['snippet']:
                    raw_data = extractor(message)
                    valid_b64 = b64_validator(*raw_data)
                    content = parser(*valid_b64)
                    tweet = Status(*content)
                    # Send to Twitter
                    try:
                    	# print(tweet)
                        twitter.update_status(tweet)
                    except tweepy.error.TweepError:
                        logging.error(f"{strftime('%Y-%m-%d %H:%M')}: The following tweet failed {tweet}", exc_info=True)
                    finally:
                        sent.append(msg_id["id"])
                else:
                    pass
        with open("email_ids.txt", "w") as out:
            for msg_id in sent[:20]:
            	out.write(f'{msg_id}')


if __name__ == '__main__':
    key = authorization()
    inbox = ListMessagesMatchingQuery(key, "me", query)
    twitter = twitter_auth()
    main()
