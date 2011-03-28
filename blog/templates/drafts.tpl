{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | Rascunhos </title>
{% endblock %}
{% block body %}
	{% for post in posts %}
	<article>
		<h2>{{ post.title }}</a> [<a href="/post/edit/{{ post.key() }}" id="edit">Editar</a> | <a href="/publish/{{ post.key() }}" id="edit">Publicar</a> | <a href="/remove/{{ post.key() }}" id="edit">Remover</a>]</h2>
		<h6>Publicado em {{ post.when.strftime("%d/%m/%Y") }} por {{ post.author.nickname() }}</h6>
		{{ post.html_content }}
		<footer>
			Tags: 
			{% for tag in post.tags %}
			<a href="/tag/{{ tag }}">{{ tag }}</a>
			{% else %}
			Nenhuma
			{% endfor %}
	</footer>
	{% else %}
	<article>
		<h2>Nenhum post {% if user %}[<a href="/post/new" id="new">Criar</a>]{% endif %}</h2>
	</article>
	{% endfor %}
{% endblock %}

