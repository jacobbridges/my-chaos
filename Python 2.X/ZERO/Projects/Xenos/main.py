import cgi
import wsgiref.handlers

from google.appengine.api import users      # UNUSED - admin delete commands
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db

################################################################################

class Message(db.Model):
    cat = db.IntegerProperty()  # Category
    con = db.IntegerProperty()  # Conversation
    mes = db.IntegerProperty()  # Message
    text = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

################################################################################

class Main_Page(webapp.RequestHandler):

    def get(self):
        # Write the header.
        self.response.out.write('<html><body>\n')
        # Perform the message query.
        messages = db.GqlQuery('SELECT * FROM Message ORDER BY date DESC')
        # Write them in block quotes.
        for message in messages:
            self.response.out.write('<h4>Message %s</h4>\n' % message.mes)
            text = cgi.escape(message.text)
            lines = text.replace('\n', '<br>')
            output = '<blockquote>%s</blockquote><hr>\n' % lines
            self.response.out.write(output)
        # Write the form and footer.
        self.response.out.write('''\
<form action="/write" method="post">
    <div><textarea name="content" rows="3" cols="60"></textarea></div>
    <div><input type="submit" value="Write"></div>
</form>
<a href="RESET">RESET</a>
</body></html>''')

################################################################################

class Message_Board(webapp.RequestHandler):

    def post(self):
        content = self.request.get('content')
        # Test for content existance.
        if content:
            message = Message()

            message.cat = 1                 # Category
            message.con = 1                 # Conversation

            # This is a counter for this conversation address.
            key = '%s:%s' % (message.cat, message.con)
            if memcache.get(key) is None:
                memcache.set(key, 1)
                value = 1
            else:
                value = memcache.incr(key)
            
            message.mes = value             # Message
            message.text = content
            message.put()

        self.redirect('/')

################################################################################

class Clear_Data(webapp.RequestHandler):

    def get(self):
        memcache.flush_all()
        messages = db.GqlQuery('SELECT * FROM Message')
        for message in messages:
            message.delete()
        self.redirect('/')

################################################################################

def main():
    application = webapp.WSGIApplication([('/', Main_Page),
                                          ('/write', Message_Board),
                                          ('/RESET', Clear_Data)],
                                         debug=True)
    wsgiref.handlers.CGIHandler().run(application)

################################################################################

if __name__ == '__main__':
    main()
