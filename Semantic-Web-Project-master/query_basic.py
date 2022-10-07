import logging
import rdflib

# configuring logging
logging.basicConfig()

# creating the graph
g=rdflib.Graph()
result=g.parse("result_dbpedia.owl", "xml")
print("graph has %s statements.\n" % len(g))

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
		FILTER regex(str(?country), "United_State")   
      }
"""
# ?film movie:producedBy ?producer_movie .
        # ?producer rdf:type movie:Producer .
         # ?language rdf:type movie:Language .
# querying and displaying the results

results = g.query(query1)
print ('{0:30s} {1:40s} {2:40s} {3:40s}'.format("Name","Duration","Country","Description"))
print ('{0:30s} {1:40s} {2:40s} {3:40s}'.format("------------------------------------------","------------------------------------------","------------------------------------------","------------------------------------------"))
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
    

print(dict_rs)

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