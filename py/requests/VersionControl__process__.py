self.reply_body = '0.1.0' # TODO change when internet is enabled

if app_version != self.reply_body:
    
    from gfx.frontend import PopUpWindow

    i = PopUpWindow()
    i.show_pop_up(internet_requests[language_code][3] + app_version + internet_requests[language_code][4] + self.reply_body + (internet_requests[language_code][5]))