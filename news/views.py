from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def scrape(request, name):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://nepalnews.com/{name}"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")

    News = soup.find_all("div", {"class": "title-news-list top-main-news-list"})

    for article in News:
        main = article.find_all("a", href=True)

        linkx = article.find("a", {"class": "title medium-title"})
        link = linkx["href"]

        titlex = article.find("h2", {"class": "home-category text-uppercase"})
        title = titlex.text

        imgx = article.find("img")["data-src"]

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.save()
    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "news/home.html", context)
