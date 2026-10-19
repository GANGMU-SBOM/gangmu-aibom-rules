"""The pack loads, and it says what gangmu's built-in tables say."""
import pytest

pytest.importorskip("gangmu.aibom")
from gangmu.aibom import (FORMATS, RUNTIMES, _B, aibom_roots, load_aibom_roots,  # noqa: E402
                          scan_aibom)

import gangmu_aibom_rules  # noqa: E402


def _rules():
    return load_aibom_roots(aibom_roots([str(gangmu_aibom_rules.path())]))


def test_the_manifest_is_of_kind_aibom():
    from gangmu.core.packs import check_manifest, read_manifest
    manifest = read_manifest(gangmu_aibom_rules.path())
    assert manifest["kind"] == "aibom"
    check_manifest(gangmu_aibom_rules.path(), manifest)


def test_every_rule_loads_and_matches_the_built_in_tables():
    rules = _rules()
    # The pack starts with the built-ins, in their order; anything after them is an addition.
    assert [f.key for f in rules.formats][:len(FORMATS)] == [f.key for f in FORMATS]
    assert [r.key for r in rules.runtimes][:len(RUNTIMES)] == [r.key for r in RUNTIMES]
    for ours, theirs in zip(rules.formats, FORMATS):
        assert ours == theirs, ours.key
    for ours, theirs in zip(rules.runtimes, RUNTIMES):
        assert ours.name == theirs.name, ours.key
    for rt in rules.runtimes:
        assert rt.patterns[0].startswith(_B), rt.key


def test_keys_are_unique():
    rules = _rules()
    for group in (rules.formats, rules.runtimes):
        keys = [x.key for x in group]
        assert len(keys) == len(set(keys))


@pytest.mark.parametrize("name, content, runtime", [
    ("kws.tflite", b"\x1c\0\0\0TFL3" + b"\0" * 16, None),
    ("a.cc", b'#include "tensorflow/lite/micro/micro_interpreter.h"\n', "tflite-micro"),
    ("b.c", b"arm_fully_connected_s8(0);\n", "cmsis-nn"),
    ("c.c", b"llama_model_load_from_file(p, q);\n", "llama-cpp"),
])
def test_the_pack_finds_what_the_built_ins_find(tmp_path, name, content, runtime):
    (tmp_path / name).write_bytes(content)
    result = scan_aibom(tmp_path, rules=_rules())
    if runtime:
        assert runtime in {h.runtime.key for h in result.runtimes}
    else:
        assert [m.fmt.key for m in result.models] == ["tflite"]


# One file per added format. Magic bytes come from the upstream source named in the comment;
# a format with only an extension is recognised by name and reported as such.
NEW_FORMATS = [
    ("net.param", b"7767517\n3 3\nInput data 0 1 data\n", "ncnn-param", True),    # ncnn net.cpp
    ("renamed.txt", b"7767517\n3 3\n", "ncnn-param", True),
    ("m.ort", b"\x1c\0\0\0ORTM" + b"\0" * 16, "onnxruntime-ort", True),       # ort.fbs file_identifier
    ("m.tnnmodel", b"\0" * 8, "tnn", False),
    ("m.tnnproto", b"\0" * 8, "tnn", False),
    ("m.tmfile", b"\0" * 8, "tengine", False),
    ("m.kmodel", b"\0" * 8, "nncase-kmodel", False),
    ("m.hef", b"\0" * 8, "hailo-hef", False),
    ("inference.pdmodel", b"\0" * 8, "paddle", False),
    ("inference.pdiparams", b"\0" * 8, "paddle", False),
    ("net.caffemodel", b"\0" * 8, "caffe", False),
    ("clf.pkl", b"\x80\x04.", "pickle", False),
    ("clf.joblib", b"\x80\x04.", "pickle", False),
]


@pytest.mark.parametrize("name, content, key, by_signature", NEW_FORMATS)
def test_added_formats_are_found(tmp_path, name, content, key, by_signature):
    (tmp_path / name).write_bytes(content)
    models = scan_aibom(tmp_path, rules=_rules()).models
    assert [(m.fmt.key, m.verified) for m in models] == [(key, by_signature)]


def test_a_param_file_that_is_not_ncnn_is_left_alone(tmp_path):
    (tmp_path / "gromacs.param").write_bytes(b"; not a model\n")
    assert scan_aibom(tmp_path, rules=_rules()).models == []


# One source line per added runtime, using an identifier from the upstream project.
NEW_RUNTIMES = [
    ("a.cc", b"ov::Core core;\n", "openvino"),
    ("a.c", b"ov_core_create(&core);\n", "openvino"),
    ("a.cc", b"auto* rt = nvinfer1::createInferRuntime(logger);\n", "tensorrt"),
    ("a.cc", b'#include "NvInferRuntime.h"\n', "tensorrt"),
    ("a.cc", b"auto p = paddle::lite_api::CreatePaddlePredictor<paddle::lite_api::MobileConfig>(c);\n", "paddle-lite"),
    ("a.cc", b"auto net = TNN_NS::TNN();\n", "tnn"),
    ("a.cc", b"mace::MaceEngine engine;\n", "mace"),
    ("a.cc", b"nncase::runtime::interpreter interp;\n", "nncase"),
    ("a.c", b"init_tengine();\n", "tengine"),
    ("a.c", b"xnn_initialize(NULL);\n", "xnnpack"),
    ("a.cc", b"armnn::IRuntimePtr rt = armnn::IRuntime::Create(options);\n", "arm-nn"),
    ("a.c", b"hailo_create_vdevice(NULL, &vdevice);\n", "hailort"),
    ("a.c", b"ctx = whisper_init_from_file_with_params(path, p);\n", "whisper-cpp"),
    ("a.cc", b'auto m = torch::jit::load("m.pt");\n', "libtorch"),
    ("a.cc", b"LiteRtCreateModelFromFile(path, &model);\n", "litert"),
]


@pytest.mark.parametrize("name, content, runtime", NEW_RUNTIMES)
def test_added_runtimes_are_found(tmp_path, name, content, runtime):
    (tmp_path / name).write_bytes(content)
    assert runtime in {h.runtime.key for h in scan_aibom(tmp_path, rules=_rules()).runtimes}


def test_every_added_rule_has_a_sample():
    rules = _rules()
    assert {f.key for f in rules.formats[len(FORMATS):]} == {k for _, _, k, _ in NEW_FORMATS}
    assert {r.key for r in rules.runtimes[len(RUNTIMES):]} == {k for _, _, k in NEW_RUNTIMES}


@pytest.mark.parametrize("line", [
    b"int tnn_core = 1;\n",                 # not TNN_NS::TNN
    b"struct tensorrt_like_thing;\n",
    b"void whisper_loud(void);\n",
    b"int my_init_tengine_x;\n",
    b'run("models/whisper.hef");\n',        # "whisper.h" is a prefix of "whisper.hef"
])
def test_lookalike_identifiers_are_not_runtimes(tmp_path, line):
    (tmp_path / "a.c").write_bytes(line)
    assert scan_aibom(tmp_path, rules=_rules()).runtimes == []


def test_wheel_carries_the_rules(tmp_path):
    """A built wheel must contain the rule tree, or an installed pack is empty."""
    import subprocess
    import sys
    import zipfile
    from pathlib import Path

    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "dist"
    subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", str(out), str(repo)],
                   check=True, capture_output=True)
    names = zipfile.ZipFile(next(out.glob("*.whl"))).namelist()
    assert "gangmu_aibom_rules/data/rulebase.json" in names
    assert "gangmu_aibom_rules/data/formats/model-formats.yaml" in names
    assert "gangmu_aibom_rules/data/runtimes/inference-runtimes.yaml" in names


def test_the_three_places_that_name_the_version_agree():
    """pyproject.toml, the package and the manifest were once 2026.10.9, 2026.10.9 and
    2026.10.15; gangmu reports the manifest's, pip the package's."""
    import json
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    declared = re.search(r'^version = "([^"]+)"', (root / "pyproject.toml").read_text(), re.M)
    manifest = json.loads((root / "rules" / "rulebase.json").read_text())["version"]
    assert declared and declared.group(1) == gangmu_aibom_rules.__version__ == manifest
