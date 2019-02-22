def handle_keys(user_input):
	# Movement Keys.
	if user_input.key == 'UP':
		return {'move': (0, -1)};
	if user_input.key == 'DOWN':
	 	return {'move': (0, 1)};
	if user_input.key == 'LEFT':
	 	return {'move': (-1, 0)};
	if user_input.key == 'RIGHT':
	 	return {'move': (1, 0)};

	if user_input.key == 'ENTER' and user_input.alt: #IF user press ENTER + ALT
		return {'fullscreen': True}; # toggle full screen
	elif user_input.key == 'ESCAPE':
		return {'exit': True};

	# No Key Was Pressed
	return {};
