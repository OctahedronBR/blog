{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | {{post.title}} </title>
		<meta name="keywords" content="{{', '.join(post.tags)}}" />
		{% if post.desc %}<meta name="description" content="{{ post.desc }}" />{% endif %}
{% endblock %}
{% block body %}
	<article>
		<header>
		<h2>{{ post.title }} {% if user %}[<a href="/post/edit/{{ post.key() }}">Editar</a> | <a href="/remove/{{ post.key() }}">Remover</a>]{% endif %}</h2>
		<h6>Publicado em {{ post.when.strftime("%d/%m/%Y") }} por {{ post.author.nickname() }}</h6>
		</header>
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
{% endblock %}

<!-- por google analytics -->
blog.octa -> UA-22233247-2
tech ->  UA-22233247-3 

