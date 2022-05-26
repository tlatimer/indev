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
        group_member_data = getGroupMemberData()
        # and then cache it
        with open('data.json', 'w') as jsonOut:
            json.dump(group_member_data, jsonOut)

        return group_member_data


def get_group_member_data():
    service = makeService()

    groupMembers = {}

    groupsAndLengths = getGroupsAndLengths(service)

    for group, length in groupsAndLengths.items():
        groupMembers[group] = getGroupMembers(service, group, length)

    return groupMembers


def getGroupsAndLengths(service, pageToken=''):
    """returns a dict of {'group email': expectedLengthOfGroup}"""
    data = service.groups().list(customer='my_customer', pageToken=pageToken).execute()

    groupEmails = {}

    for i in data['groups']:
        if i['directMembersCount'] != '0':
            groupEmails[i['email']] = i['directMembersCount']
        else:
            print(i['email'] + ' has no members!')

    if 'nextPageToken' in data:
        groupEmails.update(getGroupsAndLengths(service, pageToken=data['nextPageToken']))

    return groupEmails


def getGroupMembers(service, groupEmail, expectedLength=0, pageToken=''):
    data = service.members().list(groupKey=groupEmail, pageToken=pageToken).execute()

    print('processing: ' + groupEmail)

    assert 'members' in data  # no members in group
    groupMembers = [i['email'] for i in data['members']]

    if 'nextPageToken' in data:
        groupMembers += getGroupMembers(service, groupEmail, pageToken=data['nextPageToken'])

    if expectedLength != 0 and expectedLength == len(data['members']):
        raise 'not expected length'

    return groupMembers


def makeService():
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
