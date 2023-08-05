import requests
from requests.auth import HTTPBasicAuth
from .config import AppConfig
from .time_entry import TimeEntry
from .exceptions import TogglCommunicationException, TogglCredentialsException


class TogglIntegrator():
    """ Used to integrate with Toggl and get time entries """

    reports_url = 'https://toggl.com/reports/api/v2/details?'
    time_entries_url = 'https://www.toggl.com/api/v8/time_entries/'

    def __init__(self, config):
        self.config = config
        self.token = config.get('toggl_api_token')

    def fetch_time_entries(self):
        url = self.build_fetch_url()
        try:
            response = requests.get(
                url, auth=HTTPBasicAuth(self.token, 'api_token'))
        except ConnectionError:
            raise TogglCommunicationException()

        if not response.ok:
            raise TogglCredentialsException(response.json())

        time_entries = []
        for time_entry_data in response.json()['data']:
            time_entries.append(TimeEntry(time_entry_data))
        return time_entries
    
    def build_fetch_url(self):
        return TogglIntegrator.reports_url + self.get_time_entries_params()
    
    def update_saved_entries(self, entries):
        url = self.build_update_tags_url(entries)
        tag_info = {
            "time_entry": {
                "tags": ["SAVED"],
                "tag_action": "add"
            }
        }
        requests.put(
            url,
            data=tag_info,
            auth=HTTPBasicAuth(self.token, 'api_token')
        )
    
    def build_update_tags_url(self, entries):
        entries_ids = list(map(lambda e: e.id, entries))
        base_url = TogglIntegrator.time_entries_url
        ids = ','.join(entries_ids)
        return base_url + ids

    def get_time_entries_params(self):
        params = {
            "user_agent": self.config.get('toggl_user'),
            "workspace_id": self.config.get('toggl_workspace_id'),
            "since": self.config.get('toggl_start_date'),
            "until": self.config.get('toggl_end_date')
        }

        params_array = []
        for key in params:
            params_array.append(f'{key}={params[key]}')

        return '&'.join(params_array)
