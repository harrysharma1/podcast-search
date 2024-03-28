from wtforms import Form, StringField, URLField


class PodcastId(Form):
    url = URLField("URL")


class PodcastSearch(Form):
    search = StringField("SEARCH")
