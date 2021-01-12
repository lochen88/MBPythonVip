# -*- coding:utf-8 -*-

class Tool():
    def __init__(self,miniblink):
        self.mb=miniblink
    def mbUtilDecodeURLEscape(self,url):
        url=url.encode()
        url=self.mb.mbUtilDecodeURLEscape(url)
        return url.decode()
    def mbUtilEncodeURLEscape(self,url):
        url=url.encode()
        url=self.mb.mbUtilEncodeURLEscape(url)
        return url.decode()
    def mbUtilBase64Decode(self,text,isbytes=False):
        text=text.encode()
        text=self.mb.mbUtilBase64Decode(text)
        if not isbytes:
            return text.decode()
        return text
    def mbUtilBase64Encode(self,text,isbytes=False):
        if not isbytes:
            text=text.encode()
        text=self.mb.mbUtilBase64Encode(text)
        return text.decode()