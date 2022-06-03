# fno-descriptor-python

Convenience tool for creating FnO function & parameter descriptions from Python functions.

Manually describing functions can be time-consuming and error-prone.
The `fno-descriptor-python` enables you to quickly define a function signature
in Python,
and generates its corresponding FnO descriptions by leveraging Python
type-hinting.

## Dependencies

- `rdflib`
- `pyshacl`

## Supported

- [x] `fno:Parameter`
- [x] `fno:ParameterMapping`
- [x] `fno:Output`
- [x] `fno:ReturnMapping`
- [x] `fno:Function`
- [x] `fno:Mapping` 
- [x] `fno:MethodMapping`
- [ ] Add `func.__doc__` as `doap:description`
- [x] SHACL validation of generated FnO descriptions
- [ ] Use default type map

## Usage example (`main.py`)

The example describes the following Python function

```python
# Usage example: create FnO description graph for given Python function
# 

class Iri:
    pass

# Python function to describe
def executeRMLMapper(fpathMapping : Iri, fpathOutput: Iri, fpathRMLMapperJar: Iri,
        fpathRMLMapperTempFolder: Iri, sources: dict) -> Iri:
    return Iri()

# Python type -> target type
type_map = {
    'Iri': rdflib.XSD.anyURI,
    'dict': NAMESPACES['ex']['recordStringToAny'] # ~ TypeScript Record<string,any>
}
# 
fnod = FnODescriptor()

function_description_graph = fnod.describe_function(
    executeRMLMapper, type_map)
function_description_graph.print()
function_description_graph.serialize(destination='function_description.ttl', format='turtle')

```

You can run the example as follows:

```bash
python src/main.py
```

### Output

The FnO descriptions will be written to the standard output.

```Turtle
@prefix ex: <http://www.example.com#> .
@prefix fno: <https://w3id.org/function/ontology#> .
@prefix fnom: <https://w3id.org/function/vocabulary/mapping#> .
@prefix fns: <http://example.com/functions#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

fns:executeRMLMapperFunction a fno:Function ;
    fno:expects [ a rdf:List ;
            rdf:_1 fns:fpathRMLMapperTempFolderParameter ;
            rdf:_2 fns:sourcesParameter ;
            rdf:_3 fns:fpathMappingParameter ;
            rdf:_4 fns:fpathOutputParameter ;
            rdf:_5 fns:fpathRMLMapperJarParameter ] ;
    fno:predicate "executeRMLMapper" ;
    fno:returns [ a rdf:List ;
            rdf:_1 fns:returnOutput ] .

fns:fpathMappingParameterMapping a fno:ParameterMapping,
        fnom:PositionParameterMapping ;
    fnom:functionParameter fns:fpathMappingParameter ;
    fnom:implementationParameterPosition 0 .

fns:fpathOutputParameterMapping a fno:ParameterMapping,
        fnom:PositionParameterMapping ;
    fnom:functionParameter fns:fpathOutputParameter ;
    fnom:implementationParameterPosition 1 .

fns:fpathRMLMapperJarParameterMapping a fno:ParameterMapping,
        fnom:PositionParameterMapping ;
    fnom:functionParameter fns:fpathRMLMapperJarParameter ;
    fnom:implementationParameterPosition 2 .

fns:fpathRMLMapperTempFolderParameterMapping a fno:ParameterMapping,
        fnom:PositionParameterMapping ;
    fnom:functionParameter fns:fpathRMLMapperTempFolderParameter ;
    fnom:implementationParameterPosition 3 .

fns:returnOutputMapping a fno:ReturnMapping,
        fnom:DefaultReturnMapping ;
    fnom:functionOutput fns:returnOutput .

fns:sourcesParameterMapping a fno:ParameterMapping,
        fnom:PositionParameterMapping ;
    fnom:functionParameter fns:sourcesParameter ;
    fnom:implementationParameterPosition 4 .

fns:fpathMappingParameter a fno:Parameter ;
    fno:predicate fns:fpathMapping ;
    fno:type xsd:anyURI .

fns:fpathOutputParameter a fno:Parameter ;
    fno:predicate fns:fpathOutput ;
    fno:type xsd:anyURI .

fns:fpathRMLMapperJarParameter a fno:Parameter ;
    fno:predicate fns:fpathRMLMapperJar ;
    fno:type xsd:anyURI .

fns:fpathRMLMapperTempFolderParameter a fno:Parameter ;
    fno:predicate fns:fpathRMLMapperTempFolder ;
    fno:type xsd:anyURI .

fns:returnOutput a fno:Output ;
    fno:predicate fns:return ;
    fno:type xsd:anyURI .

fns:sourcesParameter a fno:Parameter ;
    fno:predicate fns:sources ;
    fno:type ex:recordStringToAny .
```

## Testing

### SHACL

```bash
shacl v --shapes $WORKFLOWS/function-ontology/shape.ttl --data function_description.ttl > shacl_validation_result.ttl
```

<details>
<summary>
pointers
</summary>

- https://www.w3.org/TR/shacl/#syntax-rule-SHACL-list
- SHACL UCR/uc26: https://www.w3.org/TR/shacl-ucr/#uc26:-rdf:lists-and-ordered-data
- https://www.topquadrant.com/constraints-on-rdflists-using-shacl/
- [`pyshacl` feature matrix](https://github.com/RDFLib/pySHACL/blob/master/FEATURES.md)

</details>

SHACL background
- Property shapes specify constraints about the values that can be reached from a focus node by some path. sh:property associates a shape with a property shape.



<details>
<summary>
debugging fno shape
</summary>

```turtle
👉 sum_002.ttl
Validation Report
Conforms: False
Results (1):
Constraint Violation in NodeConstraintComponent (http://www.w3.org/ns/shacl#NodeConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:maxCount Literal("1", datatype=xsd:integer) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:node fnosh:ListShape ; sh:path fno:expects ]
	Focus Node: ex:sumFunction
	Value Node: [ rdf:_1 ex:intParameterA ; rdf:_2 ex:intParameterB ; rdf:type rdf:List ]
	Result Path: fno:expects
	Message: Value does not conform to Shape fnosh:ListShape
```
</details>

