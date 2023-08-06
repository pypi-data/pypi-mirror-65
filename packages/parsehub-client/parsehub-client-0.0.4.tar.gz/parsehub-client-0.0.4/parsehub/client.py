import requests
import json
import logging
from datetime import datetime

from .utils import _parse_response_data

class ParseHubClient(object):
    
    def __init__(self, api_key=None):
        self.api_key = api_key

    def authenticate(self, api_key):
        self.api_key = api_key

    def get_run(self, run_token):
        '''Documentation: https://www.parsehub.com/docs/ref/api/v2/?python#get-a-run'''
        run_endpoint = f'https://www.parsehub.com/api/v2/runs/{run_token}'
        params = {'api_key': self.api_key}
        
        response = requests.get(run_endpoint, params=params)
        run = ParseHubRun(**response.json(), client=self)
        return run
    
    def get_project(self, project_token, offset=0, include_options=0):

        project_endpoint = f'https://www.parsehub.com/api/v2/projects/{project_token}'
        params = {
            'api_key': self.api_key,
            'offset': offset,
            'include_options': include_options
        }
        response = requests.get(project_endpoint, params=params)
        project = ParseHubProject(client=self, **response.json())
        return project 

    def list_projects(self, offset=0, limit=2, include_options=0):
        
        project_endpoint = 'https://www.parsehub.com/api/v2/projects'
        params = {
            'api_key': self.api_key,
            'offset': offset,
            'limit': limit,
            'include_options': include_options
        }
        response = requests.get(project_endpoint, params=params)
        
        # return response
        project_list = []
        for project_json in response.json()['projects']:
            project_list.append(ParseHubProject(client=self, **project_json))

        return project_list


class ParseHubProject(object):
    '''A single ParseHub Project'''
    def __init__(self, client, *initial_data, **kwargs):

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        # value formatting
        try:
            self.last_ready_run = ParseHubRun(client=client, **self.last_ready_run)
        except AttributeError:
            raise AttributeError # until I know when this happens

    def run(self, start_url=None, start_template=None, start_value_override=None, send_email=None):
        '''Documentation: https://www.parsehub.com/docs/ref/api/v2/?python#run-a-project'''
        project_run_endpoint = f"https://www.parsehub.com/api/v2/projects/{self.project_token}/run"
        params = {
            "api_key": self.client.api_key,
            "start_url": start_url,
            "start_template": start_template,
            "start_value_override": start_value_override,
            "send_email": send_email
        }
        response = requests.post(project_run_endpoint, data=params)
        return ParseHubRun(client=self.client, **response.json())

    def get_last_ready_data(self, format='json'):
        '''Documentation: https://www.parsehub.com/docs/ref/api/v2/?python#get-last-ready-data'''
        last_ready_endpoint = f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data'
        params = {"api_key": self.api_key, "format": format}
        
        response = requests.get(last_ready_endpoint, params=params)
        return _parse_response_data(response, format)


class ParseHubRun(object):
    '''A single ParseHub Run'''
    def __init__(self, client, *initial_data, **kwargs):
        
        self.client = client

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, None if dictionary[key]=='' else dictionary[key])
        for key in kwargs:
            setattr(self, key, None if kwargs[key]=='' else kwargs[key])

        # # value formatting
        # self.start_value = json.loads(self.start_value) if self.start_value else None
        # self.options_json = json.loads(self.options_json) if self.options_json else None
        # self.data_ready = bool(self.data_ready)
        # self.start_time = datetime.fromisoformat(self.start_time)
        # self.end_time = datetime.fromisoformat(self.end_time)
        # self.start_running_time = datetime.fromisoformat(self.start_running_time)

    def get_data(self, format='json'):
        '''Documentation: https://www.parsehub.com/docs/ref/api/v2/?python#get-data-for-a-run'''
        run_data_endpoint = f'https://www.parsehub.com/api/v2/runs/{self.run_token}/data'
        params = {'api_key': self.client.api_key, 'format': format}
        
        response = requests.get(run_data_endpoint, params=params)
        return _parse_response_data(response, format)

    def cancel(self):
        '''Documentation: https://www.parsehub.com/docs/ref/api/v2/?python#cancel-a-run'''
        cancel_run_endpoint = f"https://www.parsehub.com/api/v2/runs/{self.run_token}/cancel"
        params = {"api_key": self.client.api_key}
        response = requests.post(cancel_run_endpoint, data=params)
        return response.json()

    def delete(self):
        '''Documentation: https://www.parsehub.com/docs/ref/api/v2/?python#delete-a-run'''
        delete_run_endpoint = f'https://www.parsehub.com/api/v2/runs/{self.run_token}'
        params = {"api_key": self.client.api_key}
        
        response = requests.delete(delete_run_endpoint, params=params)
        return response.json()
