from slacker import Slacker

token = 'xoxb-503049869125-507458091106-VjUMKk73BfGGUWTaiWSrFHxR'
slack = Slacker(token)

# Send a message to #general channel
slack.chat.post_message('#testing', 'Hello fellow slackers!')

# Get users list
response = slack.users.list()
users = response.body['members']
print(users)

# Upload a file
slack.files.upload('english.xlsx')

# If you need to proxy the requests
proxy_endpoint = 'http://myproxy:3128'
slack = Slacker(token,
                http_proxy=proxy_endpoint,
                https_proxy=proxy_endpoint)

# Advanced: Use `request.Session` for connection pooling (reuse)
from requests.sessions import Session
with Session() as session:
    slack = Slacker(token, session=session)
    slack.chat.post_message('#testing', 'All these requests')
    slack.chat.post_message('#testing', 'go through')
    slack.chat.post_message('#testing', 'a single https connection')