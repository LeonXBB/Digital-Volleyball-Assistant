self.request_method = 'get'
request = getattr(requests, self.request_method)
self.request_body = ''
self.reply_body = request(server_ip, params=self.request_body)
