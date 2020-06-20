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
