
import ast
import os
import ollama
from pypdf import PdfReader
import re
import xml.etree.ElementTree as ET 
import owlready2

from object_property_configs import *

FIRST_PAGE = 9
LAST_PAGE = 107
NUMBER_OF_PAGES_PER_CHUNK = 1
MAX_RETRIES = 3

OBJECT_PROPERTY = "isPartOf"

BASE_PROMPT = f"""


Create an OWL ontology in RDF/XML Syntax with instances of new individuals with objectProperty {OBJECT_PROPERTY} from the Articles above.

Try to reuse already existing named individuals as much as possible so that expressions with similar meaning are represented by the same individual (for example, the phrases "Everyone" and "Every citizen" can be both represented by the same named individual "Everyone", no need to create a named individual "Every citizen").
If there are any new individuals in the Articles provided, please don't make up any, just say there are no new individuals.
Current individuals:

"""

EXAMPLE_ONTOLOGY = f"""
Base ontology (don't write this part in your response):
```xml
<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/"
        xml:base="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/"
        xmlns:owl="http://www.w3.org/2002/07/owl#"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:xml="http://www.w3.org/XML/1998/namespace"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
        xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
        xmlns:Portuguese-Constitution="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#">
        <owl:Ontology rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution"/>

    {OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE[OBJECT_PROPERTY]}
```
Write the new individuals of the classes "{TYPE_ORDER[OBJECT_PROPERTY][0]}" and "{TYPE_ORDER[OBJECT_PROPERTY][1]}" that you found that have the objectProperty {OBJECT_PROPERTY}, only if you found any, as in the following example with the named individuals "{NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY][0]}" and "{NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY][1]}":
```xml
<!-- Instantiation -->

{EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE[OBJECT_PROPERTY]}
```

After that, write only the name of the new named individuals you found exactly in this format, as in this case "{NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY][0]}" and "{NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY][1]}":

individuals = ["{NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY][0]}", "{NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY][1]}"]
"""

RDFXML_PREFIX = """
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

RDFXML_SUFFIX = """
</rdf:RDF>
"""

NAMESPACE = {
    'base': 'http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'Portuguese-Constitution': 'http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#'
}

onto = owlready2.get_ontology("ontologies/pt_const_ispartof.owl").load()
onto.namespace = "http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#"


reader = PdfReader("Constitution7th.pdf")
current_individuals = NAMED_INDIVIDUALS_NAMES[OBJECT_PROPERTY]

# for i in range(FIRST_PAGE, LAST_PAGE, NUMBER_OF_PAGES_PER_CHUNK):

current_retries = {
    i: 0 for i in range(FIRST_PAGE, LAST_PAGE, NUMBER_OF_PAGES_PER_CHUNK)
}

i = FIRST_PAGE - NUMBER_OF_PAGES_PER_CHUNK
while i < LAST_PAGE - NUMBER_OF_PAGES_PER_CHUNK:
    i += NUMBER_OF_PAGES_PER_CHUNK
    text = ""
    for page in reader.pages[i:i+NUMBER_OF_PAGES_PER_CHUNK]:
        text += page.extract_text()

    # prompt = f"""
    #     {BASE_PROMPT}
    #     classes = {current_classes}

    #     {EXAMPLE_ONTOLOGY}

        
    #     Here is the document you need to parse:

    #     {text}
    # """

    prompt = f"""
Here is the document you need to parse:

{text}

{EXAMPLE_ONTOLOGY}
{BASE_PROMPT}
individuals = {current_individuals}
    """
    
    print(f"\n\n Number of characters in prompt: {len(prompt)} \n Number of tokens in prompt: {len(prompt.split())}\n\n")

    # print(prompt)

    response = ollama.generate(model="llama3", prompt=prompt, stream=True)
    
    full_response = ""
    for chunk in response:
        print(chunk['response'], end='')
        full_response += chunk['response']

    # with open("outputs/ontology39.owl", "r") as f:
    #     full_response = f.read()

    # <owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder">
    #     <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    #     <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
    # is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
    # </owl:NamedIndividual>

    # write response to next ontologyN.owl
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    current_ontology_index = len(os.listdir("outputs"))
    
    with open(f"outputs/ontology{current_ontology_index+1}.owl", "w") as f:
        f.write(full_response)
    
    print("\n\n----")

    pattern = r'(<owl:NamedIndividual.*?</owl:NamedIndividual>)'
    named_individuals = re.findall(pattern, full_response, flags=re.DOTALL)
    if named_individuals is None:
        print(f"Pattern NamedIndividual not found, skipping page {i}")
        continue

    try:
        individuals = {}
        for ni in named_individuals:
            print(ni)
            print('\n----\n')

            # read pt_const.owl and add new individuals

            tree_new = ET.fromstring(RDFXML_PREFIX + ni + RDFXML_SUFFIX)


            individual = tree_new.find('.//owl:NamedIndividual', NAMESPACE)
            name = individual.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about').split('#')[-1]

            # print(name)

            if name in current_individuals:
                continue
            
            individuals[name] = {}
            for prop in individual:
                prop_tag = prop.tag.split('}')[1]
                if prop.attrib:
                    prop_value = list(prop.attrib.items())[0][1].split('#')[1]
                else:
                    prop_value = prop.text
                    
                if prop_tag != OBJECT_PROPERTY:
                    individuals[name][prop_tag] = prop_value
                else:
                    if individuals[name].get(prop_tag) is None:
                        individuals[name][prop_tag] = [prop_value]
                    else:
                        individuals[name][prop_tag].append(prop_value)
                # print(individuals[name])
        

        # sort by type (predicates before subjects)
        def sort_key(x):
            BIG_NUMBER = 1000000
            if x[1]['type'] not in TYPE_ORDER[OBJECT_PROPERTY]:
                return BIG_NUMBER
            return TYPE_ORDER[OBJECT_PROPERTY].index(x[1]['type'])

        sorted_individuals = sorted(individuals.items(), key=sort_key)

        # print(sorted_individuals)

        for individual, props in sorted_individuals:
            newIndividual = onto[props['type']](name=individual)
            for p in props:
                if p == 'type':
                    continue
                if p == OBJECT_PROPERTY:
                    setattr(newIndividual, p, [onto[p_i] for p_i in props[p]])
                    continue
                setattr(newIndividual, p, [props[p]])
    except Exception as e: 
        if current_retries[i] < MAX_RETRIES:
            print(f"Could not parse named individuals, retrying page {i}\n\n\n\n")
            current_retries[i] += 1
            i -= 1
            continue
        print(f"Maximum retries reached, could not parse named individuals, skipping page {i}\n\n\n\n")
        continue
    
    # extend current_individuals
    try:
        new_individuals = re.search(r"individuals\s*=\s*(\[.*?\])", full_response)

        if new_individuals is None:
            print(f"No new individuals found in page {i}\n\n\n\n")
            continue

        print(new_individuals.group(1))

        current_individuals.extend(ast.literal_eval(new_individuals.group(1)))

        # remove duplicates
        current_individuals = list(set(current_individuals))

        print(current_individuals)
    except Exception as e:
        print(f"Could not parse new individuals, skipping individuals of page {i}\n\n\n\n")
        continue

# write response to next ontologyN.owl
current_ontology_outputs_index = len(os.listdir("ontologies/output_ontologies"))

onto.save(f"ontologies/output_ontologies/pt_const{current_ontology_outputs_index + 1}.owl", format="rdfxml")

