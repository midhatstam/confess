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
		$('.new-card').fadeIn(500).fadeOut(100).fadeIn(500).fadeOut(100).fadeIn(500);
	}
	else {
		let parent_element = $('.tab-pane');

		// let new_card = '' +
		// 	'<div class="card shadow border-primary">' +
		// 	'<div class="card-body">' +
		// 	'<h6 class="text-primary text-uppercase float-left">' +
		// 	'# <span class="id-field"></span></h6>' +
		// 	'<h6 class="text-primary float-right"></h6>' +
		// 	'<p class="description mt-5"></p>' +
		// 	'<div class="confess-actions">' +
		// 	'<div class="row">' +
		// 	'<div class="col-md-9"></div>' +
		// 	'<div class="col-md-3">' +
		// 	'<button class="btn btn-light mt-4 confess-buttons btn-block">' +
		// 	'<span class="btn-inner--icon">' +
		// 	'<i class="fa fa-thumbs-up" aria-hidden="true"></i>' +
		// 	'</span>' +
		// 	'<span class="btn-inner--text"> SEND!</span>' +
		// 	'</button>' +
		// 	'</div>' +
		// 	'</div>' +
		// 	'</div>' +
		// 	'</div>' +
		// 	'</div>';
		//
		// parent_element.prepend(new_card);

		$.ajax({
			url: '/api/confesses/',
			type: 'POST',
			success: function (result) {
				let new_card = '' +
					'<div class="card shadow border-primary new-card">' +
					'<div class="card-body">' +
					'<h6 class="text-primary text-uppercase float-left">' +
					'# ' + result.id + '<span class="id-field"></span></h6>' +
					'<h6 class="text-primary float-right">' + result.item_meta_data_date + '</h6>' +
					'<h4 class="mt-5" id="new_confession" contenteditable>Tıklayınız!</h4>' +
					'<div class="confess-actions">' +
					'<div class="row">' +
					'<div class="col-md-9"></div>' +
					'<div class="col-md-3">' +
					'<button class="btn btn-light mt-4 confess-buttons btn-block">' +
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


				$('#new_confession').css("font", "1.2em Helvetica, Arial, sans-serif !important;").click(function () {
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
			}
		});
	}


});