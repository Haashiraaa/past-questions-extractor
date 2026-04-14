

# scraper.py


import requests
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Union


questions_list: List[Dict[str, Union[str, List[str], None]]] = []

base_domain = "https://myschool.ng/"
base_url = "https://myschool.ng/classroom/physics"
params = {
    "exam_type": "waec",
    "exam_year": "2015",
    "type": "theory"
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

valid_pages: int = 0

for page in range(1, 10):

    params["page"] = str(page)
    res = requests.get(base_url, params=params, headers=headers)

    soup = BeautifulSoup(res.text, "lxml")

    questions = soup.select("div.question-item")
    if len(questions) == 0:
        print(f"Stopping at page {page} (no questions)")
        break

    valid_pages += 1

    for q in soup.select("div.question-item"):
        number_tag = q.select_one(".question_sn")
        number = number_tag.get_text(strip=True) if number_tag else None

        question_tag = q.select_one(".question-desc")
        question = (
            question_tag.get_text("\n", strip=True)
            if question_tag else None
        )

        images: List[str] = []
        if question_tag:
            imgs = question_tag.find_all("img")
            images = [
                str(img["src"]) if str(img["src"]).startswith("http")
                else base_domain + str(img["src"])
                for img in imgs
            ]

        answer_link_tag = q.select_one("a.btn-outline-danger")
        answer_link = answer_link_tag["href"] if answer_link_tag else None

        questions_list.append({
            "number": number,
            "question": question,
            "images": images,
            "answer_link": answer_link
        })


print(f"Valid pages: {valid_pages}")
print("Number of questions:", len(questions_list))
for q in questions_list:
    print(json.dumps(q, indent=4))
