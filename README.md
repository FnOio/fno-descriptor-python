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
- [ ] SHACL validation of generated FnO descriptions 🚧 WIP
  - [ ] currently, `ListNodeShape` is commented out in `shapes/all.ttl`
- [ ] Use default type map

## Usage example (`main.py`)

A usage example is given in `main.py`.

You can run the example as follows:

```bash
python src/main.py
```