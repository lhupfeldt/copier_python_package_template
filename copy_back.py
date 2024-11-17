#!/bin/env python
"""Copy files from project back to template to assess changes and update template."""

import sys
import os
from pathlib import Path
import shutil


_HERE = Path(__file__).parent.resolve()


def main(subproject_path: Path):
    answers_file = subproject_path/".copier-answers.yml"
    with open(answers_file, encoding="utf-8") as caf:
        for ll in caf:
            if ll.startswith("_src_path"):
                if "copier_python_package_template" in ll:
                    break
        else:
            raise ValueError(f"'_src_path' not found in {answers_file}")

    os.chdir(_HERE)
    tmpl_dir = Path("template")

    for root, _, files in os.walk(tmpl_dir):
        root = Path(Path(root).name)
        for ff in files:
            if '{{' in ff:
                print(f"Ignore {ff}")
                continue

            sub_prj_rel_ff = root/ff.replace(".jinja", "")
            sub_prj_ff = subproject_path/sub_prj_rel_ff
            if sub_prj_ff.exists():
                tgt_ff = tmpl_dir/root/ff
                print(sub_prj_ff, "->", tgt_ff)
                shutil.copy(sub_prj_ff, tgt_ff)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
