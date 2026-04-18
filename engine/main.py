

# main.py

import logging
from haashi_pkg.utility import Logger
from engine.scraper import QuestionsScraper
from engine.formatter import QuestionsFormatter


def main(logger: Logger = Logger(level=logging.INFO)) -> None:

    scraper = QuestionsScraper()

    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    subjects = [
        "English Language",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Computer Studies",
        "Further Mathematics",
        "Civic Education",
        "Economics",
        "Biology"
    ]

    subjects = ["-".join(sub.split()).lower() for sub in subjects]

    # for year in years:
    for subject in subjects[0:2]:
        scraper.fetch_past_questions(subject=subject, exam_year=years[0])

    for question in scraper.stored_questions:
        print(QuestionsFormatter.format_question(question))


if __name__ == "__main__":
    main()
