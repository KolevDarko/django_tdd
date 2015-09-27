var initializeFunction = function(my_navigator, user, token, urls) {
	$('#id_login').click(function () {
		my_navigator.id.request();
	});
	my_navigator.id.watch({
		loggedInUser: user,
		onlogin: function(assertion){
			$.post(
				urls.login,
				{
					assertion: assertion,
				 	csrfmiddlewaretoken: token
				}
			)
			.done(function() { window.location.reload(); })
			.fail(function() { my_navigator.id.logout(); });
		},
		onlogout: function () {},
	});
};

window.Superlists = {
	Accounts: {
		initialize: initializeFunction
		}
	};

