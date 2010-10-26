{% extends "layout.tpl" %}
{% block body %}
	{% for post in posts %}
		<ul>
			<li>
				<div id="post">
					<h3><a href="/{{ post.slug }}" id="post">{{ post.title }}</a></h3>
					<p>{{ post.html_content }}</p>
				</div>
			</li>
		</ul>
	{% else %}
		<p>Nenhum post.</p>
	{% endfor %}
{% endblock %}

