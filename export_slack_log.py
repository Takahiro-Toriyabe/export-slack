import os
from slack_sdk import WebClient
import time
import requests
from env import pwd, tokens

for ws, token in tokens.items():
    # Set path and make directory if not exist
    path_ws = os.path.join(pwd, ws)
    path_file = os.path.join(path_ws, 'files')
    try:
        os.mkdir(path_ws)
        os.mkdir(path_file)
    except:
        pass

    # Get information for workspace and collect channel names and IDs
    print(f'Export {ws}')
    client = WebClient(token=token)
    client_conversation = client.conversations_list(
        types='public_channel, private_channel, mpim')
    channels = [[channel['name'], channel['id']]
                for channel in client_conversation['channels']]

    # Make mapping from user ID to username
    user_dict = {mem['id']: mem['real_name']
                for mem in client.users_list()['members'] if mem['deleted'] is False}
    user_dict.update({mem['id']: mem['profile']['real_name'] for mem in client.users_list()['members'] if mem['deleted'] is True})

    # Direct messages
    dm = client.conversations_list(types='im')
    channels = channels + [[user_dict[x['user']], x['user']]
                        for x in dm['channels'] if x['is_user_deleted'] is False]

    # Export messages
    for name, id in channels:
        path = os.path.join(path_ws, name)
        print(f'Exporting {name} to {os.path.join(path, "log.csv")}... ', end='')
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        flag_continue = True
        cursor = None
        with open(os.path.join(path, 'log.csv'), 'w', encoding='utf8') as f:
            while flag_continue:
                try:
                    result = client.conversations_history(
                        channel=id, cursor=cursor, limit=1000)
                except:
                    flag_continue = False
                for m in result['messages']:
                    try:
                        user = user_dict[m['user']]
                    except KeyError:
                        user = 'Slackbot'
                    ts = time.ctime(float(m['ts'][:10]))
                    text = m['text'].replace('\n', '').replace(',', '')
                    for key, val in user_dict.items():
                        text = text.replace(key, val)

                    f.write(f'{user}, {ts}, {text}\n')

                metadata = result['response_metadata']
                if metadata is None:
                    break
                cursor = metadata['next_cursor']
        print('Done')

    # Download files
    files = client.files_list()
    print(f'Exporting files to {path_file}... ', end='')
    for f in files['files']:
        outpath = os.path.join(path_file, f['name'])
        r = requests.get(f['url_private_download'], allow_redirects=True)
        open(outpath, 'wb').write(r.content)
    print('Done')
    print('')
