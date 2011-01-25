{% extends "layout.tpl" %}
{% block header %}
		<title>{{ config.blogname }} | {{ config.desc }}</title>
		<meta name="description" content="{{config.desc}}" />
		<meta name="keywords" content="{% for post in posts %}{{', '.join(post.tags)}}, {% endfor %}" />
{% endblock %}
{% block body %}
	{% for post in posts %}
	<div class="post">
		<h2><a href="/{{ post.slug }}">{{ post.title }}</a> {% if user %}[<a href="/post/edit/{{ post.key() }}">Editar</a> | <a href="/remove/{{ post.key() }}">Remover</a>]{% endif %}</h2>
		<h3>_Publicado em {{ post.when.strftime("%d/%m/%Y") }} por {{ post.author.nickname() }}</h3>
		<div class="text">
			<p>{{ post.html_content }}</p>
		</div>
		<div class="footer">
			<ul>
				<li><strong>_Tags:</strong></li>
				{% for tag in post.tags %}
				<li><a href="/tag/{{ tag }}">{{ tag }}</a></li>
				{% else %}
				<li>Nenhuma</li>
				{% endfor %}
			</ul>
		</div>
	</div>
	{% else %}
	<div class="section">
		<h2>Nenhum post {% if user %}[<a href="/post/new" class="new">Criar</a>]{% endif %}</h2>
	</div>
	{% endfor %}
{% endblock %}

