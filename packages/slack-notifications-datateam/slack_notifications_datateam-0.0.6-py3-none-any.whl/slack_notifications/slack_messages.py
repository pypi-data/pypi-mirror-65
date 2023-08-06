import requests

def send_message(webhook_url=None,
                text=None):

    if webhook_url is None:
            raise ValueError('No valid Slack token.')
    if text is None:
        raise ValueError('A text is needed.')

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
        )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )