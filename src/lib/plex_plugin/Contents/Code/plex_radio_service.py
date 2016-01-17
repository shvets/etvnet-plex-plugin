from error_handler import ErrorHandler
from radio_service import RadioService

class PlexRadioService(RadioService):
     def __init__(self, error_callback=None):
        self.error_handler = ErrorHandler(error_callback)