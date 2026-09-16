export const schemaStatements = [
  'CREATE CONSTRAINT subject_id_unique IF NOT EXISTS FOR (n:Subject) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT lesson_id_unique IF NOT EXISTS FOR (n:Lesson) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (n:Concept) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT property_id_unique IF NOT EXISTS FOR (n:Property) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT exercise_id_unique IF NOT EXISTS FOR (n:Exercise) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT method_id_unique IF NOT EXISTS FOR (n:Method) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (n:Document) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE',
  'CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (n:User) REQUIRE n.email IS UNIQUE',
  'CREATE CONSTRAINT progress_unique IF NOT EXISTS FOR (p:Progress) REQUIRE (p.user_id, p.concept_id) IS UNIQUE',
  'CREATE FULLTEXT INDEX conceptSearch IF NOT EXISTS FOR (n:Concept) ON EACH [n.name, n.description, n.quote, n.keyphrases, n.aliases]',
  'CREATE FULLTEXT INDEX knowledgeSearch IF NOT EXISTS FOR (n:Concept) ON EACH [n.name, n.description, n.quote, n.keyphrases, n.aliases]'
];
