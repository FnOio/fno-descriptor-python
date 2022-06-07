import rdflib
from fno_descriptor import FnODescriptor as fd, NAMESPACES

# Usage example: create FnO description graph for given Python function
# 
class Iri:
    pass

# Python function to describe
def executeRMLMapper(fpathMapping : Iri, fpathOutput: Iri, fpathRMLMapperJar: Iri,
        fpathRMLMapperTempFolder: Iri, sources: dict) -> Iri:
    return Iri()


def publish(inputRDF: Iri) -> Iri:
    pass



# Python type -> target type
type_map = {
    'Iri': rdflib.XSD.anyURI,
    'dict': NAMESPACES['ex']['recordStringToAny'] # ~ TypeScript Record<string,any>
}

# Generate the function description graph
function_description_graph = fd.describe_function(
    publish, type_map)

# Print to console    
function_description_graph.print()

# Write to file
function_description_graph.serialize(
    destination='example_function_description.ttl', 
    format='turtle')

