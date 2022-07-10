#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import multiprocessing

def copyActualToTarget(shelly):
       broker = "mqtt"
       msg = subscribe.simple('shellies/{}/roller/0/pos'.format(shelly), hostname=broker)
       publish.single('shellies/{}/roller/0/command/pos'.format(shelly), msg.payload.decode(), hostname=broker, retain=True)

class web_server(BaseHTTPRequestHandler):

    def do_GET(self):
        shelly = self.path[1:]
        pool = multiprocessing.Pool(1)
        res = pool.apply_async(copyActualToTarget, [shelly])
        try:
            res.get(5)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        except multiprocessing.TimeoutError:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()

httpd = HTTPServer(('0.0.0.0', 7070), web_server)
httpd.serve_forever()
