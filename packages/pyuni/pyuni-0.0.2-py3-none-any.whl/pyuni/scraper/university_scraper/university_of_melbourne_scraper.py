import os
import time

from .university_scraper import UniversityScraper, UniversityFactory
from pyuni.objects.subject import Subject, SubjectSession
from pyuni.exceptions import AuthenticationError


class UniversityOfMelbourneFactory(UniversityFactory):
    line_separator = '\n'
    content_separator = '\t'
    identifier_separator = '_'

    @classmethod
    def create_subjects(cls, content):
        content = content.strip().split(cls.line_separator)
        content = [entry.split(cls.content_separator) for entry in content[1:]]

        subjects = []

        for entry in content:
            # remove all the empty elements from entry
            entry = [i for i in entry if i]

            subject_identifier = entry[0].split(cls.identifier_separator)

            subject_code = subject_identifier[0]
            subject_session = subject_identifier[-1]
            subject_name = entry[1]

            subject = Subject(code=subject_code, period=subject_session, name=subject_name, sessions=[])

            if subject not in subjects:
                subjects.append(subject)
            else:
                for s in subjects:
                    subject = s

            # add the new timetable
            entry_type = entry[2]
            entry_date = f'{entry[5]} {entry[4]}'
            entry_identifier = entry[3]
            session_location = entry[7]
            session = SubjectSession(code=entry_identifier, date=entry_date,
                                     form=entry_type, location=session_location)

            subject.add_session(session)

        return subjects

    @classmethod
    def create_profile(cls, content):
        raise NotImplementedError()

    @classmethod
    def parse_day(cls, day):
        if day == 'Mon':
            return 'Monday'
        elif day == 'Tue':
            return 'Tuesday'
        elif day == "Wed":
            return 'Wednesday'
        elif day == 'Thu':
            return 'Thursday'
        elif day == 'Fri':
            return 'Friday'
        elif day == 'Sat':
            return 'Saturday'
        elif day == 'Sun':
            return 'Sunday'


class UniversityOfMelbourneScraper(UniversityScraper):
    factory = UniversityOfMelbourneFactory

    login_url = 'https://mytimetable.students.unimelb.edu.au/even/student'
    login_success_url = 'https://mytimetable.students.unimelb.edu.au/even/student?ss='

    urls = {
        'homepage': 'https://mytimetable.students.unimelb.edu.au/even/student'
    }

    element_selectors = {
        'username_input': '#usernameInput',
        'password_input': '#passwordInput',
        'login_button': '.page-inner form button[type="submit"]',
        'timetable_anchor_menu': 'a[href="#timetable"]',
        'download_button': '#timetable-tpl #download_dropdown',
        'excel_download_button': '#download_dropdown.desktop-only ul li:nth-child(3)',
        'logout_button': '.top-menu li:last-child'
    }

    @classmethod
    def authenticate(cls, client, username, password):
        client.get(cls.login_url)

        username_input = client.find_element_by_css_selector(cls.element_selectors['username_input'])
        password_input = client.find_element_by_css_selector(cls.element_selectors['password_input'])
        login_button = client.find_element_by_css_selector(cls.element_selectors['login_button'])

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        if cls.login_success_url not in client.current_url:
            raise AuthenticationError()

    @classmethod
    def scrape(cls, client):
        cls.go_to_timetable_page(client)

        timetable_filepath = cls.download_timetable(client)
        with open(timetable_filepath, 'r') as f:
            subjects = cls.factory.create_subjects(f.read())
            return subjects

    @classmethod
    def go_to_timetable_page(cls, client):
        client.get(cls.urls['homepage'])
        client.find_element_by_css_selector(cls.element_selectors['timetable_anchor_menu']).click()

    @classmethod
    def download_timetable(cls, client):
        client.find_element_by_css_selector(cls.element_selectors['download_button']).click()
        client.find_element_by_css_selector(cls.element_selectors['excel_download_button']).click()

        # wait for the file to be downloaded
        time.sleep(5)

        filename = os.listdir(client.download_dir_path)[0]
        filepath = os.path.join(client.download_dir_path, filename)

        return filepath

    @classmethod
    def end_session(cls, client):
        client.find_element_by_css_selector(cls.element_selectors['logout_button']).click()
