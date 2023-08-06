from spintop.persistence.singer_postgresql import AbstractSingerTarget

class SpintopAPIAnalytics(AbstractSingerTarget):
    def __init__(self, spintop_api):
        super().__init__()
        self.spintop_api = spintop_api

    @property
    def session(self):
        return self.spintop_api.session

    def send_messages(self, messages_str):
        return self.session.put(self.spintop_api.get_link('analytics.stream_update'), json=messages_str)
