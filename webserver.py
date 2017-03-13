#https://open.fda.gov/
#self.path es mi url
#ul=unlimited list
#https://github.com/tylucaskelley/licenser/blob/master/LICENSE

#MIT License

#Copyright (c) 2017 Sandra Montejano <nsand77@hotmail.com>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

    #Contact GitHub API Training Shop Blog About


import http.server
import http.client
import json
# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	OPENFDA_API_URL='api.fda.gov'
	OPENFDA_API_EVENT='/drug/event.json'


	def get_main_page(self):
		html='''
	    <html>
	    <head>
	        <title> OpenFDA Cool App</title>
	    </head>
	    <body>
	        <h1>OpenFDA Client</h1>
	        <form method="get" action="recieve">
	            <input type="submit" value="Drug List: Send to OpenFDA">
	            </input>
	        </form>
            <form method="get" action="search">
				<input typye="text" name="drug"></input>
                <input type="submit" value="Drug Search LYRICA: Send to OpendFDA">
            </form>
	    </body>
	    </html>
	    '''
		return html


	def get_drugs_from_events(self, events):
		drugs=[]
		for event in events:
			drugs+=[event['patient']['drug'][0]['medicinalproduct']]
			#lista_str= ",".join(lista) #Para transformarlo en string
		return drugs

	def get_list_html(self,drugs): #html con las 10 drugs
		drugs_html='''
		<html>
			<head>
				<title> OpenFDA Cool App</title>
				</head>
			<body>
				<ul>
			'''
		for drug in drugs:
			drugs_html+="<li>"+drug+"</li>\n"
		drugs_html+= '''
				</ul>
			</body>
		</html>
		'''
		return drugs_html


    # GET EVENT
	def get_events(self):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #Te conectas
		conn.request('GET',self.OPENFDA_API_EVENT +'?limit=10') #Dices que te coja los eventos
		r1 = conn.getresponse() #Obtienes los eventos (respuesta)
		data1 = r1.read() #lee los datos r1
		events = data1.decode("utf8") #lo descodifica, formato json
		return events

	def get_any_drug(self,drug):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request('GET',self.OPENFDA_API_EVENT +'?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
		r1 = conn.getresponse()
		data1 = r1.read()
		events = data1.decode("utf8")
		return events

	def get_companies_from_events(self,events):
		companies=[]
		for event in events:
			companies+=[event['companynumb']]
		return companies


    # GET
	def do_GET(self):
		main_page=False
		is_event=False
		is_search=False


		if self.path=='/':
			main_page=True
		elif self.path=="/recieve" or self.path=="/recieve?":
			is_event=True
		elif "/search?" in self.path:
			is_search=True

        #print(self.path) con esto elegimos entre evento o html
        # Send response status code
		self.send_response(200)

        # Send headers
		self.send_header('Content-type','text/html')
		self.end_headers()

        # Send message back to client
		html=self.get_main_page()

        #event=event1
		if main_page:
			self.wfile.write(bytes(html, "utf8"))
		elif is_event:
			events_str=self.get_events()
			events=json.loads(events_str)
			events=events["results"]
			drugs=self.get_drugs_from_events(events)
			html=self.get_list_html(drugs)
			#for i in range(len(events)):
			#	print (events[i])
			self.wfile.write(bytes(html, "utf8"))

		elif is_search:
			drug=self.path.split("=")[1]
			drugs=self.get_any_drug(drug)
			events=json.loads(drugs)
			events=events["results"]
			search=self.get_companies_from_events(events)
			html=self.get_list_html(search)
			self.wfile.write(bytes(html, "utf8"))
