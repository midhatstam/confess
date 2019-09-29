var csrftoken = $('[name=csrfmiddlewaretoken]').val();

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
				url: '/api/confessions/',
				type: 'POST',
				data: {
					'id': id,
					'body': body,
					'csrfmiddlewaretoken': csrftoken
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
	var data = {
		'id': parseInt(id),
		'item': 'confession',
		'csrfmiddlewaretoken': csrftoken
	};
	if ($(this).hasClass('like')) {
		data.vote = 'true'
	}
	else if ($(this).hasClass('dislike')) {
		data.vote = 'false'
	}

	$.ajax({
		url: '/api/confessions/vote/up/',
		type: 'POST',
		data: data,
		success: function (result) {
			like_button.find(".btn-inner--text").html(result.item.item_meta_data_like);
			dislike_button.find(".btn-inner--text").html(result.item.item_meta_data_dislike);
			if (like_button.prop("disabled") === true) {
				like_button.prop("disabled", false);
			}
			else if (dislike_button.prop("disabled") === true) {
				dislike_button.prop("disabled", false);
			}
			this_element.prop("disabled", true);
		}
	})
});

$('.details').on('click', function (e) {
	var button = $(e.target);
	if ($(button).hasClass('elem-exc')) {
		e.stopPropagation();
	}
	else {
		var card = button.closest('.card');
		var id = card.find('.id-field').text();
		var body = card.find('.description').text();
		var modal = $('#modal-notification').modal('show');
		$('#modal-title-notification').html('#' + id);
		$('.modal-body').html(body);
		var id_class = card.find('.id-field').parent().attr('class').split(/\s+/)[0].replace('text-', '');
		$('.modal-content').addClass('bg-gradient-' + id_class);

		var comments_panel = $('.comments-panel');
		$.ajax({
			url: '/api/confessions/' + id + '/comments/',
			type: 'GET',
			success: function (result) {
				$.each(result, function (index, data_obj) {
					var author = '';
					var data_author = data_obj.username;
					if (data_author === '' || data_author == null) {
						author = 'Anonymous';
					}
					else {
						author = data_author;
					}
					var comment_card =
						'<div class="card bg-gradient-' + id_class + ' shadow-lg border-0 comment-card p-lg-3">\n' +
						'<div class="comment-id hidden-elm">' +
						data_obj.id
						+ '</div>' +
						'\t\t\t\t\t<div class="float-left font-italic comment-author">\n' +
						author +
						'\t\t\t\t\t</div>\n' +
						'\t\t\t\t\t<div class="card-body card-body-sm">\n' +
						data_obj.body +
						'\t\t\t\t\t</div>\n' +
						'\t\t\t\t\t<div class="float-right w-50">\n' +
						'\t\t\t\t\t\t<div class="confess-actions">\n' +
						'\t\t\t\t\t\t\t<div class="confess-actions-panel">\n' +
						'\t\t\t\t\t\t\t\t<button class="btn-sm btn-' + id_class + ' comment-buttons like">\n' +
						'\t\t\t\t\t\t\t\t\t\t\t\t\t<span class="btn-inner--icon">\n' +
						'\t\t\t\t\t\t\t\t\t\t\t\t\t\t<i class="fa fa-thumbs-up" aria-hidden="true"></i>\n' +
						'\t\t\t\t\t\t\t\t\t\t\t\t\t</span>\n' +
						'\t\t\t\t\t\t\t\t\t<span class="btn-inner--text">' +
						data_obj.item_meta_data_like +
						'</span>\n' +
						'\t\t\t\t\t\t\t\t</button>\n' +
						'\n' +
						'\t\t\t\t\t\t\t\t<button style="cursor:pointer; display: block; flex-grow:1;"\n' +
						'\t\t\t\t\t\t\t\t\t\tclass="btn-sm btn-' + id_class + ' ml-3 comment-buttons dislike">\n' +
						'\t\t\t\t\t\t\t\t\t\t\t\t\t<span class="btn-inner--icon">\n' +
						'\t\t\t\t\t\t\t\t\t\t\t\t\t\t<i class="fa fa-thumbs-down" aria-hidden="true"></i>\n' +
						'\t\t\t\t\t\t\t\t\t\t\t\t\t</span>\n' +
						'\t\t\t\t\t\t\t\t\t<span class="btn-inner--text">' +
						data_obj.item_meta_data_dislike +
						'</span>\n' +
						'\t\t\t\t\t\t\t\t</button>\n' +
						'\t\t\t\t\t\t\t</div>\n' +
						'\t\t\t\t\t\t</div>\n' +
						'\t\t\t\t\t</div>\n' +
						'\t\t\t\t</div>';

					comments_panel.append(comment_card);
				});

				$('.comment-buttons').click(function () {
					var this_element = $(this);
					var comment_id = this_element.parents('.comment-card').children('.comment-id').text();
					var like_button = this_element.parent().children('.like');
					var dislike_button = this_element.parent().children('.dislike');
					var data = {
						'id': parseInt(comment_id),
						'item': 'comment',
						'csrfmiddlewaretoken': csrftoken
					};
					if ($(this).hasClass('like')) {
						data.vote = 'true'
					}
					else if ($(this).hasClass('dislike')) {
						data.vote = 'false'
					}

					$.ajax({
						url: '/api/comments/vote/up/',
						type: 'POST',
						data: data,
						success: function (result) {
							like_button.find(".btn-inner--text").html(result.item.item_meta_data_like);
							dislike_button.find(".btn-inner--text").html(result.item.item_meta_data_dislike);
							if (like_button.prop("disabled") === true) {
								like_button.prop("disabled", false);
							}
							else if (dislike_button.prop("disabled") === true) {
								dislike_button.prop("disabled", false);
							}
							this_element.prop("disabled", true);
						}
					})
				});

				$('.comment-button').click(function () {
					$('.new-comment-panel').removeClass('hidden-elm');
				});
			}
		});
	}
});

var loaded = false;

$('.send-comment-button').click(function (e) {
	var id = $('#modal-title-notification').text().replace('#', '');
	var username_elem = $('.username');
	var comment_body_elem = $('.comment-body');
	var send_icon = $('.comment-icon');
	var success_comment = $('.success-comment');
	send_icon.fadeOut();
	var data = {
		'csrfmiddlewaretoken': csrftoken,
		'body': comment_body_elem.val()
	};
	if (username_elem.val() !== '') {
		data.username = username_elem.val();
	}
	if (loaded) return;
	$.ajax({
		url: '/api/confessions/' + id + '/comments/',
		data: data,
		type: 'POST',
		success: function (result) {
			setTimeout(
				function () {
					success_comment.fadeIn();
				}, 1000
			);
			loaded = true;
			username_elem.prop("disabled", true);
			comment_body_elem.prop("disabled", true);
			comment_body_elem.removeClass('bg-neutral');
		},
		error: function (requestObject, error) {
			if (error) {
				comment_body_elem.addClass('is-invalid');
			}
		}
	});
});

$('#modal-notification').on('hidden.bs.modal', function () {
	$('.comments-panel').html('');
	$('.modal-content').removeClass().addClass('modal-content');
});