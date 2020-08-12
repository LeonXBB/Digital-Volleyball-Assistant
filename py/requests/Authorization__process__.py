if self.reply_body == 'Denied':
    i = gfx.frontend.PopUpWindow()
    i.show_pop_up(internet_requests[language_code][1])
else:
    ''' modules[1].user_id = self.reply_body.text[0]
    modules[1].user_status = self.reply_body.text[1] '''  # TODO change this to be an actual request
    user_id = 0  # while internet is disabled
    user_status = [1]
    setattr(DVA, 'user_id', user_id)
    setattr(DVA, 'user_status', user_status)
