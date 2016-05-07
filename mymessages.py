"""Get a list of Messages from the user's mailbox.
"""

from apiclient import errors
import base64
import dateutil.parser


def ListAllMessages(service, user_id='me', query='', path_name=[]):
    """List all Messages of the user's mailbox matching the query.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
        path_name: Messages with path_name applied. (ex: INBOX / Logcheck etc)

    Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
    """
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        ids = []
        for lblid in path_name:
            for label in labels:
                if label['name'] == lblid:
                    ids.append(label['id'])

        if not ids:
            raise Exception("Error with finding path name supplied.")

        response = service.users()\
            .messages()\
            .list(userId=user_id, q=query, labelIds=ids)\
            .execute()

        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users()\
                .messages()\
                .list(userId=user_id,
                      q=query,
                      labelIds=path_name,
                      pageToken=page_token)\
                .execute()

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
    message = []

    if not user_id:
        user_id = 'me'

    try:
        message = service.users().\
            messages().\
            get(userId=user_id, id=msg_id,
                format='full')\
            .execute()

        message['data'] = ''

        parts = []

        try:
            parts = message['payload']['parts']
            for obj in parts:
                message['data'] = obj['body'].get('data', '')

                if not message['data']:
                    for part in obj['parts']:
                        if part['body']['data']:
                            message['data'] = part['body']['data']
                            break

                if message['data']:
                    break

        except KeyError:
            message['data'] = message['payload']['body'].get('data', '')

        if message['data']:
            message['data'] = base64.urlsafe_b64decode(
                message['data'].encode('ascii')
            ).decode('latin-1')

    except errors.HttpError, error:
        print 'An error occurred: %s' % error

    return message


def GetFromAndTime(headers):
    if not headers:
        return None

    if headers:
        hFrom = ''
        hDate = ''
        hSubject = ''

        for header in headers:
            if header['name'] == 'From':
                hFrom = header['value']

            if header['name'] == 'Date':
                hDate = dateutil.parser.parse(header['value'])

            if header['name'] == 'Subject':
                hSubject = header['value']

            if hFrom != "" and hDate != "" and hSubject != "":
                break

    data = {
        'from': hFrom,
        'date': hDate,
        'subject': hSubject,
    }

    return data
