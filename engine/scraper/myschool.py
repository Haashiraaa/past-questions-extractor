

# myschool.py

import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple, cast
from datetime import datetime
from haashi_pkg.utility import Logger
from engine.subjects import Subjects
from engine.models.aliases import QuestionLike


class MySchoolNGScraper:

    def __init__(self, logger: Optional[Logger] = None) -> None:

        self.logger = logger or Logger(level=logging.INFO)
        self.base_domain: str = "https://myschool.ng"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.stored_questions: List[QuestionLike] = []

    def _validate(
        self,
        subject: str,
        exam_year: str,
        exam_type: str,
        question_type: str
    ) -> Tuple[str, ...]:

        if not any([subject, exam_type, exam_year, question_type]):
            raise ValueError(
                "Subject, exam type, exam year and question type are required"
            )

        if not any(
            valid_sub == subject.lower()
            for valid_sub in Subjects.valid_subjects
        ):
            raise ValueError(f"Invalid subject: {subject}!")

        if question_type.lower() not in [
            "all", "theory", "practical", "objective"
        ]:
            raise ValueError(
                f"Invalid question type: {question_type}!"
            )

        if exam_type.lower() not in ["all", "jamb", "waec", "neco"]:
            raise ValueError(
                f"Invalid exam type: {exam_type}!"
            )

        try:
            current_year = datetime.now().year
            if int(exam_year) < 1989 or int(exam_year) > current_year:
                raise ValueError(
                    f"Invalid exam year: {exam_year}! "
                    f"Exam year must be between 1989 and {current_year}"
                )
        except TypeError:
            raise TypeError(f"Invalid year input: {exam_year}!")

        except Exception as e:
            raise Exception(f"Error: {e}")

        return subject, exam_year, exam_type, question_type

    def fetch_past_questions(
        self,
        subject: str,
        exam_year: str,
        exam_type: str = "waec",
        question_type: str = "theory"
    ) -> None:

        subject, exam_year, exam_type, question_type = self._validate(
            subject=subject,
            exam_year=exam_year,
            exam_type=exam_type,
            question_type=question_type
        )

        base_url = f"{self.base_domain}/classroom/{subject}"
        params = {
            "exam_type": f"{exam_type}",
            "exam_year": f"{exam_year}",
            "type": f"{question_type}",
        }

        valid_pages: int = 0

        for page in range(1, 10):

            params["page"] = str(page)

            try:
                res = requests.get(
                    base_url, params=params, headers=self.headers
                )
                res.raise_for_status()
                self.logger.debug(f"Response: {res.status_code}")

            except requests.exceptions.Timeout as e:
                self.logger.error(
                    f"Request timeout - site may be down: {e}"
                )
                self.logger.error(exception=e, save_to_json=True)
                raise

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to fetch page: {e}")
                self.logger.error(exception=e, save_to_json=True)
                raise

            soup = BeautifulSoup(res.text, "lxml")

            questions = soup.select("div.question-item")
            if len(questions) == 0:
                self.logger.info(f"Stopping at page {page} (no questions)")
                self.logger.info(f"Last known valid page: page {valid_pages}")
                break

            valid_pages += 1

            for q in soup.select("div.question-item"):
                number_tag = q.select_one(".question_sn")
                number = number_tag.get_text(
                    strip=True) if number_tag else None

                question_tag = q.select_one(".question-desc")
                question = (
                    question_tag.get_text("\n", strip=True)
                    if question_tag else None
                )

                images: List[Optional[str]] = []
                if question_tag:
                    imgs = question_tag.find_all("img")
                    images = [
                        str(img["src"])
                        if str(img["src"]).startswith("http")
                        else self.base_domain + str(img["src"])
                        for img in imgs
                    ]

                answer_link_tag = q.select_one("a.btn-outline-danger")
                answer_link = answer_link_tag["href"] if answer_link_tag else None

                self.stored_questions.append({
                    "exam_year": exam_year,
                    "subject": subject,
                    "number": number,
                    "question": question,
                    "images": images,
                    "answer_link": cast(Optional[str], answer_link)
                })
