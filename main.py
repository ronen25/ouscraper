import requests

import catalog

CATALOG_URL = '''https://www3.openu.ac.il/ouweb/owal/catalog.sknum?v_last={}'''


def main():

    # page = requests.get(CATALOG_URL.format('1'))

    with open('tests/page1.html', encoding='windows-1255') as f:
        page = f.read()

    courses = catalog.get_courses_from_page(page)

    print(courses)


if __name__ == '__main__':
    main()
