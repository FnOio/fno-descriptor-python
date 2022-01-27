import functools
import operator
import rdflib
from fno_descriptor import FnODescriptor, NAMESPACES

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
print(type_map)
fnod = FnODescriptor()
function_description_graph = fnod.describe_function(
    executeRMLMapper, type_map)
function_description_graph.print()
function_description_graph.serialize(destination='function_description.ttl', format='turtle')

