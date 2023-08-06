class SlackMessage(object):

    @apply_defaults
    def __init__(self,
                 webhook_url=None,
                 text=None,
                 *args, **kwargs):

        if webhook_url is None:
            raise ValueError('No valid Slack token.')
        if text is not None:
            raise ValueError('A text is needed.')

        self.webhook_url = webhook_url
        self.slack_data = {'text': text}

    def slack_message(context):
        response = requests.post(
            self.webhook_url, data=json.dumps(self.slack_data),
            headers={'Content-Type': 'application/json'}
            )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )