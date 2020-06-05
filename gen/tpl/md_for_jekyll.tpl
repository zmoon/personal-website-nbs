{# Jupyter notebook as Markdown for inclusion in web site
via a static site generator.

based on nbconvert template from:
  https://predictablynoisy.com/jekyll-markdown-nbconvert 
#}
{% extends 'markdown.tpl' %}

<!-- add div for input area -->
{% block input %}
<div class="input_area" markdown="1">
{{ super() }}
</div>
{% endblock input %}

<!-- remove indentations for output text and add div classes  -->
{% block stream %}
{:.output_stream}
```
{{ output.text }}```
{% endblock stream %}

<!-- ignoring output data_text for now. see above link to put it back in... -->
{% block data_text %}
{% endblock data_text %}

{% block traceback_line  %}
{:.output_traceback_line}
```
{{ line | strip_ansi }}
```
{% endblock traceback_line  %}

<!-- tell Jekyll not to render HTML output blocks as markdown -->
{% block data_html %}
<div markdown="0">
{{ output.data['text/html'] }}
</div><!-- markdown="0" -->
{% endblock data_html %}

<!-- tell Jekyll not to render embedded Javascript blocks as markdown -->
{% block data_js %}
<div markdown="0">
<script type="text/javascript">
{{ output.data['application/javascript'] }}
</script>
</div><!-- markdown="0" -->
{% endblock data_js %}
