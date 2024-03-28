from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask
from flask import render_template, request, redirect, render_template, request, url_for
from src.podcast_id import PodcastId
from src.podcast_id import PodcastSearch
from pytube import YouTube
from sklearn.metrics.pairwise import cosine_similarity
import math


app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
nlp = spacy.load("en_core_web_sm")


def conversion(seconds):
    seconds = float(seconds) % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    s = ("%d:%02d:%02d" % (hour, minutes, seconds))
    return s


def format_time(time: List[str]):
    formatted_time = []
    for seconds in time:
        formatted_time.append(conversion(seconds))
    return formatted_time


@app.route("/", methods=["GET", "POST"])
def index():
    form = PodcastId(request.form)
    if request.method == "POST" and form.validate():
        url = form.url.data
        return redirect(url_for("search", url=url))
    return render_template("index.html", form=form)


@app.route("/search", methods=["GET", "POST"])
def search():
    podcast_form = PodcastSearch(request.form)
    form = request.args.get("url")
    url = f"{form}"
    video_id = url.split("v=")[-1]
    transcript_dict_list = YouTubeTranscriptApi.get_transcript(
        video_id, languages=['en'])
    video = YouTube(url=url)
    video_title = video.title
    video_thumbnail = video.thumbnail_url
    text = []
    start = []
    for i in transcript_dict_list:
        text.append(i["text"])
        start.append(i["start"])

    formatted_start = format_time(start)

    for i, j in enumerate(start):
        start[i] = float(j)
        start[i] = f"{math.trunc(start[i])}"
    if request.method == "POST" and podcast_form.validate():
        search_query = podcast_form.search.data
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(text)
        query_vector = tfidf_vectorizer.transform([search_query])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
        most_similar_text_index = cosine_similarities.argmax()
        most_similar_text = text[most_similar_text_index]
        most_similar_text_timestamp_formatted = formatted_start[most_similar_text_index]
        most_similar_text_timestamp = start[most_similar_text_index]
        return render_template("result.html", most_similar_text=most_similar_text, most_similar_text_timestamp_formatted=most_similar_text_timestamp_formatted, most_similar_text_timestamp=most_similar_text_timestamp, url=url)
    return render_template("podcast_form.html", form=podcast_form, video_title=video_title, video_thumbnail=video_thumbnail, start=start, text=text, formatted_start=formatted_start, url=url)
