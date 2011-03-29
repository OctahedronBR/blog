{% extends "layout.tpl" %}
{% block header %}
	<link rel="stylesheet" type="text/css" href="/js/markitup/skins/markitup/style.css" />
	<link rel="stylesheet" type="text/css" href="/js/markitup/sets/bbcode/style.css" />
	<title>{{config.blogname}}{% if post %} | Editando '{{post.title}}' {% endif %}</title>
{% endblock %}
{% block scripts %}
	<script>
		head.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", "/js/form.js", "/js/markitup/jquery.markitup.js", "/js/markitup/sets/bbcode/set.js");
	</script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Editar post</h2>
		<p class="warning"></p>
		<form action="/post/update" method="post">
			<fieldset>
				<input type="hidden" name="key" value="{{ post.key() }}" />
				<label for="title">
					Título: <br />
					<input type="text" name="title" value="{{ post.title }}" /> <br />
				</label>
				<input type="text" name="slug" value="{{ post.slug }}" />
				<button id="slugify">Slugify!</button> <br />
				<label for="desc">
					Descrição do conteúdo: (~160 caracteres / <a href="http://en.wikipedia.org/wiki/Search_engine_optimization" target="_blank">SEO</a>) <br />
					<textarea name="desc" class="large-width">{{ post.desc }}</textarea> <br />
				</label>
				<label for="content">
					Conteúdo: <a href="/help/bbcode" target="_blank">(BBCode?)</a> <br />
					<textarea type="text" name="content" class="large-width">{{ post.coded_content }}</textarea> <br />
				</label>
				<label for="tags">
					Tags: <br />
					<input type="text" name="tags" value="{{ tags }}" /> <br />
				</label>
				<label for="draft">
					<input type="checkbox" name="draft" value="True" {% if draft %}checked{% endif %}/>Rascunho <br />
				</label>
				<input id="submit" type="submit" value="Salvar" />
			</fieldset>
		</form>
	</section>
{% endblock %}
