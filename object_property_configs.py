OBJECT_PROPERTY_DEFINITIONS = {}
OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE = {}
EXAMPLE_NAMED_INDIVIDUALS = {}
EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE = {}
TYPE_ORDER = {}

TYPE_ORDER['hasRight'] = ["Right", "Entity"]

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
