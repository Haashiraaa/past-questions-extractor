

# telegram.py

import re
import logging
import requests
from typing import Optional, Dict, Union, cast, List
from haashi_pkg.utility import Logger
from engine.config.settings import Settings
from engine.aliases import QuestionLike
from engine.table_renderer import render_table
from io import BytesIO


class TelegramBot:

    def __init__(
        self,
        settings: Optional[Settings] = None,
        logger: Optional[Logger] = None
    ) -> None:

        self.settings = settings or Settings()
        self.logger = logger or Logger(level=logging.INFO)
        self.bot_token = cast(str, self.settings.TG_BOT_TOKEN)
        self.chat_id = cast(str, self.settings.TG_CHAT_ID)

        self.msg_url = (
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        )
        self.img_url = (
            f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
        )

    def _escape_markdownv2(self, text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!\\'
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

    def _send_message_without_image(self, message: str) -> None:

        payload: Dict[str, Union[str, None]] = {
            "chat_id": self.chat_id,
            "text": self._escape_markdownv2(message),
            "parse_mode": "MarkdownV2"
        }

        try:
            response = requests.post(self.msg_url, data=payload)
            self.logger.debug(f"Status: {response.status_code}")
            self.logger.debug(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send message: {e}")

    def _send_message_with_image(
        self,
        message: str,
        question: QuestionLike,
    ) -> None:

        payload: Dict[str, Union[str, None, List[str]]] = {
            "chat_id": self.chat_id,
            "photo": question.get("image"),  # scraped image URL
            "text": self._escape_markdownv2(message),
            "parse_mode": "MarkdownV2"
        }

        try:
            response = requests.post(self.img_url, data=payload)
            self.logger.debug(f"Status: {response.status_code}")
            self.logger.debug(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send message: {e}")

    def _send_table(self, question: QuestionLike) -> None:

        table = render_table(cast(List[List[str]], question.get("table")))
        payload: Dict[str, Union[str, BytesIO]] = {
            "chat_id": self.chat_id,
            "photo": table
        }

        try:
            response = requests.post(self.img_url, data=payload)
            self.logger.debug(f"Status: {response.status_code}")
            self.logger.debug(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send message: {e}")

    def send_message(self, message: str, question: QuestionLike) -> None:

        if question.get("table"):
            self._send_table(question)

        if question.get("image"):
            self._send_message_with_image(message, question)
        else:
            self._send_message_without_image(message)
