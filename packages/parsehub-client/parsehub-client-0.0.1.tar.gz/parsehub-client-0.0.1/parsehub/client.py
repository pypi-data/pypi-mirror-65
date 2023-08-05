import requests

# What's this client going to be able to do?
# Get projects
# Get runs
# Get data from run

# classes:
# Client
# Project
# Run


class ParseHubClient(object):
    def __init__(self, api_token):
        self.token = api_token


