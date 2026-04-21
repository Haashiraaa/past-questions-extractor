

# main.py

import sys
import logging
from haashi_pkg.utility import Logger
from engine.scraper.myschool import MySchoolNGScraper
from engine.delivery.formatter import QuestionsFormatter
from engine.delivery.telegram.bot import TelegramBot
from engine.config.settings import Settings


def main(logger: Logger = Logger(level=logging.DEBUG)) -> None:

    try:
        scraper = MySchoolNGScraper(logger=logger)
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
        for subject in subjects[0:2]:
            scraper.fetch_past_questions(subject=subject, exam_year=years[0])

        for question in scraper.stored_questions:
            message = QuestionsFormatter.format_question(question)
            # logger.info(message)
            bot.send_message(message=message, question=question)

    except Exception as exc:
        logger.error(exc, exception=exc, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
