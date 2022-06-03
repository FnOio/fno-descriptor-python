import typing

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

# example: basic sum


# example: KG Construction



###############################################################################

def get_shacl_graph():
    return load_graph('../shapes/all.ttl')
def run_test(f,
             type_map,
             shacl_graph,
             print_function_description_graph = False):
    print(f'👉 testing function: {f.__name__}')
    function_description_graph = fd.describe_function(
            f, type_map)

    if print_function_description_graph:
        function_description_graph.print()

    vr = pyshacl.validate(function_description_graph,
                          shacl_graph=shacl_graph)
    conforms, results_graph, results_text = vr
    print(results_text)
    assert conforms


def test_sum():
    # test function
    def mysum(a: int, b: int) -> int:
        """ Computes the sum of a and b.
        """
        return a + b

    type_map = {
            'int': rdflib.XSD.int,
    }
    shg = get_shacl_graph()
    run_test(mysum, type_map, shg,)



def test_kgc():
    # Python type -> target type
    type_map = {
            'int': rdflib.XSD.int,
            'Iri': rdflib.XSD.anyURI,
    }

    class Iri:
        pass

    # Python function to describe
    def generate_rdf(mapping: Iri) -> Iri:
        """ Generates RDF using the given RML Mapping.
        Returns the IRI to the output result.
        """
        return Iri()

    def publish(inputRDF: Iri) -> Iri:
        pass


    run_test(generate_rdf, type_map, shacl_graph=get_shacl_graph())
    run_test(publish, type_map, shacl_graph=get_shacl_graph())


test_sum()
test_kgc()