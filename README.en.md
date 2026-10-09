# gangmu-aibom-rules

The free AIBOM rule base for [gangmu](https://github.com/GANGMU-SBOM/gangmu): which model file formats and
inference runtimes `gangmu aibom` looks for in firmware and source. The tables used to live in the tool's
code; as data they can be extended with a small YAML pull request, with no tool release.

```bash
# Not on PyPI yet: install from source (gangmu 0.9.0 or later; use git main until it is released)
pip install git+https://github.com/GANGMU-SBOM/gangmu.git@main
pip install git+https://github.com/GANGMU-SBOM/gangmu-aibom-rules.git
gangmu aibom firmware/                 # installed packs of kind "aibom" are read automatically
gangmu aibom firmware/ --rules rules/  # or point at a directory while editing
```

`rules/formats/model-formats.yaml` and `rules/runtimes/inference-runtimes.yaml` are an exact export of the
tool's built-in tables; `tests/test_rules.py` compares them so the two cannot drift. A rule with the key of a
built-in replaces it; a new key adds one.

**A model format** (`formats/*.yaml`, a list under `formats:`): `key`, `name`, `suffixes` (extensions with the
dot), an optional `magic` (`offset` plus `ascii` or `hex`; a match is "found by file signature") and an optional
`note`. Give at least one of `suffixes` and `magic`.

**An inference runtime** (`runtimes/*.yaml`, a list under `runtimes:`): `key`, `name`, and `patterns`, regular
expressions for identifiers. The scan puts the identifier boundary in front, so do not write one.

A runtime is recognised by an identifier in a source file; that does not mean it is in the build. Detections that
need to read content (a TensorFlow Lite model compiled into a C array, the architecture in a GGUF header) stay
in the tool. Rules: CDLA-Permissive-2.0; packaging code: Apache-2.0. See [CONTRIBUTING.md](CONTRIBUTING.md).
