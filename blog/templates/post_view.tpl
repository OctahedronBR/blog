{% extends "layout.tpl" %}
{% block header %}
		<title>{{config.blogname}} | {{post.title}} </title>
		<meta name="keywords" content="{{', '.join(post.tags)}}" />
		{% if post.desc %}<meta name="description" content="{{ post.desc }}" />{% endif %}
{% endblock %}
{% block body %}
	<article>
		<h2>{{ post.title }} {% if user %}[<a href="/post/edit/{{ post.key() }}">Editar</a> | <a href="/remove/{{ post.key() }}">Remover</a>]{% endif %}</h2>
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
{% endblock %}

{% block scripts_bottom %}
	{% if config.analytics %}
		<script>
			var _gaq=[["_setAccount","{{ config.analytics }}"],["_trackPageview"]];
			(function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];g.async=1;
			g.src=("https:"==location.protocol?"//ssl":"//www")+".google-analytics.com/ga.js";
			s.parentNode.insertBefore(g,s)}(document,"script"));
		</script>
	{% endif %}
{% endblock %}
