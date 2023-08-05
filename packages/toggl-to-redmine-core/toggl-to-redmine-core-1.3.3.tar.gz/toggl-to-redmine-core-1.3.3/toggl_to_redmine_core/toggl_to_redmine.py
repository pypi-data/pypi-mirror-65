import logging
from .config import AppConfig
from .exceptions import ConfigException, RedmineIntegrationException
from .time_entry import TimeEntry
from .redmine_integrator import RedmineIntegrator
from .toggl_integrator import TogglIntegrator

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


def toggl_to_redmine(config):
    """ A program to automaticaly import Toggl time entries to a Redmine app """
    app_config = AppConfig(config)
    redmine = RedmineIntegrator(app_config.redmine_config())
    toggl = TogglIntegrator(app_config.toggl_config())

    time_entries = toggl.fetch_time_entries()

    entries_logged = []
    entries_not_logged = []

    for time_entry in time_entries:
        if time_entry.should_be_imported():
            try:
                redmine.save_entry(time_entry)
                entries_logged.append(time_entry)
            except RedmineIntegrationException as e:
                msg = str(e)
                if msg == None or msg == '':
                    msg = 'Redmine integration failed'
                time_entry.message = msg
                entries_not_logged.append(time_entry)
        else:
            entries_not_logged.append(time_entry)
    
    toggl.update_saved_entries(entries_logged)

    return {
        'entries_saved': entries_logged,
        'entries_not_saved': entries_not_logged
    }
