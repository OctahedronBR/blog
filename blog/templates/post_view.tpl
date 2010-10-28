{% extends "layout.tpl" %}
{% block body %}
	<div class="post">
		<h2>{{ post.title }} {% if user %}[<a href="/post/edit/{{ post.key() }}" id="edit">Editar</a>]{% endif %}</h3>
		<h3>_Publicado em {{ post.when.strftime("%d/%m/%Y") }} por {{ post.author.nickname() }}</h3>
		<div id="text">
			<p>{{ post.html_content }}</p>
		</div>
		<div id="footer">
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

