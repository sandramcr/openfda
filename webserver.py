#https://open.fda.gov/
#self.path es mi url
#ul=unlimited list
#https://github.com/tylucaskelley/licenser/blob/master/LICENSE
#accion parecida a recieve: atribute

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
			</form>
			<form method="get" action="listCompanies">
				<input type="submit" value="Company List: Send to OpenFDA">
				</input>
			</form>
	        <form method="get" action="listDrugs">
	            <input type="submit" value="Drug List: Send to OpenFDA">
	            </input>
	        </form>
			<form method="get" action="searchCompany">
				<input type="text" name="company">
				</input>
				<input type="submit" value="Company Search:Send to OpenFDA">
				</input>
			</form>
            <form method="get" action="searchDrug">
				<input type="text" name="drug">
				</input>
                <input type="submit" value="Drug Search: Send to OpendFDA">
				</input>
	    </body>
	    </html>
	    '''
		return html


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
			drugs_html+="<li>"+drug+"</li>"
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
		conn.request('GET',self.OPENFDA_API_EVENT +'?search='+drug+'&limit=10')
		r1 = conn.getresponse()
		data1 = r1.read()
		events = data1.decode("utf8")
		return events

	def get_any_company(self,company):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request('GET',self.OPENFDA_API_EVENT +'?search='+company+'&limit=10')
		r1 = conn.getresponse()
		data1 = r1.read()
		events = data1.decode("utf8")
		return events

	def get_companies_from_events(self,events):
		companies=[]
		for event in events:
			companies=companies+[event['companynumb']]
		return companies

	def get_drugs_from_events(self, events):
		drugs=[]
		for event in events:
			drugs=drugs+[event['patient']['drug'][0]['medicinalproduct']]
			#lista_str= ",".join(lista) #Para transformarlo en string
		return drugs


	#def get_company_list(self,events):
		#company=[]
		#for event in events:
			#company+=[event['companynumb']]
		#return company

    # GET
	def do_GET(self):
		main_page=False
		drug_event=False
		search_drugs=False
		search_company=False
		company_event=False

		if self.path=='/':
			main_page=True
		elif self.path=="/listCompanies" in self.path :
			company_event=True
		elif self.path=="/listDrugs" in self.path:
			drug_event=True
		elif "/searchDrug" in self.path:
			search_drugs=True
		elif "/searchCompany" in self.path:
			search_company=True
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

		elif drug_event:
			events_str=self.get_events()
			events=json.loads(events_str)
			events=events["results"]
			drugs=self.get_drugs_from_events(events)
			html=self.get_list_html(drugs)
			self.wfile.write(bytes(html, "utf8"))
			#for i in range(len(events)):
			#	print (events[i])

		elif company_event:
			events_str=self.get_events()
			events=json.loads(events_str)
			events=events["results"]
			companies=self.get_companies_from_events(events)
			html=self.get_list_html(companies)
			self.wfile.write(bytes(html, "utf8"))

		elif search_company:
			company=self.path.split("=")[1]
			event_str=self.get_any_company(company)
			events=json.loads(event_str)
			events=events["results"]
			search=self.get_drugs_from_events(events)
			html=self.get_list_html(search)
			self.wfile.write(bytes(html, "utf8"))

		elif search_drugs:
			drug=self.path.split("=")[1]
			drugs=self.get_any_drug(drug)
			events=json.loads(drugs)
			events=events["results"]
			search=self.get_companies_from_events(events)
			html=self.get_list_html(search)
			self.wfile.write(bytes(html, "utf8"))
