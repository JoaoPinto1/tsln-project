import os
import ollama

prompt = """

Create an OWL ontology in RDF/XML Syntax with instances of new individuals with objectProperty "hasRight" in the following Articles. Try to reuse already existing classes for instantiating individuals. If you really need a new class (only if really necessary), add them at the end of your response as described below.

Start your response with "```xml" and end your response with "```classes = [class1, class2, ...]", replacing the [class1, class2, ...] with your new classes.
Don't write other text apart from that.

Current classes and properties:
classes = ['Right', 'Entity']

Articles:

Article 12 
(Principle of universality) 
1. Every citizen enjoys the rights and is subject to the duties enshrined in the Constitution. 
2. Legal persons enjoy the rights and are subject to the duties that are compatible with their nature. 
Article 13 
(Principle of equality) 
1. All citizens possess the same social dignity and are equal before the law. 
2. No one may be privileged, favoured, prejudiced, deprived of any right or exempted from any duty for 
reasons of ancestry, sex, race, language, territory of origin, religion, political or ideological beliefs, 
education, economic situation, social circumstances or sexual orientation. 
Article 14 
(Portuguese abroad) 
Portuguese citizens who find themselves or who reside abroad enjoy the state’s protection in the exercise 
of the rights and are subject to the duties that are not incompatible with their absence from the country. 
Article 15 
(Foreigners, stateless persons, European citizens) 
1. Foreigners and stateless persons who find themselves or who reside in Portugal enjoy the same rights 
and are subject to the same duties as Portuguese citizens. 
2. Political rights, the exercise of public functions that are not predominantly technical in nature, and the 
rights and duties that the Constitution and the law reserve exclusively to Portuguese citizens are excepted 
from the provisions of the previous paragraph. 
3. Save for access to appointment to the offices of President of the Republic, President of the Assembleia da 
República, Prime Minister and President of any of the supreme courts, and for service in the armed forces 
and the diplomatic corps, rights that are not otherwise granted to foreigners are accorded, as laid down by 
law and under reciprocal terms, to the citizens of Portuguese-speaking states who reside permanently in 
Portugal. 
4. Under reciprocal terms, the law may accord foreigners who reside in Portugal the eligibility to vote for 
and stand for election as officeholders of local authority organs. 
5. Under reciprocal terms, the law may also accord citizens of European Union Member States who reside 
in Portugal the eligibility to vote for and stand for election as Members of the European Parliament. 
Article 16 
(Scope and interpretation of fundamental rights) 
1. The fundamental rights enshrined in the Constitution shall not exclude any others set out in applicable 
international laws and legal rules. 
2. The constitutional and legal precepts concerning fundamental rights must be interpreted and completed 
in harmony with the Universal Declaration of Human Rights. 
Article 17 
(Regime governing rights, freedoms and guarantees) 
The  regime  governing  rights,  freedoms  and  guarantees  applies  to  those  set  out  in  Title II  and  to 
fundamental rights of an analogous nature. 
Article 18 
(Legal force) 
1. The constitutional precepts with regard to rights, freedoms and guarantees are directly applicable and 
are binding on public and private entities. 
2. The law may only restrict rights, freedoms and guarantees in cases expressly provided for in the 
Constitution, and such restrictions must be limited to those needed to safeguard other constitutionally 
protected rights and interests. 
3. Laws that restrict rights, freedoms and guarantees must have a general and abstract nature and may not 
have a retroactive effect or reduce the extent or scope of the essential content of the constitutional precepts.




Base ontology:
```xml
<owl:ObjectProperty rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#hasRight">
    <rdfs:domain rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
    <rdfs:range rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
</owl:ObjectProperty>

<owl:Class rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity">
    <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Portuguese_Republic"/>
</owl:Class>

<owl:Class rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right">
    <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Portuguese_Republic"/>
</owl:Class>
```

Example "hasRight" ObjectProperty instantiation:
```xml
<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Everyone">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Entity"/>
    <Portuguese-Constitution:hasRight rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder"/>
</owl:NamedIndividual>



<!-- http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder -->

<owl:NamedIndividual rdf:about="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#resistInfringementOrder">
    <rdf:type rdf:resource="http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#Right"/>
    <Portuguese-Constitution:description>Resist any order that infringes their rights, freedoms or guarantees and, when it 
is not possible to resort to the public authorities, to use force to repel any aggression</Portuguese-Constitution:description>
</owl:NamedIndividual>
```
"""

# append ontology to the prompt from file
# with open("ontologies/pt_const.owl", "r") as f:
#         prompt += f.read()

response = ollama.generate(model="llama3", prompt=prompt, stream=True)
full_response = ""
for chunk in response:
    print(chunk['response'], end='')
    full_response += chunk['response']

# write response to next ontologyN.owl
current_ontology_index = len(os.listdir("outputs"))

with open(f"outputs/ontology{current_ontology_index+1}.owl", "w") as f:
    f.write(full_response)


