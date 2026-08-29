# AI4SciComp organization governance

This repository is the source of truth for the AI4SciComp organization
profile, repository boundaries, research lifecycle, machine-readable
repository map, and default community-health files.

Repository-local policies take precedence when they are stronger or more
specific. The repository map describes organization relationships; it is not a
runtime service or a discovery dependency for developer tools.

Validate a change with:

```console
python scripts/validate_governance.py
python -m unittest discover -s tests -v
```

See [the organization profile](profile/README.md), [repository
boundaries](docs/repository-boundaries.md), and [contribution
guidance](CONTRIBUTING.md).
