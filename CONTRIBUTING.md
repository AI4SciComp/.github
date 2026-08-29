# Contributing to AI4SciComp

Choose the repository that owns the change before opening an issue or pull
request. The [repository boundary guide](docs/repository-boundaries.md) and
[machine-readable map](docs/repository-map.yaml) identify ownership and
dependency direction.

Every contribution should:

1. state a bounded purpose and acceptance evidence;
2. preserve repository-local instructions such as `AGENTS.md` and build
   contracts;
3. keep generated artifacts separate from hand-authored sources;
4. verify AI-assisted output with tests or traceable evidence;
5. disclose relevant data, model, and dependency licenses;
6. avoid credentials, unpublished private data, and secrets;
7. use a focused branch and pull request.

Organization defaults complement repository-local contribution and security
files. A stronger or more specific repository-local policy is authoritative.
Do not replace it with these defaults.

Architecture and governance changes must pass:

```console
python scripts/validate_governance.py
python -m unittest discover -s tests -v
```
