"""
Convert notebooks to md format but insert JavaScript elements.

We don't define a custom HTML exporter, because want to be able to take 
advantage of existing solutions like nbinteract for special situations.

"""

import nbconvert
import nbformat
from traitlets.config import Config


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

# loop through cells to collect text
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

    for output in outputs:

        if output.output_type == "stream":
            print(output.text)
        else:
            output_data_keys = output.data.keys()
            try:
                print(output.data["text/plain"])
            except:
                print(f"`output.data.keys()`: {output_data_keys}")

    print()