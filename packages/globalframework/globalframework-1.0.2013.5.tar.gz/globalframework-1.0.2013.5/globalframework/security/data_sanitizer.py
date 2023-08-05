# default libraries
import html


# Class to sanitize data. This is part of preventing XSS

class DataSanitizer:
    def __init__(self):
        pass


    def sanitize(self, data):
        """Sanitize data

        Args:\n
            data (str):

        Returns:
            Sanitized data
        """

        return html.escape(data)