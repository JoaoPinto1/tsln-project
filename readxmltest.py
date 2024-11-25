import re
import xml.etree.ElementTree as ET 
import owlready2

with open("ontologies/pt_const.owl", "r") as f:
    full_response = f.read()

tree = ET.fromstring(full_response)

# xmlns="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/"
#      xml:base="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/"
#      xmlns:owl="http://www.w3.org/2002/07/owl#"
#      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#      xmlns:xml="http://www.w3.org/XML/1998/namespace"
#      xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
#      xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
#      xmlns:Portuguese-Constitution="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#">

namespace = {
    'base': 'http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'Portuguese-Constitution': 'http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#'
}

individuals = {
}

for individual in tree.findall('.//owl:NamedIndividual', namespace):
    name = individual.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
    # print(name)

    individuals[name] = {}

    for property in individual:
        individuals[name][property.tag] = property.attrib if property.attrib else property.text.replace('\n', '')
    # print(individuals[name])

print(individuals, len(individuals))

new_individuals = """
<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Citizen">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToFreeSpeech"/>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToFreeSpeech">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Exercising the right to free speech</Portuguese-Constitution:description>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToDefense">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Defending oneself against any aggression</Portuguese-Constitution:description>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToAssemble">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Assembling peacefully and without arms</Portuguese-Constitution:description>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToPetition">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Petitioning the authorities peacefully and without arms</Portuguese-Constitution:description>
</owl:NamedIndividual>
"""

# read pt_const.owl and add new individuals

onto = owlready2.get_ontology("ontologies/pt_const.owl").load()
print(onto.Right)



