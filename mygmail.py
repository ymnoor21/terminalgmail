import httplib2
from credentials import get_credentials
from apiclient import discovery
from mymessages import ListAllMessages
from mymessages import GetMessage, GetFromAndTime
import sys


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        query = sys.argv[1]
    except IndexError:
        query = 'is:unread'

    try:
        path = sys.argv[2]
    except IndexError:
        path = 'INBOX'

    results = ListAllMessages(service, 'me', query, [path])
    rawData = {}

    messages = []
    threads = []
    currThread = ''

    if not results:
        print ('No messages found.')
    else:
        for message in results:
            rawData = GetMessage(service, 'me',
                                 message['id'])

            headers = rawData['payload']['headers']
            currThread = message['threadId']

            if currThread not in threads:
                info = []
                info = GetFromAndTime(headers)
                messages.append(info)
                threads.append(currThread)

    msg_len = len(messages)

    display_init_msg = "\nFetching " +\
                       str(msg_len) +\
                       " email(s) from " + path + "."

    print (display_init_msg)
    print (len(display_init_msg) * "-")

    if msg_len > 0:
        for message in messages:
            from_str = message['from']
            date_str = message['date'].__str__()
            subject_str = message['subject']\
                if message['subject'] else "(No Subject)"

            print ("+ From: " + from_str +
                   ", at " + date_str + "\n" +
                   "  Sub: " + subject_str + "\n\n")

if __name__ == '__main__':
    main()
