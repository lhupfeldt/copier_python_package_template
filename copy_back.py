#!/bin/env python
"""Copy files from project back to template to assess changes and update template."""

import sys
import os
from pathlib import Path
import shutil


_HERE = Path(__file__).parent.resolve()
_TEMPLATE_NAME = "copier_python_package_template"

def _check_template(subproject_path):
    assert _HERE.name == _TEMPLATE_NAME, "Did template change name?"

    answers_file = subproject_path/".copier-answers.yml"
    with open(answers_file, encoding="utf-8") as caf:
        for ll in caf:
            if ll.startswith("_src_path"):
                if _TEMPLATE_NAME not in ll:
                    raise ValueError(
                        f"Copier subproject in '{subproject_path}' is from another template: {ll}")
                break
        else:
            raise ValueError(f"'_src_path' not found in {subproject_path/answers_file}")


def _copy_back(subproject_path: Path):
    os.chdir(_HERE/"template")
    for root, _, files in os.walk("."):
        root = Path(root)
        for ff in files:
            if '{{' in ff:
                print(f"Ignore {ff}")
                continue

            sub_prj_rel_ff = root/ff.replace(".jinja", "")
            sub_prj_ff = subproject_path/sub_prj_rel_ff
            if sub_prj_ff.exists():
                tgt_ff = root/ff
                print(sub_prj_ff, "->", tgt_ff)
                shutil.copy(sub_prj_ff, tgt_ff)


def main(subproject_path: Path):
    subproject_path = subproject_path.resolve().absolute()
    _check_template(subproject_path)
    _copy_back(subproject_path)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
