{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Configurações gerais</title>
{% endblock %}
{% block scripts %}
	<script>
		head.js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", "/js/form.js");
	</script>
{% endblock %}
{% block body %}
	<section class="intern">
		<h2>Configuração</h2>
		{% if saved %}<p class="warning">Configurações salvas</p>{% endif %}
		<form action="/config/save" method="post">
			<fieldset>
				<label for="blogname">
					Nome do Blog: <br />
					<input type="text" id="blogname" name="blogname" value="{{ config.blogname }}" /> <br />
				</label>

				<label for="url">
					URL: <br />
					<input type="text" id="url" name="url" value="{{ config.url }}" /> <br />
				</label>

				<label for="desc">
					Descrição: <br />
					<textarea id="desc" name="desc" >{{ config.desc }}</textarea> <br />
				</label>

				<label for="lang">
					Língua: [e.g.: 'en', 'pt_BR', ...] <br />
					<input type="text" id="lang" name="lang" value="{{ config.lang }}" /> <br />
				</label>

				<input id="submit" type="submit" value="Salvar" />
			</fieldset>
		</form>

		<hr />

		<h3>Links <small>[<a href="/config/add_link">Adicionar novo</a>]</small></h3>
		{% if config.links.count() > 0 %}
		<ul>
		{% for link in config.links %}
			<li>{{link.name}} - {{link.url}} <small>[<a href="/config/remove_link/{{link.name}}" title="Remove">X</a>]</small></li>
		{% endfor %}
		</ul>
		{% else %}
		<p>Nenhum link cadastrado.</p>
		{% endif %}

		<h3>Twitter API <small>[<a href="/config/twitter">Configurar</a>]</small></h3>
		{% if config.access_key and config.access_secret %}
		<dl>
			<dt>Access key:</dt> <dd>{{config.access_key}}</dd>
			<dt>Access secret:</dt> <dd>{{config.access_secret}}</dd>
		</dl>
		{% else %}
		<p>Nenhuma configuração.</p>
		{% endif %}

		<h3>Google Analytics <small>[<a href="/config/analytics">Configurar</a>]</small></h3>
		{% if config.analytics %}
		<dl>
			<dt>Chave:</dt> <dd>{{config.analytics}}</dd>
		</dl>
		{% else %}
		<p>Nenhuma configuração.</p>
		{% endif %}
	</section>
{% endblock %}

