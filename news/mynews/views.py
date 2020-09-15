from django.shortcuts import render, redirect
from .models import Headline
import requests
from bs4 import BeautifulSoup as BSoup
# Create your views here.

def home(request):
    return render(request, "base.html")




def scrape(request):
  session = requests.Session()
  Headline.objects.all().delete()
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  url = "https://www.theonion.com/"

  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}


  toi_r = requests.get("https://www.nytimes.com/trending/", headers=headers)
  toi_soup = BSoup(toi_r.content, 'html.parser')

  nt_link = toi_soup.find_all('img', {"class":"css-8atqhb"})
  image_link= []

  for post in nt_link:
    image_link.append(post.get('src'))


  image_link = image_link[1:]
  nt_desc = toi_soup.find_all('h1')
  desc_mat = []

  for post in nt_desc:
      desc_mat.append(str(post)[4:][:-5])

  desc_mat =  desc_mat[1:-1]


  nt_link = toi_soup.find_all('li', {"class":"css-1iski2w"})
  link = []

  for post in nt_link:
      link.append(post.a.get('href'))




  for i in range(len(link)):
      new_headline = Headline()

      print(image_link[i])
      print(desc_mat[i])
      print(link[i])
      new_headline.title = desc_mat[i]
      new_headline.url = link[i]
      new_headline.image = image_link[i]
      new_headline.save()




  return redirect("..")



def news_list(request):
    print(Headline.objects.all())
    headlines = Headline.objects.all()[::-1]

    context = {
        'object_list': headlines,
    }
    return render(request, "base.html", context)