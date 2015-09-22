from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import cgi
import re
## import CRUD operations from lesson 1 ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				#print output
				return

			if self.path.endswith("/hola"):
                                self.send_response(200)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()

                                output = ""
                                output += "<html><body>&#161Hola   <a href = '/hello'>Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                                output += "</body></html>"
				self.wfile.write(output)
                                #print output
                                return
			if self.path.endswith("/restaurants"):
				rests = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Make a New Restaurant Here</a></br></br>"
				for rest in rests:
					output += rest.name
					output += "</br>"
					output += '<a href="/restaurants/%s/edit">Edit</a></br>' % rest.id
					output += '<a href="/restaurants/%s/delete">Delete</a></br></br>' % rest.id
				output += "</body></html>"
				self.wfile.write(output)
				#print output
				return
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='restname' type='text'><input type='submit' value='Create'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				return
			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
                                self.end_headers()
				paths = self.path.split('/')
				restid = paths[2]
				rest= session.query(Restaurant).get(restid)
				if rest != []:
					output = ""
					output += "<html><body>"
					output += "<h1>%s</h1>" % rest.name
					output += "<form method='POST' enctype='multipart/form-data' action='"
					output+= self.path
					output+= "'><input name='restname' type='text'><input type='submit' value='Rename'></form>"
					output += "</body></html>"
					print output
					self.wfile.write(output)		
				return
			if self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				restid= self.path.split('/')[2]
				rest = session.query(Restaurant).get(restid)
				if rest != []:
					output = ""
					output += "<html><body>"
					output += "<h2>Are you sure you want to delete: </br>%s</h2>" % rest.name
					output += '<form method="POST" enctype="multipart/form-data" action="%s"><input type="submit" value="Delete"></form>' %self.path
					output += "</body></html>"
					self.wfile.write(output)
				return
		except:
			self.send_error(404, "File Not Found %s" % self.path)
	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
	                        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
	                        if ctype == 'multipart/form-data':
	                                fields=cgi.parse_multipart(self.rfile, pdict)
	                        restname = fields.get('restname')
				
				newrest= Restaurant(name = restname[0])
				session.add(newrest)
				session.commit()
				print "Whoops! Rests"	
                                #print output
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return 
			if self.path.endswith('/edit'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                                if ctype == 'multipart/form-data':
                                        fields=cgi.parse_multipart(self.rfile, pdict)
                                restname = fields.get('restname')
                                
				paths = self.path.split('/')
                                restid = paths[2]
				
				rest= session.query(Restaurant).get(restid)
                                #UPDATE rest with new name!!!!!
				if rest != []:		
					print rest.name	
					newrestname=  restname[0]
					rest.name = newrestname
					session.commit()

                                	#print output
                                	self.send_response(301)
                                	self.send_header('Content-type', 'text/html')
                                	self.send_header('Location', '/restaurants')
                                	self.end_headers()
				return
			if self.path.endswith('/delete'):
				paths = self.path.split('/')
                                restid = paths[2]
				rest= session.query(Restaurant).get(restid)
                                #UPDATE rest with new name!!!!!
                                if rest != []:
					session.delete(rest)
					session.commit()
				self.send_response(301)
                                self.send_header('Content-type', 'text/html')
                                self.send_header('Location', '/restaurants')
                                self.end_headers()
			return
			#self.send_response(301)
			#self.end_headers()

			#ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			#if ctype == 'multipart/form-data':
			#	fields=cgi.parse_multipart(self.rfile, pdict)
			#messagecontent = fields.get('message')

			#output = ""
			#output += "<html><body>"
			#output += "<h2> Okay, how about this: </h2>"
			#output += "</h1> %s </h1>" % messagecontent[0]

			#output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
			#output += "</body></html>"
			#self.wfile.write(output)
			#print output
			
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()
