OBJECT_PROPERTY_DEFINITIONS = {}
OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE = {}
EXAMPLE_NAMED_INDIVIDUALS = {}
EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE = {}
NAMED_INDIVIDUALS_NAMES = {}
TYPE_ORDER = {}

TYPE_ORDER['hasRight'] = ['Right', 'Entity']

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

NAMED_INDIVIDUALS_NAMES['hasRight'] = ['Everyone', 'resistInfringementOrder']


TYPE_ORDER['hasDuty'] = ['Duty', 'Entity']
OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE['hasDuty'] = """
<owl:ObjectProperty rdf:about="#hasDuty">
        <rdfs:domain rdf:resource="#Entity"/>
        <rdfs:range rdf:resource="#Duty"/>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="#description">
        <rdfs:domain rdf:resource="#Duty"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
    </owl:DatatypeProperty>

    <owl:Class rdf:about="#Duty">
        <rdfs:subClassOf rdf:resource="#Portuguese_Republic"/>
    </owl:Class>

    <owl:Class rdf:about="#Entity">
        <rdfs:subClassOf rdf:resource="#Portuguese_Republic"/>
    </owl:Class>
"""

EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE['hasDuty'] = """
<owl:NamedIndividual rdf:about="#EducateChildren">
    <rdf:type rdf:resource="#Duty"/>
    <Portuguese-Constitution:description>Educate and maintain their children</Portuguese-Constitution:description>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="#Parents">
    <rdf:type rdf:resource="#Entity"/>
    <Portuguese-Constitution:hasDuty rdf:resource="#EducateChildren"/>
</owl:NamedIndividual>
"""

NAMED_INDIVIDUALS_NAMES['hasDuty'] = ['Parents', 'EducateChildren']


TYPE_ORDER['supports'] = ['Entity', 'Entity']

OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE['supports'] = """
<owl:ObjectProperty rdf:about="#supports">
        <rdfs:domain rdf:resource="#Entity"/>
        <rdfs:range rdf:resource="#Entity"/>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="#description">
        <rdfs:domain rdf:resource="#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
    </owl:DatatypeProperty>

    <owl:Class rdf:about="#Entity">
        <rdfs:subClassOf rdf:resource="#Portuguese_Republic"/>
    </owl:Class>
"""

EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE['supports'] = """
<owl:NamedIndividual rdf:about="#Cooperatives">
    <rdf:type rdf:resource="#Entity"/>
    <Portuguese-Constitution:description>Creation and activities of cooperatives</Portuguese-Constitution:description>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="#State">
    <rdf:type rdf:resource="#Entity"/>
    <Portuguese-Constitution:supports rdf:resource="#Cooperatives"/>
    <Portuguese-Constitution:description>The Portuguese state</Portuguese-Constitution:description>
</owl:NamedIndividual>
"""

NAMED_INDIVIDUALS_NAMES['supports'] = ['Cooperatives', 'State']


TYPE_ORDER['isPartOf'] = ['Entity', 'Entity']

OBJECT_PROPERTY_DEFINITIONS_WITHOUT_NAMESPACE['isPartOf'] = """
<owl:ObjectProperty rdf:about="#isPartOf">
        <rdfs:domain rdf:resource="#Entity"/>
        <rdfs:range rdf:resource="#Entity"/>
    </owl:ObjectProperty>

    <owl:DatatypeProperty rdf:about="#description">
        <rdfs:domain rdf:resource="#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
    </owl:DatatypeProperty>

    <owl:Class rdf:about="#Entity">
        <rdfs:subClassOf rdf:resource="#Portuguese_Republic"/>
    </owl:Class>
"""

EXAMPLE_NAMED_INDIVIDUALS_WITHOUT_NAMESPACE['isPartOf'] = """
<owl:NamedIndividual rdf:about="#Law">
    <rdf:type rdf:resource="#Entity"/>
    <Portuguese-Constitution:description>Portuguese Law</Portuguese-Constitution:description>
</owl:NamedIndividual>

<owl:NamedIndividual rdf:about="#InternationalLaw">
    <rdf:type rdf:resource="#Entity"/>
    <Portuguese-Constitution:isPartOf rdf:resource="#Law"/>
    <Portuguese-Constitution:description>The norms and principles of general or common international law</Portuguese-Constitution:description>
</owl:NamedIndividual>
"""

NAMED_INDIVIDUALS_NAMES['isPartOf'] = ['Law', 'InternationalLaw']