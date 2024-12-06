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
    name = individual.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about').split('#')[-1]
    # print(name)

    individuals[name] = {}
    for prop in individual:
        prop_tag = prop.tag.split('}')[1]
        if prop.attrib:
            prop_value = list(prop.attrib.items())[0][1].split('#')[1]
        else:
            prop_value = prop.text
        individuals[name][prop_tag] = prop_value
    # print(individuals[name])

print(individuals, len(individuals))

prefix = """
<rdf:RDF xmlns="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/"
     xml:base="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:Portuguese-Constitution="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#">
    <owl:Ontology rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution"/>
"""

suffix = """
</rdf:RDF>
"""

new_individuals = """
<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Citizen">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToFreeSpeech"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToDefense"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#rightToAssemble"/>
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

# Define the regex pattern to match the entire <owl:NamedIndividual> element including nested tags
pattern = r'(<owl:NamedIndividual[^>]*>.*?</owl:NamedIndividual>)'

# Use re.findall() to extract all matches of <owl:NamedIndividual> elements
named_individuals = re.findall(pattern, new_individuals, flags=re.DOTALL)


individuals = {
}

# Print the result
for ni in named_individuals:
    print(ni)
    print('---')

    # read pt_const.owl and add new individuals

    tree_new = ET.fromstring(prefix + ni + suffix)


    individual = tree_new.find('.//owl:NamedIndividual', namespace)
    name = individual.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about').split('#')[-1]
    # print(name)

    individuals[name] = {}
    for prop in individual:
        prop_tag = prop.tag.split('}')[1]
        if prop.attrib:
            prop_value = list(prop.attrib.items())[0][1].split('#')[1]
        else:
            prop_value = prop.text

        if prop_tag != 'hasRight':
            individuals[name][prop_tag] = prop_value
        else:
            if individuals[name].get(prop_tag) is None:
                individuals[name][prop_tag] = [prop_value]
            else:
                individuals[name][prop_tag].append(prop_value)
            
    print("INDIVIDUALS;", individuals[name])

print(individuals, len(individuals))

def sort_key(x):
    BIG_NUMBER = 1000000
    if x[1]['type'] not in ['Right', 'Entity']:
        return BIG_NUMBER
    return ['Right', 'Entity'].index(x[1]['type'])

individuals = sorted(individuals.items(), key=sort_key)

print(individuals)

onto = owlready2.get_ontology("ontologies/pt_const.owl").load()
onto.namespace = "http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#"
# print(dir(onto['Entity']))

# print(dir(onto))

# print(onto.Everyone.hasRight)
# print(onto.resistInfringementOrder.description)


# RightToFreeSpeech = onto.Right("rightToFreeSpeech")
# RightToFreeSpeech.description = ["Exercising the right to free speech"]
# Citizen = onto.Entity("Citizen")
# Citizen.hasRight = [onto.rightToFreeSpeech]

# print(onto.Citizen.hasRight)
# print(onto.rightToFreeSpeech.description)


for individual, props in individuals:
    print(individual)
    NewIndividual = onto[props['type']](name=individual)
    for p in props:
        if p == 'type':
            continue
        if p == 'hasRight':
            print(p, props[p], [onto[p_i] for p_i in props[p]])
            setattr(NewIndividual, p, [onto[p_i] for p_i in props[p]])
            continue
        setattr(NewIndividual, p, [props[p]])


print([c for c in onto.classes()])

onto.save("ontologies/pt_const_test.owl", format="rdfxml")
