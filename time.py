from datetime import datetime


class DateTime(datetime):

    def db_format(self):
        return self.strftime('%Y-%d-%m %H:%M:%S')
