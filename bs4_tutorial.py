import requests
from bs4 import BeautifulSoup

url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text

image = soup.find('img', class_='attachment-post-image')['src']

post_tag = soup.find('main').find('article').find('div')
post_text = post_tag.text

print(title_text)
print()
print(image)
print()
print(post_text)