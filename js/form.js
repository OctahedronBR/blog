$(document).ready(function() {

	$('input[type=submit]').click(function() {
		var title = $("input[name=title]").val();
		var content =  $("textarea[name=content]").val();

		$('p.warning').html("");
		if (title.length == 0 || content.length == 0) {
			$('p.warning').html("Preencha o formulário corretamente!");
			return false;
		}
	});

	$('button#slugify').click(function() {
		var slug = $("input[name=title]").val();
		slug = slug.replace(/\s+/g,'-');
		slug = slug.replace(/[^a-zA-Z0-9\-]/g,'');
		slug = slug.toLowerCase();
		$('input[name=slug]').val(slug);

		return false;
	});

	$("textarea[name=content]").markItUp(mySettings);
});

