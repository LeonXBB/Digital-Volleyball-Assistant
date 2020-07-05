self.request_method = 'post'
request = getattr(requests, self.request_method)
self.request_body = {"login": self.data[2][0], "password": self.data[2][1]}
self.reply_body = request(server_ip, params=self.request_body)
