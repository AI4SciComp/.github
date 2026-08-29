# Organization architecture

AI4SciComp separates research control, scientific-computing implementation, and
engineering policy so that provenance relationships do not become accidental
source dependencies.

```text
research plane             scientific-computing plane       engineering plane
asc-os sidecar  <------>   domain repositories              asc-cmake policy
                           |                                 asc-devtools CLI
                           v
                           released foundations
```

The research sidecar exchanges authored manifests and deterministic generated
context. It does not become a numerical runtime dependency. Specialized
libraries may depend on released public foundation APIs. Foundations do not
depend on specializations.

AI-generated text, code, or experimental suggestions remain proposals until
tests, checksums, source provenance, and domain review make their status
explicit. Repository-local contracts and hand-authored instructions remain
authoritative.
