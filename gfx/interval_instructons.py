instructions = [
'''
PopUpWindow().show_interval_window([1, 2, 
":".join([str(int(self.design.main_widget.timer.text.split(":")[0]) + time_between_court_entry_and_coin_tossing), self.design.main_widget.timer.text.split(":")[1]])])
''', # court entry interval

'''
pass
''', # coin_toss_interval

'''
match.status = 'Ongoing'
match.start_time = str(time.localtime()[3]) + ':' + str(time.localtime()[4])
match_events_dispatch.run(SetStart, None, self.arguments[0][0])
''', # match interval

'''
pass
''', # time out interval

'''
match_events_dispatch.run(SetStart, None, self.arguments[0][0])
''' # set interval
]
