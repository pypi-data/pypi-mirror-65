class ConfigException(Exception):
    """ Exception used when the stored config is corrupted """
    pass


class TimeEntryValidationError(Exception):
    """ Exception used to express a validation problem on Time Entry """
    pass


class TogglCommunicationException(Exception):
    """ Exception used when the communication with Toggl Failed """
    pass


class TogglCredentialsException(Exception):
    """ Exception used when Toggl rejected user credentials """
    pass

class EntryNotImportedException(Exception):
    """
    Use this exception when you want Toggl Import to know that the current 
    entry was not imported by your custom logic. Be sure to add a message
    when using this exception, as it should be reported to the user as the reason
    why the entry was not imported. 
    """
    pass