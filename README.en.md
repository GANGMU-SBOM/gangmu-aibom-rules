# gangmu-aibom-rules

The free AIBOM rule base for [gangmu](https://github.com/GANGMU-SBOM/gangmu): which model file formats and
inference runtimes `gangmu aibom` looks for in firmware and source. The tables used to live in the tool's
code; as data they can be extended with a small YAML pull request, with no tool release.

```bash
# This pack is not on PyPI yet: install it from source (needs gangmu 0.9.0 or later)
pip install gangmu-sbom
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

Beyond the built-in tables the pack adds formats (ncnn `.param` and ONNX Runtime `.ort`, both by file signature; TNN,
Tengine, Kendryte kmodel, Hailo HEF, PaddlePaddle, Caffe and pickle/joblib by extension) and runtimes (OpenVINO,
TensorRT, Paddle Lite, TNN, MACE, nncase, Tengine, XNNPACK, Arm NN, HailoRT, whisper.cpp, LibTorch, LiteRT). Identifiers and
magic bytes were checked against the upstream sources. kmodel and HEF have identifier constants upstream but no sample file
to confirm their byte order, so they are matched by extension only.

Three more runtime files cover NPU and microcontroller stacks (Coral Edge TPU, Arm Ethos-U, Arm Compute Library, NNAPI, OpenHarmony NNRt, Qualcomm
QNN, Ascend CANN, Sophgo cviruntime, MindSpore Lite, TinyMaix, AIfES, FANN, ESP-NN, OpenCV DNN, emlearn), the Python entry points that load a model
(ONNX Runtime, Transformers, `torch.load`/`torch.jit.load`, TFLite/LiteRT, Keras, Ultralytics), and the host names of hosted model APIs (OpenAI,
Anthropic, Gemini, Alibaba DashScope, Zhipu, Baidu Qianfan). Added formats: ggml (magic `lmgg`, i.e. `0x67676d6c` little-endian), and
`.espdl`, `.bmodel`, `.ptl` by extension.

**How this differs from the SBOM rules.** This pack says which models, inference stacks and hosted endpoints a tree uses. Which open-source
library and version a directory is, and its CVEs, is the SBOM's job (gangmu-rules). So runtime rules hold identifiers only (functions, types,
headers, host names), never directory markers, hashes or version probes. The scan reads source files, not `.json` or `.yaml`, so a host name kept
in a config file is not seen.

A runtime is recognised by an identifier in a source file; that does not mean it is in the build. Detections that
need to read content (a TensorFlow Lite model compiled into a C array, the architecture in a GGUF header) stay
in the tool. Rules: CDLA-Permissive-2.0; packaging code: Apache-2.0. See [CONTRIBUTING.md](CONTRIBUTING.md).
