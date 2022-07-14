import requests
import bs4

from _class import Class


def get_classes(term: str, subject: str, catalog_nbr: str) -> list[Class]:
    session = requests.session()

    # CSRFToken is required in order to post data
    res = session.get(url="https://psmobile.pitt.edu/app/catalog/classSearch/2231")
    csrf = res.cookies.get("CSRFCookie")

    res = session.post(
        url="https://psmobile.pitt.edu/app/catalog/getClassSearch",
        data={
            "CSRFToken": csrf,
            "term": term,
            "campus": "PIT",
            "subject": subject,
            "catalog_nbr": catalog_nbr,
        },
    )
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    name = soup.find("div", {"class": "secondary-head"}).text

    # Go through each class from HTML and create a Class object with the respective values
    classes = []
    htmlClasses = soup.find_all("a", {"class": "list-item__link"})
    for htmlClass in htmlClasses:
        data = htmlClass.find("div", {"class": "section-content"}).attrs
        secondaryData = htmlClass.find_all("div", {"class": "section-body"})
        room = secondaryData[3].text.split(": ")[1]
        instructor = secondaryData[4].text.split(": ")[1]
        c = Class(
            name=name,
            days=data["data-days"],
            start=float(data["data-start"]),
            end=float(data["data-end"]),
            room=room,
            instructor=instructor,
        )
        classes.append(c)

    return classes


if __name__ == "__main__":
    term = "2231"  # Fall Term 2022-2023
    subject = "MATH"
    catalog_nbr = "0220"
    classes = get_classes(term, subject, catalog_nbr)
    print(len(classes))
