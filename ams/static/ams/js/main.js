var ApprovalPage = {
	init: function() {
		this.$container = $('.approval-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-approval', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.approval', self).toggleClass('approved');
				}
			});

			return false;
		});
	}
};

$(document).ready(function() {
	ApprovalPage.init();
});
