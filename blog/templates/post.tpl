{% extends "layout.tpl" %}
{% block body %}
	<div id="post">
		<h3>{{ post.title }} {% if user %}<a href="/post/edit/{{ post.key() }}">Editar{% endif %}</h3>
		<h4>{{ post.author.nickname() }}</h4>
		<p>{{ post.content }}</p>
	</div>
{% endblock %}

