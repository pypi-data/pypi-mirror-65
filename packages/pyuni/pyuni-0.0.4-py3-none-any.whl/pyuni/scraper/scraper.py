import time


class Scraper:

    def __init__(self, client, university_scraper):
        self.client = client
        self.university_scraper = university_scraper()

    def scrape(self):
        return self.university_scraper.scrape(self.client)

    def authenticate(self, username, password):
        """
        Authenticate the client against the university system
        :rtype: None
        :param username: the username or email to log in to the uni system
        :type username: str
        :param password: the password to log in to the system
        :type password: str
        """
        self.university_scraper.authenticate(self.client, username, password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.university_scraper.end_session(self.client)
        time.sleep(3)
