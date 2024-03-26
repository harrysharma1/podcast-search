from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer 
from flask import Flask
from flask import render_template 
app = Flask(__name__)

video_id = "a87Tb27UE4Y"
nlp = spacy.load("en_core_web_sm")

#tfidf_vectorizer = TfidfVectorizer()
a = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])
#tfidf_matrix = tfidf_vectorizer.fit_transform(a)
print(a)
for i in a:
    pass



@app.route("/")
def hello_world():
    return render_template("index.html")
