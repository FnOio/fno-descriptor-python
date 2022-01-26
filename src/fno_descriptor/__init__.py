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
        :return:
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
            (s,FNO['predicate'], rdflib.Literal(name)),
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
            (s,FNO['predicate'], rdflib.Literal(name)),
            (s,FNO['type'], ptype),
            # parameter mapping
            (s_param_mapping, RDF.type, FNO['ReturnMapping']),
            (s_param_mapping, RDF.type, FNO['DefaultReturnMapping']),
            (s_param_mapping, FNOM['functionOutput'], s)
        ]
        [ g.add(x) for x in triples ]

        return g


    @staticmethod
    def create_description_graph(f, type_map: dict) -> rdflib.Graph:
        """
        """
        function_meta = FnODescriptor.extract_function_metadata(f, type_map)

        parameter_descriptions_dict = { 
            pname: FnODescriptor.describe_parameter(**pannot)
            for pname, pannot in function_meta['input'].items()}
        
        output_descriptions_dict = { 
            pname: FnODescriptor.describe_output(**pannot)
            for pname, pannot in function_meta['output'].items()}

        # Combine parameter + output descriptions and generate RDF graph
        function_description_graph = functools.reduce(
            operator.add,[ *parameter_descriptions_dict.values(), 
            *output_descriptions_dict.values() ])

        return function_description_graph
