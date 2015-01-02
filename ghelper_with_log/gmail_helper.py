#-*-coding:utf-8 -*-
import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
from apiclient import errors
import time
from auto2 import send_mail
import base64
import email
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                datefmt='%Y %m %d %H:%M:%S',
                filename='mail_note.log',
                filemode='a')
mail_log = logging.getLogger('maillog')


last_email = ''


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

# Retrieve a page of threads
# threads = gmail_service.users().threads().list(userId='me').execute()

# # Print ID for each thread
# if threads['threads']:
#   for thread in threads['threads']:
#     print 'Thread ID: %s' % (thread['id'])

def ListMessagesWithLabels(service, user_id, label_ids=[]):
  """List all Messages of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

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

    print 'Message snippet: %s' % message['snippet']

    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def init():
  global last_email
  last_email = ListMessagesWithLabels(gmail_service,'me')[0]['id']

def isnew():
  global last_email
  themail = ListMessagesWithLabels(gmail_service,'me')
  for each in themail:
    if each['id'] != last_email:
      tosend(each['id'])
    else:
      mail_log.info(u'没有新邮件')
      break
  last_email = themail[0]['id']

def tosend(id):
  b = GetMessage(gmail_service,'me',id)
  content =  b['snippet']
  sender =  b['payload']['headers'][3]['value']
  subject = b['payload']['headers'][12]['value']
  body = sender + '\n' + content
  send_mail(subject,body)
  mail_log.info(subject)
  mail_log.info(body)

if __name__=='__main__':
    init()
    mail_log.info(u'邮件转发开始！')
    while 1:
      time.sleep(3600) #每一小时检查一次邮箱
      isnew()


