import time, os
from libs import llm
from libs import document
from libs import scraper
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def make_news(url_arr):
  news_result = []
  for index, url in enumerate(url_arr):
    for i in range(3):
      try:
        scrape_result = scraper.get_news(url)
        news = llm.generate_news(scrape_result["news"], api_key=os.getenv("GROQ_API_KEY"))
        if scrape_result["img"] is not None:
          news["image"]["content"] = scrape_result["img"]
        else:
          news["image"]["content"] = None
        news["src"] = urlparse(url).netloc
        news_result.append(news)
        document.create_page(data=news, img=news["image"], news_length=len(url_arr), news_index=index)
        print(f"News ({index+1}/{len(url_arr)}) created: {news["title"]["content"]}")
        break
      except Exception as e:
        print(e)
        print(f"Creating news ({index+1}/{len(url_arr)}) failed. Retrying ({i+1})")
        time.sleep(0.3)
    time.sleep(0.3)
  document.create_document(news_result[0])