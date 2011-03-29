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
