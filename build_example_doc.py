PROGRAM_DESCRIPTION = """
Given a target directory, this program:
- finds a single target Markdown file named <name>_template.md
- searches all code files for
/*** CODE FRAGMENT fragment name ***/
....
code fragment
....
/*** END CODE FRAGMENT ***/
building a dict of fragment name -> code fragment
- takes code fragments and subs them in to markdown template
  using Jinja2 syntax {{ ex_name }}
"""

SOURCE_FILE_EXTENSIONS = [".html", ".js"]

CODE_FRAGMENT_RE = (
r"""\/\*\*\* CODE FRAGMENT (?P<fragment_name>.*?) \*\*\*\/
(?P<fragment>.*?)
\s*\/\*\*\* END CODE FRAGMENT \*\*\*\/"""
)

import argparse
import itertools
from pathlib import Path
import re
import sys

import jinja2

def dedent(fragment):
    if "\t" in fragment:
        sys.stderr.write("Nae tabs allowed")
        sys.exit(-1)
    dedent_length = len(fragment) - len(fragment.lstrip(" "))
    return "\n".join(line[dedent_length:] for line in fragment.split("\n"))

parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument(
    "target_dir", metavar="TARGET_DIR", type=Path, nargs=1,
    help="The target directory for the program."
)
args = parser.parse_args()
target_dir = args.target_dir[0]

if not target_dir.exists() or not target_dir.is_dir():
    sys.stderr.write("The path specified must exist and be a directory")
    sys.exit(-1)

template_files = list(target_dir.glob("*_template.md"))
assert len(template_files) == 1, "Found no or more than one template file: "+str(template_files)
template_file = template_files[0]
output_filename = str(template_file)[:-12]+".md"

fragments = {}
source_files_iterators = (target_dir.rglob("*"+ext) for ext in SOURCE_FILE_EXTENSIONS)
for source_file in itertools.chain(*source_files_iterators):
    if not source_file.is_file():
        continue
    with open(source_file) as f:
        text = f.read()
        matches = list(re.finditer(CODE_FRAGMENT_RE, text, re.DOTALL))
        print(matches)
        current_file_fragments = {
            m["fragment_name"]: dedent(m["fragment"])
            for m in matches
        }
        fragments.update(current_file_fragments)

template = jinja2.Template(open(template_file).read())
render_out = template.render(fragments)
env = jinja2.Environment()
compiled = env.compile(render_out)

with open(output_filename, "w") as f_out:
    f_out.write(template.render(fragments))