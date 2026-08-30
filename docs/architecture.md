# Organization architecture

AI4SciComp separates research control, scientific-computing implementation, and
engineering policy so that provenance relationships do not become accidental
source dependencies.

```text
                              asc-py
                            /        \
                           v          v
                      asc-xde      asc-no
                         |             ^
                         +-- PDE artifacts --+

asc-os -- development sidecar --> asc-py / asc-xde / asc-no
asc-cpp -- independent C++ performance foundation --> future optional providers
```

The research sidecar exchanges authored manifests and deterministic generated
context. It does not become a numerical runtime dependency. Specialized
libraries may depend on released public foundation APIs. Foundations do not
depend on specializations.

Python is the primary language for general scientific abstractions, algorithm
development, backend portability, data workflows, and machine-learning
integration. ASC Python owns the domain-neutral array, backend, conversion,
random-state, configuration, logging, error, data, and safe-persistence
contracts. ASC XDE specializes those contracts for differential equations and
artifact generation; ASC NO specializes them for neural operators and model
workflows.

ASC C++ is not a mandatory parent of either Python library. It remains the
route for standalone high-performance components and future task-specific
native providers after profiling. Such providers must preserve and be tested
against the Python reference semantics.

AI-generated text, code, or experimental suggestions remain proposals until
tests, checksums, source provenance, and domain review make their status
explicit. Repository-local contracts and hand-authored instructions remain
authoritative.
