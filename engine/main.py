

# main.py

import logging
from haashi_pkg.utility import Logger
from engine.scraper import QuestionsScraper
from engine.formatter import QuestionsFormatter
from engine.telegram import TelegramBot
from engine.config.settings import Settings


def main(logger: Logger = Logger(level=logging.DEBUG)) -> None:

    scraper = QuestionsScraper()
    settings = Settings()
    bot = TelegramBot(settings=settings, logger=logger)

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
    # for subject in subjects[0:2]:
    scraper.fetch_past_questions(subject=subjects[1], exam_year=years[0])

    for question in scraper.stored_questions:
        message = QuestionsFormatter.format_question(question)
        # logger.info(message)
        # bot.send_message(message=message, question=question)


if __name__ == "__main__":
    main()
