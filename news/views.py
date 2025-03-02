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

    # Updated class for the news container
    News = soup.find_all("li", {"class": "title-news-list top-main-news-list"})

    for article in News:
        # Extracting title
        titlex = article.find("h2", {"class": "title-container d-flex flex-column"}).find("a")
        title = titlex.text.strip() if titlex else "No Title"

        # Extracting link
        link = titlex["href"] if titlex else "#"

        # Extracting image
        img_tag = article.find("img")
        imgx = img_tag["src"] if img_tag else ""

        new_headline = Headline(title=title, url=link, image=imgx)
        new_headline.save()

    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "news/home.html", context)
