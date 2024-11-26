import ollama
from pypdf import PdfReader
import re

extracted_knowledge = {
    "entities": set(),
    "relationships": []
}

def extract_owl_and_relationships_recursive(articles, i, known_relationships=None):
    if i >= len(articles) or i+1 >= len(articles):
        return 
    if known_relationships is None:
        known_relationships = extracted_knowledge["relationships"]

    prompt = f"Currently I have these properties: {', '.join(known_relationships)}.\n" \
             f"Create ontologies from the Law bellow in the OWL format with relevant properties." \
             f"Try to reuse the maximum of properties that are related with already have been used (at the start of the prompt)"\
             f"Only write in the response the entities and relationships, nothing else."\
             f"if you really need to add new ones (only if really needed), write the new set of relations in the format at the beginning of your answer [...,...]"\
             f"Dont write any text more than what is necessary in order for me to parse it correctly"\
             f"Example: <?xml version=\"1.0\"?>\n"\
             f"<rdf:RDF xmlns=\"http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/\"\n"\
             f"xml:base=\"http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution/\"\n"\
             f"xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n"\
             f"xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n"\
             f"xmlns:xml=\"http://www.w3.org/XML/1998/namespace\"\n"\
             f"xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n"\
             f"xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n"\
             f"xmlns:Portuguese-Constitution=\"http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#\">\n"\
             f"<owl:Ontology rdf:about=\"http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution\">\n"\
             f"<!-- Define the classes -->\n"\
             f"<owl:Class rdf:about=\"http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity\">\n"\
             f"<rdfs:subClassOf rdf:resource=\"http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Portuguese_Republic\"/>\n"\
             f"</owl:Class>\n"\
             f"\n\n{articles[i]}"

    response = ollama.generate(model='llama3', prompt=prompt)
    
    response_text = response["response"]

    print("Raw Response Text:", response_text)
    return extract_owl_and_relationships_recursive(articles, i+1, extracted_knowledge["relationships"])

reader = PdfReader("constpt2005.pdf")
text = ""
for page in reader.pages[:5]:
    text += page.extract_text()

article_pattern = re.compile(r"(Artigo) \d.º")
articles = article_pattern.split(text)
articles.pop(0)
# print(articles)
extract_owl_and_relationships_recursive(articles, 0)

#legal_text = "Article 1: Portugal is a sovereign Republic. Article 2: The Constitution governs the Republic."
#extracted_knowledge = extract_entities_relationships_recursive(reader)