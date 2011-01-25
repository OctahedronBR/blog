{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Configurações gerais</title>
{% endblock %}
{% block body %}
	<div class="section">
		<h2>Configuração</h2>
		<div class="margin">
			<p class="warning">{% if saved %}<strong>Configuration Saved</strong>{% endif %}</p>
			<form action="/config/save" method="post">
				<fieldset>
					<label for="blogname">
						Nome do Blog: <br />
						<input type="text" name="blogname" value="{{ config.blogname }}" class="normal-width"/> <br />
					</label>
					<label for="url">
						URL: <br />
						<input type="text" name="url" value="{{ config.url }}" class="normal-width"/> <br />
					</label>
					<label for="desc">
						Descrição: <br />
						<textarea name="desc" class="normal-width">{{ config.desc }}</textarea> <br />
					</label>
					<label for="lang">
						Língua: [e.g.: 'en', 'pt_BR', ...] <br />
						<input type="text" name="lang" value="{{ config.lang }}" class="tiny-width"/> <br />
					</label>
					<input id="submit" type="submit" value="Salvar" />
				</fieldset>
			</form>
			<h3>Links <small>[<a href="/config/add_link">Adicionar novo</a>]</small></h3>
			{% if config.links %}
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
		</div>
	</div>
{% endblock %}
{% block scripts %}
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
	<script type="text/javascript" src="/js/form.js"></script>
{% endblock %}

