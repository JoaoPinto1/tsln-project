import os
import ollama

prompt = """
Extend the ontology with following article. Please write just the new part of the ontology. Try to reuse already existing properties and classes as much as possible, so that it
is not too complex. Start the prompt with "```xml" and ent your prompt with "```classes = [class1, class2, ...], objectProperties = [objectProperty1, objectProperty2, ...], dataProperties = [dataProperty1, dataProperty2, ...]", data, replacing the [class1, class2, ...], [objectProperty1, objectProperty2, ...], [dataProperty1, dataProperty2, ...] with your new classes, object properties and data properties.

Current classes and properties:
classes = ['Duty', 'Right', 'Individual'], properties = ['hasRight', 'hasDuty', 'description']

Article 12 
(Principle of universality) 
1. Every citizen enjoys the rights and is subject to the duties enshrined in the Constitution. 
2. Legal persons enjoy the rights and are subject to the duties that are compatible with their nature.

Ontology:

"""

# append ontology to the prompt from file
with open("ontologies/pt_const.owl", "r") as f:
        prompt += f.read()

response = ollama.generate(model="llama3", prompt=prompt, stream=True)
full_response = ""
for chunk in response:
    print(chunk['response'], end='')
    full_response += chunk['response']

# write response to next ontologyN.owl
current_ontology_index = len(os.listdir("outputs"))

with open(f"outputs/ontology{current_ontology_index+1}.owl", "w") as f:
    f.write(full_response)


