import json
import os.path

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def main():
    if os.path.exists('data.json'):
        # load cached data
        with open('data.json', 'r') as json_in:
            return json.load(json_in)

    else:
        # gotta go get that data
        group_member_data = get_group_member_data()
        # and then cache it
        with open('data.json', 'w') as jsonOut:
            json.dump(group_member_data, jsonOut)

        return group_member_data


def get_group_member_data():
    service = make_service()

    group_members = {}

    groups_and_lengths = get_groups_and_lengths(service)

    for group, length in groups_and_lengths.items():
        group_members[group] = get_group_members(service, group, length)

    return group_members


def get_groups_and_lengths(service, page_token=''):
    """returns a dict of {'group email': expectedLengthOfGroup}"""
    data = service.groups().list(customer='my_customer', pageToken=page_token).execute()

    group_emails = {}

    for i in data['groups']:
        if i['directMembersCount'] != '0':
            group_emails[i['email']] = int(i['directMembersCount'])
        else:
            print(i['email'] + ' has no members!')

    if 'nextPageToken' in data:
        group_emails.update(get_groups_and_lengths(service, page_token=data['nextPageToken']))

    return group_emails


def get_group_members(service, group_email, expected_length=0, page_token=''):
    data = service.members().list(groupKey=group_email, pageToken=page_token).execute()

    print('processing: ' + group_email)

    assert 'members' in data  # no members in group
    group_members = [i['email'] for i in data['members']]

    if 'nextPageToken' in data:
        group_members += get_group_members(service, group_email, page_token=data['nextPageToken'])

    if expected_length:  # top level call, not a recursive call
        assert expected_length == len(group_members)  # not expected length

    return group_members


def make_service():
    scopes = ['https://www.googleapis.com/auth/admin.directory.user.readonly',
              'https://www.googleapis.com/auth/admin.directory.group.readonly']
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        # If no valid creds, open a browser window to complete OAuth flow and save token.
        flow = client.flow_from_clientsecrets('credentials.json', scopes)
        creds = tools.run_flow(flow, store)

    return build(
        serviceName="admin",
        version="directory_v1",
        http=creds.authorize(Http()))


if __name__ == '__main__':
    main()
