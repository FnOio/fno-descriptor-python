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

function_description_graphs = {
        os.path.basename(x): load_graph(x)
        for x in sorted(glob('test/resources/*.ttl'))
}
print('function description graphs: ' , function_description_graphs.keys())

shg = load_graph('shapes/all.ttl')
for fdg_key, function_description_graph in function_description_graphs.items():
    print(f'👉 {fdg_key}')
    vr = pyshacl.validate(function_description_graph,
                          shacl_graph=shg,
                          inference='rdfs',
                          advanced=True,
                          allow_infos=True,
                          allow_warnings=True

                          )
    conforms, results_graph, results_text = vr
    print(results_text)

#fpath_function_description = os.path.join(OUTPUT_DIR, 'function_description.ttl')
#function_description_graph.serialize(destination=fpath_function_description, format='turtle')

