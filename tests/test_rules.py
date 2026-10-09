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
    assert [f.key for f in rules.formats] == [f.key for f in FORMATS]
    assert [r.key for r in rules.runtimes] == [r.key for r in RUNTIMES]
    for ours, theirs in zip(rules.formats, FORMATS):
        assert ours == theirs, ours.key
    for ours, theirs in zip(rules.runtimes, RUNTIMES):
        assert ours.name == theirs.name, ours.key
        assert ours.patterns[0].startswith(_B), ours.key


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
