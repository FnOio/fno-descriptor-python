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
def test_function_description_graphs(function_description_graphs,
                                     shape_graph,
                                     should_conform,
                                     kwargs_shacl_validate ={
                                             'inference'     : 'rdfs',
                                             'advanced'      : True,
                                             'allow_infos'   : True,
                                             'allow_warnings': True},
                                     print_validation_result = True
                                     ):
    """Evaluates the given function_description graphs against given shape graph.
    If should_conform is set to True, the validation result is expected to conform.
    Otherwise, not. This can be used to perform invalid tests.
    """
    for fdg_key, function_description_graph in function_description_graphs.items():
        print(f'👉 {fdg_key}')
        vr = pyshacl.validate(function_description_graph,
                              shacl_graph=shape_graph,
                              **kwargs_shacl_validate
                              )
        conforms, results_graph, results_text = vr
        if print_validation_result:
            print(results_text)
        if not conforms == should_conform:
            raise Exception(
            f'''❌ function graph: {fdg_key} 
            Expected conformance:\t{should_conform}
            Resulting conformance:\t{conforms} 
            ''')

# SHACL shape graph
shg = load_graph('shapes/all.ttl')

# VALID

function_description_graphs = {
        os.path.basename(x): load_graph(x)
        for x in sorted(glob('test/resources/valid/*.ttl'))
}
print('🟩 VALID function description graphs: ' , function_description_graphs.keys())
test_function_description_graphs(function_description_graphs,
                                 shg,
                                 should_conform=True)
# INVALID

invalid_function_description_graphs = {
        os.path.basename(x): load_graph(x)
        for x in sorted(glob('test/resources/invalid/*.ttl'))
}
print('🟥 INVALID function description graphs: ' , invalid_function_description_graphs.keys())
test_function_description_graphs(invalid_function_description_graphs,
                                 shg,
                                 should_conform=False)
