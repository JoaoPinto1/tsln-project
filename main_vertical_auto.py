import ollama
from pypdf import PdfReader
import re
import os

FIRST_PAGE = 15
LAST_PAGE = 17
NUMBER_OF_PAGES_PER_CHUNK = 1

OBJECT_PROPERTY = "hasRight"
OBJECT_PROPERTY_DEFINITION = """
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
BASE_PROMPT = f"""
Create an OWL ontology in RDF/XML Syntax with instances of new individuals with objectProperty {OBJECT_PROPERTY} from the Articles above.

Try to reuse already existing named individuals as much as possible so that expressions with similar meaning are represented by the same individual (for example, "Everyone" and "Every citizen" can be both represented as the same named individual "Everyone", no need to create a new one).
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

    {OBJECT_PROPERTY_DEFINITION}
```
Write the new individuals of the classes "Entity" and "Right" that you found that have the objectProperty "hasRight", only if you found any, as in the following example with the named individuals "Everyone" and "resistInfringementOrder":
```xml
<!-- Instantiation -->

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Everyone">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder"/>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
</owl:NamedIndividual>
```

After that, write only the name of the new named individuals you found exactly in this format, as in this case "Everyone" and "resistInfringementOrder":

individuals = ["Everyone", "resistInfringementOrder"]
"""


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

    # # <owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder">
    # #     <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    # #     <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
    # # is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
    # # </owl:NamedIndividual>
    
    # # get all named individuals and properties from the response
    # individuals = re.findall("<owl:NamedIndividual.*</owl:NamedIndividual>", full_response)
    # print(individuals)
    # assert False

    
    # write response to next ontologyN.owl
    current_ontology_index = len(os.listdir("outputs"))

    with open(f"outputs/ontology{current_ontology_index+1}.owl", "w") as f:
        f.write(full_response)

    print("\n\n\n\n")
