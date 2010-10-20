$(document).ready(function() {

	$('input[type=submit]').click(function() {
		var title = $("input[name=title]").val();
		var content =  $("textarea").val();

		$("p.warning").html("");
		if (title.length == 0 || content.length == 0) {
			$('p.warning').html("Preencha o formulário corretamente!");
			return false;
		}

	});
});

