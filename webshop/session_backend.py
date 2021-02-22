from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self):
        super(SessionStore, self).cycle_key()
        self.save()