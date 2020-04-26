from PIL import Image
import requests


url = 'https://m.media-amazon.com/images/G/01/imdb/images/nopicture/medium/film-3385785534._CB468454186_.png'

response = requests.get(url)
         # Opening Inage file using PIL Image
with open('test.png','wb') as img:
    img.write(response.content)

with open('test.png','rb') as img:
    print(img.read())



