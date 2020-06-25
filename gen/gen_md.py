"""
Convert notebooks to md format but insert JavaScript elements.

We don't define a custom HTML exporter, because want to be able to take 
advantage of existing solutions like nbinteract for special situations.

"""

from pathlib import Path

import nbconvert
import nbformat
from traitlets.config import Config
import yaml


c = Config()
c.HTMLExporter.preprocessors = ["nbconvert.preprocessors.ExtractOutputPreprocessor"]
c.MarkdownExporter.preprocessors = ["nbconvert.preprocessors.ExtractOutputPreprocessor"]

html_exporter = nbconvert.HTMLExporter(config=c)
html_exporter.template_file = 'basic'

md_exporter = nbconvert.MarkdownExporter(config=c)


# test

as_version = nbformat.NO_CONVERT

nb = nbformat.read("../nb-src/sample_jnb_1.ipynb", as_version=as_version)

# execute nb?

# HTML exporter output
(_, resources_html) = html_exporter.from_notebook_node(nb)

# MD exporter output
tpl = "./tpl/md_for_jekyll.tpl"
(body, resources) = md_exporter.from_notebook_node(nb, template_file=tpl)



def update_gist(nb_path):
    """Update an existing nb Gist."""
    pass


def create_gist(nb_path):
    """Create GH Gist for Notebook, in order to run on Binder."""
    pass


def header_links(nb_path, gistID=None):
    """Create and return md header links."""

    nb_name = nb_path.name
    src = f"{nb_path.stem}.py"  # assume Jupytext Python script is the nb source

    if gistID is None:
        gistID = "{gistID}"

    badge_nbviewer = "https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg"
    badge_binder = "https://mybinder.org/badge_logo.svg"

    username = "zmoon92"

    return f"""
[![NBViewer](badge_nbviewer)](https://nbviewer.jupyter.org/gist/{username}/{gistID})
(view rendered on Jupyter nbviewer)

[![Binder](badge_binder)](https://mybinder.org/v2/gist/{username}/{gistID}/)
(open the notebook directly via MyBinder)

[View source](https://github.com/zmoon92/personal-website-nbs/blob/master/nb-src/{src})
    """.strip()


# currently testing this with:
# python gen_md.py > tmp/test.md

# test header_links
p_nb = Path("../nb-src/sample_jnb_1.ipynb")
print(header_links(p_nb))

# loop through cells to collect text
nb_stem = p_nb.stem
js_paths = []  # collect these to add to YFM (and then include in the layout)
lang = nb.metadata.language_info.name
for i, cell in enumerate(nb.cells):
    print(f"<!-- Cell {i+1:02d} ({i:02d})\n---------------->")
    print("<!-- source -->")
    if cell.cell_type == "markdown":
        print(cell.source)
    elif cell.cell_type == "code":
        print(f"```{lang}\n{cell.source}\n```")

    outputs = cell.get("outputs", [])
    if outputs:
        print("<!-- output(s) -->")

    ext = ""
    for j, output in enumerate(outputs):
        
        print(f"* output {j+1} ({j}):\n  - `output_type`: `{output.output_type!r}`")

        # need to catch other text types here like traceback and data_text ?
        if output.output_type == "stream":
            print(f"```\n{output.text.strip()}\n```")
        else:
            output_data_keys = output.data.keys()
            print(f"  - `output.data.keys()`: `{output_data_keys!r}`")
            try:
                textplain = output.data["text/plain"]  # plaintext repr of the object
                print("<!-- plaintext repr of displayed output -->")
                print(f"```\n{textplain}\n```")
            except KeyError:  # no plaintext repr
                pass

            # save to file
            if "text/html" in output_data_keys:
                ext = "html"
            elif "application/javascript" in output_data_keys:
                ext = "js"
            elif not output_data_keys:  # the holoviews plot creates an empty output like this
                continue
            else:
                raise NotImplementedError(f"Not sure what to do with {output_data_keys!r}")

            fp = Path(f"./tmp/output_{i+1:02d}_{j+1:02d}.{ext}")

            with open(fp, "wb") as f:
                f.write("\n\n".join(output.data[k] 
                    for k in output_data_keys if k not in ("text/plain")
                    ).encode("utf-8"))

            # include or note the paths of output files
            if ext == "html":
                print(f"\n{{% include md_nbs/{nb_stem}/{fp.name} %}}")
            elif ext == "js":
                # print(f'<script src="assets/js/{nb_stem}/{fp.name}"></script>')
                js_paths.append(f"assets/js/{nb_stem}/{fp.name}")


    print()

# YFM
# can store some things in the YFM of the Jupytext script
# but need to decide on standards
yfm = {
    "scripts": js_paths
}
print(f"""
YFM (will be at top...):

```yaml
{yaml.dump(yfm)}
```
""")
