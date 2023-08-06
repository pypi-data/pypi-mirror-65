class Subject:

    def __init__(self, name, code, period, sessions):
        self.name = name
        self.code = code
        self.period = period
        self.sessions = sessions

    def add_session(self, session):
        self.sessions.append(session)

    def __eq__(self, other):
        return self.name == other.name and self.code == other.code and self.period == other.period

    def __repr__(self):
        return f'{self.code} - {self.name} - {self.period}'


class SubjectSession:

    def __init__(self, code, form, date, location):
        self.code = code
        self.form = form
        self.date = date
        self.location = location

    def __repr__(self):
        return f'{self.code} - {self.form} - {self.date}'
