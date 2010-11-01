{% extends "layout.tpl" %}
{% block body %}
	{% for post in posts %}
	<div class="post">
	<h2>{{ post.title }}</a> [<a href="/post/edit/{{ post.key() }}" id="edit">Editar</a> | <a href="/publish/{{ post.key() }}" id="edit">Publicar</a> | <a href="/remove/{{ post.key() }}" id="edit">Remover</a>]</h3>
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
	{% else %}
	<div class="section">
		<h2>Nenhum post {% if user %}[<a href="/post/new" id="new">Criar</a>]{% endif %}</h2>
	</div>
	{% endfor %}
{% endblock %}

