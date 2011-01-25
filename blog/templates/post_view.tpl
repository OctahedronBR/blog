{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | {{post.title}} </title>
		<meta name="keywords" content="{{', '.join(post.tags)}}" />
		{% if post.desc %}<meta name="description" content="{{ post.desc }}" />{% endif %}
{% endblock %}
{% block body %}
	<div class="post">
		<h2>{{ post.title }} {% if user %}[<a href="/post/edit/{{ post.key() }}">Editar</a> | <a href="/remove/{{ post.key() }}">Remover</a>]{% endif %}</h2>
		<h3>_Publicado em {{ post.when.strftime("%d/%m/%Y") }} por {{ post.author.nickname() }}</h3>
		<div class="text">
			{{ post.html_content }}
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
{% endblock %}

