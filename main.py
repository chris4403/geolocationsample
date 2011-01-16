from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from model import Point
import geohash

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user == None:
      self.redirect(users.create_login_url(self.request.uri))
    template_values = {
      'method' : 'get',
    }
    self.response.out.write(template.render('templates/index.html', template_values))

  def post(self):
    user = users.get_current_user()
    if user == None:
      self.response.out.write()
    else :
      lat = float(self.request.get('lat'))
      lon = float(self.request.get('lon'))
      hash = geohash.encode(lat,lon)
      point = Point()
      point.geohash = hash
      point.owner   = users.get_current_user()
      point.put()
      template_values = {
        'method' : 'post',
      }
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write('{result:"OK", geohash:"' + hash + '"}')

class HistoryPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user == None:
      self.redirect(users.create_login_url(self.request.uri))
    userPoints = Point.gql("WHERE owner = :1 ORDER BY created DESC ",users.get_current_user()) 
    template_values = {
      'method' : 'get',
      'points' : userPoints
    }
    self.response.out.write(template.render('templates/history.html', template_values))

class GeohashPage(webapp.RequestHandler):
  def get(self):
    lat = float(self.request.get('lat'));
    lon = float(self.request.get('lon'));
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(geohash.encode(lat,lon))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/history', HistoryPage),
                                      ('/geohash', GeohashPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
