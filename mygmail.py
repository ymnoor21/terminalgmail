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

    try:
        char_count = int(sys.argv[3])
    except IndexError:
        char_count = 100

    results = ListAllMessages(service, 'me', query, [path])
    messageDict = {}

    messages = []
    threads = []
    currThread = ''

    if results:
        for message in results:
            messageDict = GetMessage(service, 'me',
                                     message['id'])

            headers = messageDict['payload']['headers']
            currThread = message['threadId']

            if currThread not in threads:
                info = []
                info = GetFromAndTime(headers)
                info['data'] = messageDict['data'][:char_count]
                messages.append(info)
                threads.append(currThread)

    msg_len = len(messages)

    display_init_msg = "\nFetching " +\
                       str(msg_len) +\
                       " email(s) from " + path + "."

    print (display_init_msg)
    print (len(display_init_msg) * "-")

    if msg_len > 0:
        seq = 1
        for message in messages:
            from_str = message['from']
            date_str = message['date'].__str__()
            subject_str = message['subject']\
                if message['subject'] else "(No Subject)"

            msg_str = message['data']\
                if message['data'] else "(No Message)"

            email_str = "\nEmail: " + str(seq)
            print (email_str)
            print (len(email_str) * "-")

            print ("\n+ From: " + from_str +
                   ", at " + date_str + "\n" +
                   "  Sub: " + subject_str + "\n" +
                   "  Msg: " + msg_str + "\n" +
                   "--------------------------\n")

            seq += 1

if __name__ == '__main__':
    main()
