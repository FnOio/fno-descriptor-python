import rdflib
from fno_descriptor import FnODescriptor as fd, NAMESPACES
import os
import pyshacl
from glob import glob

print(__file__)
FILE_NAME = os.path.basename(__file__)
OUTPUT_DIR = os.path.join('output', FILE_NAME)
os.makedirs(OUTPUT_DIR, exist_ok=True)
###############################################################################
def load_graph(fpath) -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse(fpath)
    return g

###############################################################################
def mysum(a: int, b: int) -> int:
    """ Computes the sum of a and b.
    """
    return a + b
###############################################################################
# Python type -> target type
# TODO: use defaults
type_map = {
    'int': rdflib.XSD.int,
}


function_description_graph = fd.describe_function(
    mysum, type_map)

function_description_graph.print()




##### SHACL
shacl_graphs = {
        os.path.basename(x): load_graph(x)
        for x in [ '../shapes/function_mappings.ttl' ]
}

print('shacl graphs: ' , shacl_graphs.keys())

# validation reports
for shg_name, shg in shacl_graphs.items():
    print(f'👉 {shg_name}')
    vr = pyshacl.validate(function_description_graph, shacl_graph=shg)
    conforms, results_graph, results_text = vr
    print(results_text)

#fpath_function_description = os.path.join(OUTPUT_DIR, 'function_description.ttl')
#function_description_graph.serialize(destination=fpath_function_description, format='turtle')

