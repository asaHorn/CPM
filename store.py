class pwdStore:
    pwds = dict()

    def __init__(self):
        pass

    def exists(self, user: str, box: str):
        try:
            self.prettyGetPwd(user, box)
        except KeyError:
            return False
        return True

    def addPwd(self, user: str, box: str, pwd: str):
        self.pwds[self.makeID(user, box)] = pwd

    def getPwd(self, user: str, box: str):
        return self.pwds[self.makeID(user, box)]

    def prettyGetPwd(self, user: str, box: str):
        return self.makeID(user, box) + ': ' + self.getPwd(user, box)

    def makeID(self, user: str, box: str):
        return user + '/' + box

    def dump(self):
        """
        returns a list of tuples with all currently tracked passwords
        format: [((ID, pass)), ((ID2, pass2))]
        """
        return str(self.pwds)

        ret = []
        for x in self.pwds:
            ret += ((list(self.pwds.keys())[list(self.pwds.values()).index(x)], x))

        return ret
