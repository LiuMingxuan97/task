import requests
import openai
openai.api_key =  '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'


response = openai.Image.create(
  prompt="A six-month-old kitten with silver creamings wore a pearl necklace around her neck ",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)
