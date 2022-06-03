import os
import functools
import operator
import rdflib
from rdflib import XSD, RDF
import typing

from prefixes import prefixes
NAMESPACES = { k: rdflib.Namespace(v) for k,v in prefixes.items() }

FNO = NAMESPACES['fno']
FNOM = NAMESPACES['fnom']
FNS = NAMESPACES['fns']

class Util:
    @staticmethod
    def bind_namespaces(g: rdflib.Graph, namespaces = NAMESPACES) -> rdflib.Graph:
        for prefix, ns in NAMESPACES.items():
            g.bind(prefix, ns)
        return g


class FnODescriptor:


    @staticmethod
    def extract_function_metadata(f, type_map: dict) -> dict:
        """
        :param f: function to extract metadata from
        :param type_map: mapping of Python type -> target type
        :return: dict {
            'input': dict,
            'output': dict
        }
        """
        out = {
            k: {
                'name': k,
                'ptype': type_map[v.__name__],
                'index': i

            }
            for i,(k,v) in enumerate(f.__annotations__.items())
        }
        return {
            'input': {k:v for k,v in out.items() if k != 'return'},
            'output': {k:v for k,v in out.items() if k == 'return'}
        }


    @staticmethod
    def describe_parameter(name, ptype, required = None, index = None, **kwargs):
        """
        :param name:
        :param ptype:
        :param required: TODO
        :param index:
        :return: RDFGraph
        """
        suff = 'Parameter'
        pname = f'{name}{suff}'
        g = rdflib.Graph()
        Util.bind_namespaces(g)
        # Parameter resource
        s = FNS[pname]
        s_param_mapping = FNS[f'{name}{suff}Mapping']
        triples = [
            # parameter
            (s,RDF.type, FNO['Parameter']),
            (s,FNO['predicate'], FNS[name]),
            (s,FNO['type'], ptype),
            # parameter mapping
            (s_param_mapping, RDF.type, FNO['ParameterMapping']),
            (s_param_mapping, RDF.type, FNOM['PositionParameterMapping']),
            (s_param_mapping, FNOM['functionParameter'], s),
            (s_param_mapping, FNOM['implementationParameterPosition'], rdflib.Literal(index, datatype=XSD.integer)),
        ]
        [ g.add(x) for x in triples ]

        return g

    @staticmethod
    def describe_output(name, ptype, **kwargs):
        """
        fns:strOutput
            a             fno:Output ;
            fno:name      "String output" ;
            rdfs:label    "String output" ;
            fno:predicate fns:out ;
            fno:type xsd:string
        .


        fns:strOutputMapping
            a fno:ReturnMapping, fnom:DefaultReturnMapping ;
            fnom:functionOutput fns:strOutput
        .
        """
        suff = 'Output'
        pname = f'{name}{suff}'
        g = rdflib.Graph()
        Util.bind_namespaces(g)
        # Parameter resource
        s = FNS[pname]
        s_param_mapping = FNS[f'{name}{suff}Mapping']
        triples = [
            # parameter
            (s,RDF.type, FNO['Output']),
            (s,FNO['predicate'], FNS[name]),
            (s,FNO['type'], ptype),
            # parameter mapping
            (s_param_mapping, RDF.type, FNO['ReturnMapping']),
            # Note: namespace for DefaultReturnMapping is FNOM!
            (s_param_mapping, RDF.type, FNOM['DefaultReturnMapping']),
            (s_param_mapping, FNOM['functionOutput'], s)
        ]
        [ g.add(x) for x in triples ]

        return g

    @staticmethod
    def describe_function(f, type_map: dict) -> rdflib.Graph:
        """
        fns:functionC
            a fno:Function ;
            dcterms:description "function C "@en ;
            fno:expects ( fns:str0Parameter ) ;
            fno:returns ( fns:strOutput )
        .

        # todo: dcterms:description "function C "@en ; can be extracted from __doc__

        """
        #
        g = rdflib.Graph()
        Util.bind_namespaces(g)
        # Function resource
        suff = 'Function'
        name = f.__name__
        pname = f'{name}{suff}'

        s = FNS[pname]
        triples = [
            # Function
            (s,RDF.type, FNO['Function']),
            (s,FNO['predicate'], rdflib.Literal(name)),
        ]
        [ g.add(x) for x in triples ]

        g_params_outputs = FnODescriptor.create_description_graph(f,type_map)

        def create_rdf_list(g, elements):
            """ Helper to create an RDF List with the given elements.
            :param g: RDF Graph on which the RDF list will be attached.

            """
            return rdflib.Container(g,
                             rdflib.BNode(),
                             seq=elements,
                             rtype='List')

        # create fno:expects container
        c_expects = create_rdf_list(
                g,
                [x['s']
                 for x in g_params_outputs.query(
                        '''SELECT ?s ?p ?o WHERE {  ?s a fno:Parameter }''',
                        initNs=NAMESPACES)
                ]
        )

        # create fno:returns list
        c_returns = create_rdf_list(
                g,
                [x['s']
                 for x in g_params_outputs.query(
                        '''SELECT ?s ?p ?o WHERE {  ?s a fno:Output }''',
                        initNs=NAMESPACES)
                 ]
        )

        g += g_params_outputs

        g.add((s, FNO['expects'], c_expects.uri))
        g.add((s, FNO['returns'], c_returns.uri))

        # add fno:Mapping
        # At this point, the function description graph contains
        # - parameter descriptions & parameter mappings
        # - return descriptions & return mappings

        # Build the fno:Mapping (https://fno.io/spec/#fno-Mapping)
        # The fno:Mapping maps a fno:Function to a (part) of an implementation.
        # It comprises of
        # - the mapping of the method name [ ]
        # - the mapping of parameters [x]
        # - the mapping of the outputs [x]

        g_method_mapping = rdflib.Graph()

        s_mapping = FNS[f'{name}_MethodMapping']
        bn_method_mapping = rdflib.BNode()
        mm_triples = [
                (s_mapping, RDF.type, FNO['Mapping']),
                (s_mapping, FNO['methodMapping'], bn_method_mapping),
                (bn_method_mapping, RDF.type, FNOM['StringMethodMapping']),
                (bn_method_mapping, FNOM['method-name'], rdflib.Literal(name))
        ]
        for t in mm_triples:
            try:
                g_method_mapping.add(t)
            except Exception as e:
                print(f'''
                Exception: {e}
                For triple: {t}
                ''')

        # add method mapping graph to result graph
        g += g_method_mapping

        return g
        
    @staticmethod
    def create_description_dict(f, type_map: dict) -> dict:
        """
        """
        function_meta = FnODescriptor.extract_function_metadata(f, type_map)

        parameter_descriptions_dict = { 
            pname: FnODescriptor.describe_parameter(**pannot)
            for pname, pannot in function_meta['input'].items()}
        
        output_descriptions_dict = { 
            pname: FnODescriptor.describe_output(**pannot)
            for pname, pannot in function_meta['output'].items()}

        return {
            'input': parameter_descriptions_dict,
            'output': output_descriptions_dict
        }

    @staticmethod
    def create_description_graph(f, type_map: dict) -> rdflib.Graph:
        """
        
        """
        description_dict = FnODescriptor.create_description_dict(f, type_map)
        
        # Combine parameter + output descriptions and generate RDF graph
        function_description_graph = functools.reduce(
            operator.add,[ 
                *description_dict['input'].values(), 
                *description_dict['output'].values(), 
                # TODO: https://gitlab.ilabt.imec.be/fno/fno-descriptor-python/-/issues/2
            ])

        return function_description_graph
