{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}


{%- block header -%}
<!DOCTYPE html>
<html>
<head>
{%- block html_head -%}
<meta charset="utf-8" />
{% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
<title>{{nb_title}}</title>

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

{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 8px;
}
div#notebook {
  overflow: visible;
  border-top: none;
}
{%- if resources.global_content_filter.no_prompt-%}
div#notebook-container{
  padding: 6ex 12ex 8ex 12ex;
  max-width: 900px;
  -webkit-box-shadow: none;
  box-shadow: none;
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

div.output_png, div.output_html {
    margin: 0px auto;
}

h1.nb_title {
    font-size: 3.5em;
}

</style>

<!-- Custom stylesheet, it must be in the same directory as the html file -->
<link rel="stylesheet" href="custom.css">

<!-- Loading mathjax macro -->
{{ mathjax() }}
{%- endblock html_head -%}
</head>
{%- endblock header -%}

{% block body %}
<body>
  <div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container">
    {% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
    {% set nb_author = nb.metadata.get('author', '') %}
    <h1 class="nb_title">{{ nb_title | replace("_", " ") | capitalize }}</h1>
    {% if nb_author %}<h3 class="nb_author">{{ nb_author }}</h3>{% endif %}
    <hr />
{{ super() }}
    </div>
  </div>
</body>
{%- endblock body %}

{% block data_png %}
<figure>
{{ super() }}
{% if cell.metadata.caption %}
<figcaption>{{ cell.metadata.caption }}</figcaption>
{% endif %}
</figure>
{% endblock data_png %}

{% block footer %}
{{ super() }}
</html>
{% endblock footer %}