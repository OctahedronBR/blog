{% extends "layout.tpl" %}
{% block header %}
		<title>{{ config.blogname }} | {{ config.desc }}</title>
		<meta name="description" content="{{config.desc}}" />
		<meta name="keywords" content="{% for post in posts %}{{', '.join(post.tags)}}, {% endfor %}" />
{% endblock %}
{% block body %}
	{% for post in posts %}
	<article>
		<h2><a href="/{{ post.slug }}">{{ post.title }}</a> {% if user %}[<a href="/post/edit/{{ post.key() }}">Editar</a> | <a href="/remove/{{ post.key() }}">Remover</a>]{% endif %}</h2>
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
	</article>
	{% else %}
	<article>
		<h2>Nenhum post {% if user %}[<a href="/post/new" class="new">Criar</a>]{% endif %}</h2>
	</article>
	{% endfor %}
{% endblock %}

<!-- por google analytics -->
