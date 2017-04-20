#https://open.fda.gov/
#self.path es mi url
#ul=unlimited list
#https://github.com/tylucaskelley/licenser/blob/master/LICENSE
#accion parecida a recieve: atribute

import http.server
import http.client
import json
# HTTPRequestHandler class
class OpenFDAClient():
	OPENFDA_API_URL='api.fda.gov'
	OPENFDA_API_EVENT='/drug/event.json'

	def get_events(self,limit):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #Te conectas
		conn.request('GET',self.OPENFDA_API_EVENT +'?limit=' +limit) #Dices que te coja los eventos
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

class OpenFDAParser():

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

	def get_patient_sex(self,events):
		sex=[]
		for event in events:
			sex=sex+[event['patient']['patientsex']]
		return sex

class OpenFDAHTML():

	def get_main_page(self):
		html='''
	    <html>
	    <head>
	        <title> OpenFDA Cool App</title>
	    </head>
	    <body>
	        <h1>OpenFDA Client</h1>
			<body> Escriba el numero de eventos </body>
			<form method="get" action="listCompanies">
				<input type="text" size="3" name="limit">
				<input type="submit" value="Company List: Send to OpenFDA">
				</input>
			</form>
			<body> Escriba el numero de eventos </body>
	        <form method="get" action="listDrugs">
				<input type="text" size="3" name="limit">
	            <input type="submit" value="Drug List: Send to OpenFDA">
	            </input>
	        </form>
			<body> Escribe el numero de eventos </body>
			<form method="get" action="listGender">
				<input type="text" size="3" name="limit">
				<input type="submit" value="Gender report: Send to OpenFDA">
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
            </form>
	    </body>
	    </html>
	    '''
		return html

	def get_list_html(self,drugs):
		drugs_html='''
		<html>
			<head>
				<title>OpenFDA Cool App</title>
			</head>
			<body>
				<ol>
		'''
		for drug in drugs:
			drugs_html+="<li>"+drug+"</li>"
		drugs_html+= '''
				</ol>
			</body>
		</html>
		'''
		return drugs_html

	def get_html_error(self):
		error_html='''
		<html>
			<head>
				<title>OpenFDA Cool App</title>
			</head>
			<body>
			<h1>Error 404: Not Found</h1>
			</body>
			<body>No se ha encontrado esta URL</body>
		</html>
		'''
		return error_html

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		#Clases
		client=OpenFDAClient()
		parser=OpenFDAParser()
		HTML=OpenFDAHTML()
		response=200
		header1='Content-type'
		header2='text/html'

		if self.path=='/':
			html=HTML.get_main_page()

		elif "/listDrugs" in self.path:
			limit=self.path.split("=")[1]
			events_str=client.get_events(limit)
			events=json.loads(events_str)
			events=events["results"]
			drugs=parser.get_drugs_from_events(events)
			html=HTML.get_list_html(drugs)


		elif "/listCompanies" in self.path :
			limit=self.path.split("=")[1]
			events_str=client.get_events(limit)
			events=json.loads(events_str)
			events=events["results"]
			companies=parser.get_companies_from_events(events)
			html=HTML.get_list_html(companies)


		elif "/listGender" in self.path:
			limit=self.path.split("=")[1]
			events_str=client.get_events(limit)
			events=json.loads(events_str)
			events=events["results"]
			gender=parser.get_patient_sex(events)
			html=HTML.get_list_html(gender)


		elif "/searchCompany" in self.path:
			company=self.path.split("=")[1]
			event_str=client.get_any_company(company)
			events=json.loads(event_str)
			events=events["results"]
			search=parser.get_drugs_from_events(events)
			html=HTML.get_list_html(search)


		elif "/searchDrug" in self.path:
			drug=self.path.split("=")[1]
			drugs=client.get_any_drug(drug)
			events=json.loads(drugs)
			events=events["results"]
			search=parser.get_companies_from_events(events)
			html=HTML.get_list_html(search)

		elif "/redirect" in self.path:
			response=302
			header1='Location'
			header2='http://localhost:8000'

		elif "/secret" in self.path:
			response=401
			header1='WWW-Authenticate'
			header2='Basic realm = "My Realm"'


		else:
			response=404
			html=HTML.get_html_error()
#'?search=patient.drug.medicinalproduct:'
		self.send_response(response)

		self.send_header(header1,header2)
		self.end_headers()

		if response==200 or response==404:
			self.wfile.write(bytes(html, "utf8"))
