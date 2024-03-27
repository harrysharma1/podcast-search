from typing import List
from numpy import float_
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask
from flask import render_template, request
from src.podcast_id import PodcastId
from pytube import YouTube

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

nlp = spacy.load("en_core_web_sm")
# tfidf_vectorizer = TfidfVectorizer()
#  a = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
# tfidf_matrix = tfidf_vectorizer.fit_transform(a)
# print(a)


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
        url = f"{form.url.data}"
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
        start = format_time(start)
        return render_template("podcast_form.html", video_title=video_title, video_thumbnail=video_thumbnail, text=text, start=start)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
