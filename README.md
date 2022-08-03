# export-slack

## Requirement

- Python 3.X: Install the following libraries
  - `slack_sdk`
  - `requests`

## Get Slack API token

1. Sign in to your Slack workspace with your web browser 
2. Click `Your apps` in [this page](https://api.slack.com/apps)
3. Click `Create an app` and choose `From an app manifest`
4. Select your workspace
5. Copy and paste [manifest.yml](https://github.com/Takahiro-Toriyabe/export-slack/blob/main/manifest.yml)
6. Click `Create`
7. Click `Install to Workspace`

## Set up `env.py` file

1. rename [`env_example.py`](https://github.com/Takahiro-Toriyabe/export-slack/blob/main/env_example.py) to `env.py`
2. Edit `env.py`
   - Set `pwd` where your slack log will be exported
   - Set `tokens`: You can find your User OAuth Token from `OAuth & Permissions` in Slack API web page

**Keep User OAuth Token confidential**: It gives access to your slack messages

## Take Slack message log

- Make sure that `env.py` is in the same directory as [`export_slack_log.py`](https://github.com/Takahiro-Toriyabe/export-slack/blob/main/export_slack_log.py)
- Run [`export_slack_log.py`](https://github.com/Takahiro-Toriyabe/export-slack/blob/main/export_slack_log.py)
  - Messages will be exported to `pwd`/`workspace_name`/`channel_name`/log.csv with **utf-8** format
  - Files uploaded on Slack will be exported to `pwd`/`workspace_name`/files/

## Bugs/Limitations

- For some reasons, direct messages are not exported (multi-persons direct messages are exported)
- Deleted channels are not exported
