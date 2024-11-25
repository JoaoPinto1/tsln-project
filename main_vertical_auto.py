
import os
import ollama
from pypdf import PdfReader
import re
import xml.etree.ElementTree as ET 
import owlready2

FIRST_PAGE = 15
LAST_PAGE = 16
NUMBER_OF_PAGES_PER_CHUNK = 1

OBJECT_PROPERTY_DEFINITIONS = {}
OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE = {}
EXAMPLE_NAMED_INDIVIDUALS = {}
EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE = {}

OBJECT_PROPERTY = "hasRight"

OBJECT_PROPERTY_DEFINITIONS['hasRight'] = """
<owl:ObjectProperty rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#hasRight">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#description">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
    </owl:DatatypeProperty>

    <owl:Class rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Portuguese_Republic"/>
    </owl:Class>

    <owl:Class rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Portuguese_Republic"/>
    </owl:Class>
"""

OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE['hasRight'] = """
<owl:ObjectProperty rdf:about="#hasRight">
        <rdfs:domain rdf:resource="#Entity"/>
        <rdfs:range rdf:resource="#Right"/>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="#description">
        <rdfs:domain rdf:resource="#Right"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
    </owl:DatatypeProperty>

    <owl:Class rdf:about="#Entity">
        <rdfs:subClassOf rdf:resource="#Portuguese_Republic"/>
    </owl:Class>

    <owl:Class rdf:about="#Right">
        <rdfs:subClassOf rdf:resource="#Portuguese_Republic"/>
    </owl:Class>
"""

EXAMPLE_NAMED_INDIVIDUALS['hasRight'] = """
<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Everyone">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder"/>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
</owl:NamedIndividual>
"""

EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE['hasRight'] = """
<owl:NamedIndividual rdf:about="#Everyone">
    <rdf:type rdf:resource="#Entity"/>
    <Portuguese-Constitution:hasRight rdf:resource="#resistInfringementOrder"/>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="#resistInfringementOrder">
    <rdf:type rdf:resource="#Right"/>
    <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
</owl:NamedIndividual>
"""

BASE_PROMPT = f"""


Create an OWL ontology in RDF/XML Syntax with instances of new individuals with objectProperty {OBJECT_PROPERTY} from the Articles above.

Try to reuse already existing named individuals as much as possible so that expressions with similar meaning are represented by the same individual (for example, "Everyone" and "Every citizen" can be both represented by the same named individual "Everyone", no need to create a new one).
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

    {OBJECT_PROPERTY_DEFINITIONS[OBJECT_PROPERTY]}
```
Write the new individuals of the classes "Entity" and "Right" that you found that have the objectProperty "hasRight", only if you found any, as in the following example with the named individuals "Everyone" and "resistInfringementOrder":
```xml
<!-- Instantiation -->

{EXAMPLE_NAMED_INDIVIDUALS[OBJECT_PROPERTY]}
```

After that, write only the name of the new named individuals you found exactly in this format, as in this case "Everyone" and "resistInfringementOrder":

individuals = ["Everyone", "resistInfringementOrder"]
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

onto = owlready2.get_ontology("ontologies/pt_const.owl").load()
onto.namespace = "http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#"


reader = PdfReader("Constitution7th.pdf")
current_individuals = ["Everyone", "resistInfringementOrder"]

for i in range(FIRST_PAGE, LAST_PAGE, NUMBER_OF_PAGES_PER_CHUNK):
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

    response = ollama.generate(model="llama3", prompt=prompt, stream=True)
    
    full_response = ""
    for chunk in response:
        print(chunk['response'], end='')
        full_response += chunk['response']

    # <owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder">
    #     <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    #     <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
    # is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
    # </owl:NamedIndividual>

    # write response to next ontologyN.owl
    current_ontology_index = len(os.listdir("outputs"))
    
    with open(f"outputs/ontology{current_ontology_index+1}.owl", "w") as f:
        f.write(full_response)
    
    print("\n\n----")

    try:
        pattern = r'(<owl:NamedIndividual.*?</owl:NamedIndividual>)'
        named_individuals = re.findall(pattern, full_response, flags=re.DOTALL)
    except:
        print(f"Pattern NamedIndividual not found, skipping page {i}")
        continue

    # try:
    individuals = {}
    for ni in named_individuals:
        print(ni)
        print('\n----\n')

        # read pt_const.owl and add new individuals

        tree_new = ET.fromstring(RDFXML_PREFIX + ni + RDFXML_SUFFIX)


        individual = tree_new.find('.//owl:NamedIndividual', NAMESPACE)
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

    for individual, props in individuals.items():
        newIndividual = onto[props['type']](name=individual)
        for p in props:
            if p == 'type':
                continue
            if p == 'hasRight':
                setattr(newIndividual, p, [onto[props[p]]])
                continue
            setattr(newIndividual, p, [props[p]])
    # except Exception as e: 
        
    #     print(f"Could not parse named individuals, skipping page {i}\n\n\n\n")
    #     continue
    
    print([c for c in onto.classes()])
    print("\n\n\n\n")


# write response to next ontologyN.owl
current_ontology_outputs_index = len(os.listdir("ontologies/outputs_ontologies"))

onto.save(f"ontologies/outputs_ontologies/pt_const{current_ontology_outputs_index + 1}.owl", format="rdfxml")