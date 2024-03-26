from wtforms import Form, URLField


class PodcastId(Form):
    url = URLField("URL")
