from datetime import datetime


class TimeService(object):
    def get_datetime_now(self):
        return datetime.utcnow().timestamp()
