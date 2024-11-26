import ollama

response = ollama.generate(model="llama3", prompt="""
Currently i have these properties:
[hasRight, isPartOf]

Article 1
(Portuguese Republic)
Portugal is a sovereign Republic, based on the dignity of the human person and the will of the people and
committed to building a free, just and solidary society.

Create an ontology from the the law Article 1 in the OWL format with relevant properties, try to reuse the maximum of 
properties that are related with already have been used (at the start of the prompt), if you really need to add new 
ones (only if really needed), write the new set of relations in the format at the end of your answer in the 
format [...,...]
""", stream=True)
for chunk in response:
  print(chunk['response'], end='')
print()

