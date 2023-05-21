
from datetime import datetime
class Log:
    def __init__(self, file_name='log.txt'):
        self.file_name = file_name
    def write(self, message):
        with open(self.file_name, 'a+') as f:
            f.write(f"{datetime.now()}: {message}")
