from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask
from flask import render_template, request
from src.podcast_id import PodcastId
app = Flask(__name__)


nlp = spacy.load("en_core_web_sm")
# tfidf_vectorizer = TfidfVectorizer()
#  a = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
# tfidf_matrix = tfidf_vectorizer.fit_transform(a)
# print(a)


@app.route("/", methods=["GET", "POST"])
def index():
    form = PodcastId(request.form)
    if request.method == "POST" and form.validate():
        url = f"https://www.youtube.com/watch?v={form.id.data}"
        return render_template("podcast_form.html", url=url)
    return render_template("index.html", form=form)
