self.request_method = 'post'
request = getattr(requests, self.request_method)
self.request_body = str(self.data[2][0])
if not self.no_internet:
    self.reply_body = request(server_ip, params=self.request_body)
