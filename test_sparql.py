import owlready2

def get_all_citizen_rights(file_path=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

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


def get_all_relations(file_path=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

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



def get_all_rights(file_path=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

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


def get_all_entity_rights(file_path=None, entity_name=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

  # Get description of all rights of entity "entity_name"
  query_entity_rights = f"""
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?right ?description
  WHERE {{
    :{entity_name} rdf:type :Entity .
    :{entity_name} :hasRight ?right .
    ?right :description ?description .
  }}
  """

  results_entity_rights = list(onto.world.sparql(query_entity_rights))

  for result in results_entity_rights:
      right = result[0]
      description = result[1]
      print(f"Right: {right}, Description: {description}")


def get_all_entity_duties(file_path=None, entity_name=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

  # Get description of all duties of entity "entity_name"
  query_entity_duties = f"""
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?duty ?description
  WHERE {{
    :{entity_name} rdf:type :Entity .
    :{entity_name} :hasDuty ?duty .
    ?duty :description ?description .
  }}
  """

  results_entity_duties = list(onto.world.sparql(query_entity_duties))

  for result in results_entity_duties:
      duty = result[0]
      description = result[1]
      print(f"Duty: {duty}, Description: {description}")


def get_all_duties(file_path=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

  #Get description of all duties
  query_duties_descriptions = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?duty ?description
  WHERE {
    ?duty rdf:type :Duty .
    ?duty :description ?description .
  }
  """

  results_duties_descriptions = list(onto.world.sparql(query_duties_descriptions))

  for result in results_duties_descriptions:
      duty = result[0]
      description = result[1]
      print(f"Duty: {duty}, Description: {description}")


def get_all_entity_supports(file_path=None, entity_name=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

  # Get description of all supports of entity "entity_name"
  query_entity_supports = f"""
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?entity ?description
  WHERE {{
    :{entity_name} rdf:type :Entity .
    :{entity_name} :supports ?entity .
    ?entity :description ?description .
  }}
  """

  results_entity_supports = list(set(tuple(result) for result in onto.world.sparql(query_entity_supports)))

  # print(results_entity_supports)

  for result in results_entity_supports:
      entity = result[0]
      description = result[1]
      print(f"Entity: {entity}, Description: {description}")



def get_all_supports(file_path=None):
  if file_path is None:
    onto = owlready2.get_ontology("ontologies/pt_const2.owl").load()
  else:
    onto = owlready2.get_ontology(file_path).load()

  #Get description of all supports
  query_supports_descriptions = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX : <http://www.semanticweb.org/jbsantos/ontologies/2024/10/Portuguese-Constitution#>

  SELECT ?entity ?description ?entity2 ?description2
  WHERE {
    ?entity rdf:type :Entity .
    ?entity :supports ?entity2 .
    ?entity :description ?description .
    ?entity2 :description ?description2 .
  }
  """

  results_supports_descriptions = list(set(tuple(result) for result in onto.world.sparql(query_supports_descriptions)))

  for result in results_supports_descriptions:
      entity = result[0]
      description = result[1]
      entity2 = result[2]
      description2 = result[3]
      print(f"Entity: {entity}, Description: {description}, Entity2: {entity2}, Description2: {description2}")


# get_all_rights("ontologies/outputs_ontologies/pt_const_rights.owl")

# get_all_entity_rights("ontologies/outputs_ontologies/pt_const_rights.owl", "everyone")

# get_all_entity_duties("ontologies/outputs_ontologies/pt_const_duties.owl", "Citizen")

get_all_entity_supports("ontologies/outputs_ontologies/pt_const_supports.owl", "Portuguese_state")

# get_all_supports("ontologies/outputs_ontologies/pt_const_supports.owl")
