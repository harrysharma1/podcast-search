from typing import List
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


def convert_time(time: List[str]):
    for seconds in time:
        hour  = int(time)/3600
        print(hour)

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
        return render_template("podcast_form.html", video_title=video_title, video_thumbnail=video_thumbnail, text=text, start=start)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
