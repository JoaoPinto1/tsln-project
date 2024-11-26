import owlready2


def get_all_relations():
  onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()

  #Get rights and dutys of each entity
  query = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?entity ?right ?duty
  WHERE {
    ?entity rdf:type :Entity .
    OPTIONAL { ?entity :hasRight ?right . }
    OPTIONAL { ?entity :hasDuty ?duty . }
  }
  """

  results = list(onto.world.sparql(query))

  for result in results:
      entity = result[0]
      right = result[1] if len(result) > 1 else None
      duty = result[2] if len(result) > 2 else None
      print(f"Entity: {entity}, Right: {right}, Duty: {duty}")


def get_all_citizen_rights():
  onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()

  #Get all rights of a citizen
  query = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?right
  WHERE {
    :Citizen rdf:type :Entity .
    :Citizen :hasRight ?right .
  }
  """

  results = list(onto.world.sparql(query))

  for result in results:
      right = result[0]
      print(f"Citizen has right: {right}")


def get_all_rights():
  onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()

  #Get description of all rights
  query_rights_descriptions = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?right ?description
  WHERE {
    ?right rdf:type :Right .
    ?right :description ?description .
  }
  """

  results_rights_descriptions = list(onto.world.sparql(query_rights_descriptions))

  for result in results_rights_descriptions:
      right = result[0]
      description = result[1]
      print(f"Right: {right}, Description: {description}")

def get_all_accused_persons_rights():
  onto = owlready2.get_ontology("ontologies/outputs_ontologies/pt_const19.owl").load()

  #Get all rights of a accused person
  query = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?right ?description
  WHERE {
    :AccusedPersons rdf:type :Entity .
    :AccusedPersons :hasRight ?right .
    ?right :description ?description .
  }
  """

  results = list(onto.world.sparql(query))

  for result in results:
      right = result[0]
      description = result[1]
      print(f"Accused Person has right: {right}, Description: {description}")


get_all_accused_persons_rights()
