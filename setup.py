"""Build hook: copy the top-level ``rules/`` tree into the wheel as ``gangmu_aibom_rules/data``."""

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildPyWithRules(build_py):
    def run(self):
        super().run()
        src = Path(__file__).parent / "rules"
        if not (src / "rulebase.json").is_file():
            raise SystemExit("rules/rulebase.json not found; refusing to build an empty rule pack")
        dest = Path(self.build_lib) / "gangmu_aibom_rules" / "data"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))


setup(cmdclass={"build_py": BuildPyWithRules})
