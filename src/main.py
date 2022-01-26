import functools
import operator
import rdflib
from fno_descriptor import FnODescriptor

# Usage example: create FnO description graph for given Python function
# 


class Iri:
    pass

# Python function to describe
def executeRMLMapper(
        fpathMapping : Iri,
        fpathOutput: Iri,
        fpathRMLMapperJar: Iri,
        fpathRMLMapperTempFolder: Iri
) -> Iri:
    # ...
    result: Iri
    # ...
    return result


# Python type -> target type
type_map = {
    'Iri': rdflib.XSD.anyURI
}
fnod = FnODescriptor()
# 

function_description_graph = fnod.create_description_graph(
    executeRMLMapper, type_map)
function_description_graph.print()
