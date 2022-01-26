# fno-descriptor-python

Convenience tool for creating FnO function & parameter descriptions from Python functions.

## Usage example (`main.py`)

The example describes the following Python function
```python
# Python function to describe
class Iri:
    pass

# Usage example: create FnO description graph for given Python function
# 

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
```

You can run the example as follows:

```bash
python src/main.py
```

### Output

```Turtle
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

fns:returnOutputMapping a fno:DefaultReturnMapping,
        fno:ReturnMapping ;
    fnom:functionOutput fns:returnOutput .

fns:fpathMappingParameter a fno:Parameter ;
    fno:predicate "fpathMapping" ;
    fno:type xsd:anyURI .

fns:fpathOutputParameter a fno:Parameter ;
    fno:predicate "fpathOutput" ;
    fno:type xsd:anyURI .

fns:fpathRMLMapperJarParameter a fno:Parameter ;
    fno:predicate "fpathRMLMapperJar" ;
    fno:type xsd:anyURI .

fns:fpathRMLMapperTempFolderParameter a fno:Parameter ;
    fno:predicate "fpathRMLMapperTempFolder" ;
    fno:type xsd:anyURI .

fns:returnOutput a fno:Output ;
    fno:predicate "return" ;
    fno:type xsd:anyURI .
```