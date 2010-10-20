{% extends "layout.tpl" %}
{% block body %}
	{% for post in posts %}
		<ul>
			<li>
				<div id="post">
					<h3>{{ post.title }}</h3>
				</div>
			</li>
		</ul>
	{% else %}
		<p>Nenhum post.</p>
	{% endfor %}
{% endblock %}

