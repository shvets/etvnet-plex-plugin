class ErrorHandler():
    def __init__(self, error_callback=None):
       self.error_callback = error_callback

    def handle_exception(self, callback, error_callback=None, exception_type=Exception, **args):
        if error_callback:
            current_error_callback = error_callback
        else:
            current_error_callback = self.error_callback

        try:
            return callback(**args)
        except exception_type as e:
            return current_error_callback(e)