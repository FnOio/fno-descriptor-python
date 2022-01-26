# fno-descriptor-python

Convenience tool for creating FnO function & parameter descriptions from Python functions.

Manually describing functions can be time-consuming and error-prone.
The `fno-descriptor-python` enables you to quickly define a function signature
in Python,
and generates its corresponding FnO descriptions by leveraging Python
type-hinting.

## Supported

- [x] `fno:Parameter`
- [x] `fno:ParameterMapping`
- [x] `fno:Output`
- [x] `fno:ReturnMapping`
- [ ] `fno:Function`
- [ ] `fno:Mapping` 
- [ ] `fno:MethodMapping`
- [ ] Add `func.__doc__` as `doap:description`

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
function_description_graph = fnod.create_description_graph(
    executeRMLMapper, type_map)
function_description_graph.print()
function_description_graph.serialize(destination='params_and_outputs.ttl', format='turtle')
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
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

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