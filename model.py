from google.appengine.ext import db

class Point(db.Model):
    owner   = db.UserProperty()
    geohash = db.StringProperty(multiline=False)
    created = db.DateTimeProperty(auto_now_add=True)
