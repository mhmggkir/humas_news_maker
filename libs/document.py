import datetime, math
from libs import scraper
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
from html2image import Html2Image

hti = Html2Image()
document = Document()

def create_page(data, img, news_length, news_index):
  title = document.add_paragraph()
  title_format = title.paragraph_format
  title_format.space_after = Pt(0)
  title_font = title.add_run(data["title"]["content"]).font
  title_font.name = data["title"]["font"]
  title_font.size = Pt(data["title"]["size"])
  title_font.bold = data["title"]["bold"]

  quotes = document.add_paragraph()
  quotes_font = quotes.add_run(data["quotes"]["content"]).font
  quotes_font.size = Pt(data["quotes"]["size"])
  quotes_font.italic = data["quotes"]["italic"]
  quotes_font.name = data["quotes"]["font"]

  try:
    if (img == None):
      document.add_picture("./assets/placeholder.png", height=Inches(img["height"]))
    else:
      document.add_picture(img["content"], height=Inches(img["height"]))
  except:
      document.add_picture("./assets/placeholder.png", height=Inches(img["height"]))

  last_paragraph = document.paragraphs[-1]
  last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

  for p in data["paragraphs"]:
    paragraph = document.add_paragraph()
    paragraph_font = paragraph.add_run(p["content"]).font
    paragraph_font.name = p["font"]
    paragraph_font.size = Pt(p["size"])
  if news_index+1 < news_length:
    document.add_page_break()



def create_document(data, classement_list):
  section = document.sections[0]
  section.page_width = Inches(data["page"]["width"])
  section.page_height = Inches(data["page"]["height"])
  section.top_margin = Inches(data["page"]["mtop"])
  section.bottom_margin = Inches(data["page"]["mbot"])
  section.left_margin = Inches(data["page"]["mlef"])
  section.right_margin = Inches(data["page"]["mrig"])

  document.add_page_break()

  for classement in classement_list:
    scraper.get_classement(classement)
    document.add_picture("./assets/screenshot.png", width=Inches(4.3))

  datetime_now = datetime.datetime.now()
  first_weekday = datetime.datetime(year=datetime_now.year, month=datetime_now.month, day=1).weekday()

  offset_date = datetime_now.day + first_weekday - 1
  week = math.floor(offset_date/7)
  month, year = datetime_now.month, datetime_now.year
  if week == 0:
    week = 4
    month -= 1
    if month == 0:
      month = 12
      year -=1
  
  formatted_date = datetime.datetime(month=month, year=year, day=1)

  edition = f"{formatted_date.strftime("%B %Y")} ({str(week)})"
  section.footer.add_paragraph(f"Santri Update {edition}")
  
  document.save(f"sans {edition}.docx")

