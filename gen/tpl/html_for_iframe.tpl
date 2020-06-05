{# HTML output for iframe
we don't need so much space around edges of notebook

This is based on the default HTML template ('full.tpl').
 #}
{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{# 
  begin originally in <head>
#}
{%- block header -%}
<!DOCTYPE html>
<html>
<head>
{%- block html_head -%}

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

{% block ipywidgets %}
{%- if "widgets" in nb.metadata -%}
<script>
(function() {
  function addWidgetsRenderer() {
    var mimeElement = document.querySelector('script[type="application/vnd.jupyter.widget-view+json"]');
    var scriptElement = document.createElement('script');
    var widgetRendererSrc = '{{ resources.ipywidgets_base_url }}@jupyter-widgets/html-manager@*/dist/embed-amd.js';
    var widgetState;

    // Fallback for older version:
    try {
      widgetState = mimeElement && JSON.parse(mimeElement.innerHTML);

      if (widgetState && (widgetState.version_major < 2 || !widgetState.version_major)) {
        widgetRendererSrc = '{{ resources.ipywidgets_base_url }}jupyter-js-widgets@*/dist/embed.js';
      }
    } catch(e) {}

    scriptElement.src = widgetRendererSrc;
    document.body.appendChild(scriptElement);
  }

  document.addEventListener('DOMContentLoaded', addWidgetsRenderer);
}());
</script>
{%- endif -%}
{% endblock ipywidgets %}

{# 
  includes everything needed to look like normal Jupyter style
  Bootstrap, syntax highlighting, etc.
  we don't want it since we want to have our own style
#}
{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 2px;
  margin: 0;
}

{%- if resources.global_content_filter.no_prompt-%}
div#notebook-container{
  padding: 6ex 12ex 8ex 12ex;
}
{%- endif -%}

@media print {
  div.cell {
    display: block;
    page-break-inside: avoid;
  } 
  div.output_wrapper { 
    display: block;
    page-break-inside: avoid; 
  }
  div.output { 
    display: block;
    page-break-inside: avoid; 
  }
}
</style>

{# 
  nbconvert's macro to load mathjax 
  may not be necessary since I do my own mathjax loading? I could make the config match
#}
{{- mathjax() }}
{%- endblock html_head -%}
{# </head> #}
{%- endblock header -%}
{#
  end originally in head
#}

{% block body %}
<body>
  {# <div tabindex="-1" id="notebook" class="border-box-sizing"> #}
    <div class="container-fluid" id="notebook-container"><!-- container -> container-fluid to fill whole area -->
{{ super() }}
    </div>
  {# </div> #}
</body>
{%- endblock body %}

{# 
  probably don't need this 
  doesn't seem like it usually has anything in it
#}
{% block footer %}
{{ super() }}
</html>
{% endblock footer %}
