#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import http.client
import getopt
import sys


class HttpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = http.client.HTTPConnection(self.host, self.port)

    def sendRequest(self, method, url, body=None):
        self.conn.request(method, url, body)
        return self.conn.getresponse()


class TinyUrlClient(HttpClient):
    def __init__(self, host = 'localhost', port=8088):
        HttpClient.__init__(self, host, port)

    def getPing(self):
        return HttpClient.sendRequest(self, "GET", "/ping")

    def postUrl(self, url):
        return HttpClient.sendRequest(self, "POST", "/url/{0}".format(url))


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["ping", "postUrl="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    cliObj = TinyUrlClient()

    isPing = False
    isPostUrl = False
    url = ""
    for k, v in opts:
        if k == "--ping":
            isPing = True
            break
        if k == "--postUrl":
            isPostUrl = True
            url = v
            break

    if isPing:
        resp = cliObj.getPing()
        print(resp.status)
        print(resp.read())
    elif isPostUrl:
        resp = cliObj.postUrl(url)
        print(resp.status)
        print(resp.read())
