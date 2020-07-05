self.request_method = 'get'
request = getattr(requests, self.request_method)
self.request_body = str(self.data[2])
self.reply_body = request(server_ip, params=self.request_body)