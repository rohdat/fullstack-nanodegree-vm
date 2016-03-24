from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import time
from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
myform = """
<form method='POST' enctype='multipart/form-data' action='/hello'>
<h2> WHAT?!</h2>
<input name='message' type='text'>
<input type='submit' value='Submit'>
</form>
"""

editForm = """
<a href='/restaurants?edit=%s'>Edit</a>
"""

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

execfile("lotsofmenus.py")

def getRestaurants():
	return session.query(Restaurant).all()

def ack(self):
	self.send_response(200)
	self.send_header('Content-type', 'text/html')
	self.end_headers()


def deleteRestaurant(self, id):
	to_delete = session.query(Restaurant).filter_by(id = id).one()
	session.delete(to_delete)
	session.commit()

def write(self, output):
	self.wfile.write(output)

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			c = 0
			print "\nset c = 0\n"
			output = ""
			output += "<html><body>"
			write(self, output)
			if self.path.endswith("/hello"):
				ack(self)
				# self.send_response(200)
				# self.send_header('Content-type', 'text/html')
				# self.end_headers()
				output += "Hello!"
				output += myform
			if self.path.endswith("/restaurants"):
				ack(self)
				# self.send_response(200)
				# self.send_header('Content-type', 'text/html')
				# self.end_headers()
				rs = None
				print "\n\t set rs = %s c = %s\n\n"%(rs, c)
				rs = getRestaurants()
				for r in rs:
					c += 1
					output += "<br>%s"%r.name
					output += editForm%r.id
			

			output += "</body></html>"
			print output
			# self.wfile.write(output)
			write(self,output)

			return

		except IOError:
			self.send_error(404, "File Not Found %s" %self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype,pdict = cgi.parse_header(self.headers.getheader('Content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')

			output = ""
			output += "<html><body>"
			output += "<h2> Olay, how abt this </h2>"
			output += "<h1> %s </h1>"%messagecontent[0]
			output += myform
			output += "</body></html>"
			self.wfile.write(output)
			print output
		except:
			pass

def main():
	port = 8080
	server = HTTPServer(('', port), webserverHandler)
	try:
		print ("Web server running on port %s"% port)
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered. Stopping web server..."
		server.socket.close()

	server.server_close()
	print "Server stopped at:", time.asctime()


if __name__ == '__main__':
	main()