$('#tabs-text-1-tab').click(function () {
	window.location = "/";
});

$('#tabs-text-2-tab').click(function () {
	window.location = "/popular/";
});

$('#tabs-text-3-tab').click(function () {
	window.location = "/best/";
});

$('#tabs-text-4-tab').click(function () {
	window.location = "/by_comments/";
});

$('#tabs-text-5-tab').click(function () {
	window.location = "/by_likes/";
});

$('#tabs-text-6-tab').click(function () {
	window.location = "/by_dislikes/";
});

$('.write-button').click(function () {
	if ($('.new-card').length > 0) {
		$('.new-card').fadeIn(500).fadeOut(100).fadeIn(500).fadeOut(100).fadeIn(500).delay(100);
	}
	else {
		let parent_element = $('.tab-pane');

		let new_card = '' +
			'<div class="card shadow border-primary new-card">' +
			'<div class="card-body">' +
			'<h6 class="text-primary text-uppercase float-left">' +
			'#<span class="id-field"></span></h6>' +
			'<h6 class="text-primary float-right date-field"></h6>' +
			'<h4 class="mt-5" id="new-confession" contenteditable>Tıklayınız!</h4>' +
			'<div class="confess-actions">' +
			'<div class="row">' +
			'<div class="col-md-9"></div>' +
			'<div class="col-md-3">' +
			'<button class="btn btn-light mt-4 confess-buttons btn-block" id="send-button">' +
			'<span class="btn-inner--icon">' +
			'<i class="fa fa-thumbs-up" aria-hidden="true"></i>' +
			'</span>' +
			'<span class="btn-inner--text"> SEND!</span>' +
			'</button>' +
			'</div>' +
			'</div>' +
			'</div>' +
			'</div>' +
			'</div>';

		var html_card = $($.parseHTML(new_card));
		html_card.hide().prependTo(parent_element).slideDown(200);


		$('#new-confession').css("font", "1.2em Helvetica, Arial, sans-serif !important;").click(function () {
			if ($(this).text() === "" || $(this).text() === 'Tıklayınız!') {
				$(this).empty();
			}
		}).focusout(function () {
				if ($(this).text() === "") {
					$(this).html('Tıklayınız!');
				}
				else {

				}
			}
		);

		$("#send-button").click(function () {
			var id = $('.id-field').text();
			var body = $('#new-confession').text();
			$.ajax({
				url: '/api/confesses/',
				type: 'POST',
				data: {
					'id': id,
					'confess_body': body,
				},
				success: function (result) {
					console.log('success');
					$('.id-field').html(result.id);
					$('.date-field').html("just now");
					$("#send-button").remove();
					$('#new-confession').removeAttr('contenteditable');
				}
			});
		});
	}
});

$('.confess-buttons').click(function () {
	var this_element = $(this);
	var id = this_element.parents('.card-body').children('.float-left').children('.id-field').text();
	var like_button = this_element.parent().children('.like');
	var dislike_button = this_element.parent().children('.dislike');
	var data = {};
	if (dislike_button.prop("disabled") === true) {
		data = {
			'like': '1',
			'dislike': '0',
			'id': id
		}
	}
	else if (like_button.prop("disabled") === true) {
		data = {
			'like': '0',
			'dislike': '1',
			'id': id
		}
	}
	else {

	}
	if ($(this).hasClass('like')) {
		if (Object.keys(data).length === 0 && data.constructor === Object) {
			data = {
				'like': '1',
				'id': id
			}
		}
		$.ajax({
			url: '/api/confesses/' + id + '/',
			type: 'PUT',
			data: data,
			success: function (result) {
				var like = this_element.find(".btn-inner--text");
				like.html(result.item_meta_data_like);
				var dislike = this_element.parent().children('.dislike').find(".btn-inner--text");
				dislike.html(result.item_meta_data_dislike);
				like.parent().prop("disabled", true);
				if (dislike_button.prop("disabled") === true) {
					dislike_button.prop("disabled", false);
				}
			}
		});
	}
	else if ($(this).hasClass('dislike')) {
		if (Object.keys(data).length === 0 && data.constructor === Object) {
			data = {
				'dislike': '1',
				'id': id
			}
		}
		$.ajax({
			url: '/api/confesses/' + id + '/',
			type: 'PUT',
			data: data,
			success: function (result) {
				var dislike = this_element.find(".btn-inner--text");
				dislike.html(result.item_meta_data_dislike);
				var like = this_element.parent().children('.like').find(".btn-inner--text");
				like.html(result.item_meta_data_like);
				dislike.parent().prop("disabled", true);
				if (like_button.prop("disabled") === true) {
					like_button.prop("disabled", false);
				}
			}
		});
	}
});