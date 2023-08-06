from auger.api.auth import AugerAuth


class AuthCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def login(self, username, password, organization, url):
        AugerAuth(self.ctx).login(username, password, organization, url)

    def logout(self):

        AugerAuth(self.ctx).logout()

    def whoami(self):
        AugerAuth(self.ctx).whoami()
