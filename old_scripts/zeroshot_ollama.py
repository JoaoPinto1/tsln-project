import ollama

response = ollama.generate(model="llama3", prompt="""
Article 1
(Portuguese Republic)
Portugal is a sovereign Republic, based on the dignity of the human person and the will of the people and
committed to building a free, just and solidary society.

Create an ontology from the the law Article 1 in the OWL format.
""", stream=True)
for chunk in response:
  print(chunk['response'], end='')
print()

