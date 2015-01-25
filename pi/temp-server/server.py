# Web server to read and respond with the current temperature reading of the
# thermocouple

import tornado.ioloop
import tornado.web

from max31855 import MAX31855

# Thermocouple GPIO configuration
cs_pin    = 24
clock_pin = 23
data_pin  = 22

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        thermocouple = MAX31855(cs_pin, clock_pin, data_pin, 'f')
        thermocouple.read()
        celsius     = thermocouple.data_to_tc_temperature()
        farenheight = thermocouple.to_f(celsius)
        thermocouple.cleanup()

        response = { 'celsius': celsius, 'farenheight': farenheight }
        self.write(response)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

