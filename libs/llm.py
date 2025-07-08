import json, time
from groq import Groq


news_structure = {"src": "", "page": {"width": 8.27, "height": 11.69, "mtop": 0.5, "mbot": 0.5, "mlef": 0.5, "mrig": 0.5}, "title": {"font": "Times New Roman", "size": 22, "bold": True, "content": ""}, "quotes": {"font": "Times New Roman", "size": 10, "italic": True, "content": ""}, "image": {"height": 2.36, "content": ""}, "paragraphs": [{"font": "Times New Roman", "size": 11, "content": ""}]}

system_prompt = f"Buat berita yang di kirimkan oleh user menjadi berita yang menarik dan bermodel paragraf, gunakan format json di setiap style font, gunakan struktur seperti berikut {str(news_structure)}, pastikan isi berita dapat pas pada ukuran kertas yang diberikan (Inch), ukuran font (pt), gunakan bahasa Indonesia, jika berita yang diberikan oleh user kosong maka tuliskan gagal di setiap content, berikan dateline di awal berita yang mengandung tempat dan sumber berita, jangan berikan tulisan copyright, buat 6 paragraf, buat masing masing paragraf berisi 5 baris, gunakan gaya bahasa seperti artikel ilmiah populer"

def generate_news(news, api_key):
  client = Groq(api_key=api_key)
  for i in range(3):
    try:
      generated_news = client.chat.completions.create(messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": news}
      ], model="deepseek-r1-distill-llama-70b", reasoning_format="parsed", response_format={"type": "json_object"}, stream=False)
      result = generated_news.choices[0].message.content
      return json.loads(result)
    except Exception as e:
      print(f"News failed to generate. Attemps: {i+1}")
      time.sleep(0.5)