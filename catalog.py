import urllib.parse as urlparse
from collections import namedtuple
import re
from bs4 import BeautifulSoup

import course


OPENU_CATALOG_URL_BASE = 'https://www3.openu.ac.il'
COURSE_NAME_PARTS_PATTERN = re.compile(r'(.+)\s\((\d+)\)')


def get_courses_from_page(page_contents):
    soup = BeautifulSoup(page_contents, "html.parser")

    table = soup.find('table', class_='table1')
    if not table:
        return []

    rows = soup.css.select('.table1 tr')
    if len(rows) < 1:
        return []

    courses_data = []
    for row in rows[1::]:
        data = row.select('td')

        # First cell = course name and link
        course_name_and_link = data[0].select('a', class_='links')[0]
        course_full_name = course_name_and_link.text

        course_name, course_number = COURSE_NAME_PARTS_PATTERN.match(
            course_full_name).groups()

        course_link = urlparse.urljoin(
            OPENU_CATALOG_URL_BASE, course_name_and_link['href'])

        # Second cell = level
        # Can be multiple levels, so if it is, split it
        level = data[1].text.strip()

        # Third cell = credits
        credits = data[2].text.strip()

        # Fourth cell = is available abroad
        is_abroad = data[3].text.strip() == '+'

        # Fifth cell = semesters
        semesters = data[4]
        print(data[4].text.strip())

        course_data = course.Course(
            course_number, course_name, credits, is_abroad, semesters)
        courses_data.append(course_data)

    return courses_data
