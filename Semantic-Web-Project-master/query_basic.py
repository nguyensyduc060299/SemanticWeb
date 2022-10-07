import logging
from pickle import GET
import rdflib
from flask import Flask, request
app = Flask(__name__)
import json
logging.basicConfig()

# creating the graph
g=rdflib.Graph()
result=g.parse("result_dbpedia.owl", "xml")
print("graph has %s statements.\n" % len(g))
def query_country(country):
    # movies filmed in United Kingdom
    query1 = """
    PREFIX movie: <http://www.semanticweb.org/duc.nguyensy10/ontologies/2022/8/untitled-ontology-21#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
    SELECT ?name ?duration  ?country ?moviedes
    WHERE { ?film rdf:type movie:Movie .
            ?film movie:movieName ?name .
            ?film movie:durationSeconds ?duration .
            ?film movie:movieDescription ?moviedes .
            ?film movie:filmedIn ?country .
            FILTER regex(str(?country), "Country")
        }
    """.replace("\"Country\"", "\""+ country+"\"")
    # ?film movie:producedBy ?producer_movie .
            # ?producer rdf:type movie:Producer .
            # ?language rdf:type movie:Language .
    # querying and displaying the results
    results = g.query(query1)
    dict_rs = []
    def process_country(country):
        rs = " ".join(country.split("/")[-1].split("_"))
        return rs

    def process_duration(duration):
        rs = float(duration.split("^^")[0].replace("\"",""))
        return rs
    for rs in results:
        mv = rs.asdict()
        movie = {
            'name': mv['name'].toPython(),
            'duration': process_duration(mv['duration'].toPython().n3()),
            'country': process_country(mv['country'].toPython()),
            'description': mv['moviedes'].toPython()
        }
        dict_rs.append(movie)
    return dict_rs


@app.route('/')
def hello_world():
   return None
# configuring logging


@app.route("/country", methods=['GET'])
def query_result():
    args = request.args
    country = args.get("country")
    print(country)
    return json.dumps(query_country(country))

if __name__ =="__main__":

    app.run(host="127.0.0.1", port=5000)

# movies lasting less than 100 seconds
# query2 = """
# PREFIX movie: <http://www.semanticweb.org/duc.nguyensy10/ontologies/2022/8/untitled-ontology-21#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
# SELECT DISTINCT ?name ?durationSeconds
# WHERE { ?film rdf:type movie:Movie .
#         ?film movie:movieName ?name .
#         ?film movie:durationSeconds ?durationSeconds .
# 		FILTER (?durationSeconds < "660.0"^^xsd:float)   
#       }
# """

# results = g.query(query2)
# print ('{0:30s} {1:30s}'.format("Name","Duration (sec)"))
# print ('{0:30s} {1:30s}'.format("------------------------------","------------------------------"))
# for name,duration in results:
# 	print ('{0:30s} {1:30s}'.format(name,duration))
	

# query3 = """
# PREFIX movie: <http://www.semanticweb.org/duc.nguyensy10/ontologies/2022/8/untitled-ontology-21#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
# SELECT DISTINCT ?name ?budget
# WHERE { ?film rdf:type movie:Movie .
#         ?film movie:movieName ?name .
#         ?film movie:budget ?budget .
# 		FILTER (?budget < 6600)   
#       }
# """

# results = g.query(query3)
# print ('{0:30s} {1:30s}'.format("Name","Budget($))"))
# print ('{0:30s} {1:30s}'.format("------------------------------","------------------------------"))
# for name,budget in results:
# 	print ('{0:30s} {1:30s}'.format(name,budget))