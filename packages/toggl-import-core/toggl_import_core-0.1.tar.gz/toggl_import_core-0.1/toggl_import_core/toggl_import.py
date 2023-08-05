import logging
from .config import AppConfig
from .exceptions import ConfigException, EntryNotImportedException
from .time_entry import TimeEntry
from .toggl_integrator import TogglIntegrator

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


def toggl_import(config):
    """ A program to automaticaly import Toggl time entries """
    app_config = AppConfig(config)
    toggl = TogglIntegrator(app_config.toggl_config())

    time_entries = toggl.fetch_time_entries()

    entries_logged = []
    entries_not_logged = []

    import_handler = config['import_handler']

    for time_entry in time_entries:
        if time_entry.should_be_imported():
            try:
                import_handler(time_entry)
                entries_logged.append(time_entry)
            except EntryNotImportedException as e:
                msg = str(e)
                if msg == None or msg == '':
                    raise "There was no message explaining import failure"
                time_entry.message = msg
                entries_not_logged.append(time_entry)
        else:
            entries_not_logged.append(time_entry)
    
    toggl.update_saved_entries(entries_logged)

    return {
        'entries_saved': entries_logged,
        'entries_not_saved': entries_not_logged
    }
