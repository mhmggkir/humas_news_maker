import json, time
from groq import Groq

def generate_news(news, api_key, system_prompt, news_structure, LLM):
  client = Groq(api_key=api_key)
  system_prompt += str(news_structure)
  print(system_prompt)
  model = LLM["name"]
  reasoning_support_model_list = LLM["reasoningSupportModels"]
  temperature = LLM["temperature"]
  top_p = LLM["top_p"]

  for i in range(3):
    try:
      if model in reasoning_support_model_list: generated_news = client.chat.completions.create(messages=[
            {"role": "system", "content": str(system_prompt)},
            {"role": "user", "content": news}
          ], model=model, reasoning_format="hidden", response_format={"type": "json_object"}, stream=False, temperature=temperature, top_p=top_p)
      else: generated_news = client.chat.completions.create(messages=[
            {"role": "system", "content": str(system_prompt)},
            {"role": "user", "content": news}
          ], model=model, response_format={"type": "json_object"}, stream=False, temperature=temperature, top_p=top_p)
      result = generated_news.choices[0].message.content
      return json.loads(result)
    except Exception as e:
      print(e)
      print(f"News failed to generate. Attemps: {i+1}")
      time.sleep(0.5)