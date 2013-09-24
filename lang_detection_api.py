# -*- coding: utf-8 -*-

"""
Language detection API
@author: Paradigmalabs
"""
import os, sys, json
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.insert(0, parent_dir)
import time

from tornado.web import Application
from tornado.ioloop import IOLoop
import tornado.httpserver
import tornado.ioloop
import numpy
import logging
from logging import config
import argparse
import yaml
from lib import ldig


class Application(tornado.web.Application):

    def __init__(self, modeldir):
        # configure logging
        logging_conf_path = os.path.join('./conf', 'log.yml')
        config.dictConfig(yaml.load(open(logging_conf_path,'r')))
        self.log = logging.getLogger('language_detection')

        handlers = [(r"/detect_language", LanguageDetectionHandler),
                    (r"/language_probabilities", LanguageDetectionProbabilitiesHandler)]

        tornado.web.Application.__init__(self, handlers)
        self.detector = Detector(modeldir)    

class Detector(object):
    def __init__(self, modeldir):
        self.log = logging.getLogger("language_detection")
        self.log.info("Initializing language detector...")
        self.ldig = ldig.ldig(modeldir)
        self.features = self.ldig.load_features()
        self.trie = self.ldig.load_da()
        self.labels = self.ldig.load_labels()
        self.param = numpy.load(self.ldig.param)
        self.log.info("Language detector ready.")

    def detect_with_threshold(self, st, threshold):
        lang_probs = self.detect(st)
        max_lang = max(lang_probs, key=lang_probs.get)
        max_prob = float(lang_probs[max_lang])
        return max_lang if max_prob > threshold else None

    def detect_most_probable(self, st):
        lang_probs = self.detect(st)
        return max(lang_probs, key=lang_probs.get)

    def detect(self, st):
        label, text, org_text = ldig.normalize_text(st)
        events = self.trie.extract_features(u"\u0001" + text + u"\u0001")
        sum = numpy.zeros(len(self.labels))

        data = []
        for id in sorted(events, key=lambda id:self.features[id][0]):
            phi = self.param[id,]
            sum += phi * events[id]
            data.append({"id":id, "feature":self.features[id][0], "phi":["%0.3f" % x for x in phi]})
        exp_w = numpy.exp(sum - sum.max())
        prob = exp_w / exp_w.sum()
        return dict(zip(self.labels, ["%0.3f" % x for x in prob]))


class GenericHandler(tornado.web.RequestHandler):
    """
    Class to define common methods and response/error formatting
    """
    
    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type")
        try:
            self.set_status(200)
        except Exception as e:
            self.application.error_log.exception(e)
            self.write_error(500, success=False, message="%s" % e)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        if 'exc_info' in kwargs: # Tornado threw a HTTP error internally
            self.application.log.info(kwargs['exc_info'][1]) # Access to the message
            error_response = {
                'success': False,
                'message': kwargs['exc_info'][1],
            }
            self.write(error_response)
        else:
            self.write(kwargs)
        self.flush()
        self.finish()

    def send_response(self,response):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)
        self.flush()
        self.finish()


class LanguageDetectionHandler(GenericHandler):
    """
        REST service that receives a string and returns the detected language. 
    """
    def get(self):
        start = time.time()
        text = self.get_argument("text")
        try:
            response = {}
            response["language"] = self.application.detector.detect_most_probable(text)
            response["elapsed_time"] = time.time() - start
            self.send_response(response)
        except Exception as e:
            self.application.log.exception(e)
            self.write_error(500, success=False, message="%s" % e)


class LanguageDetectionProbabilitiesHandler(GenericHandler):
    """
        REST service that receives a string and returns the language probability
        distribution.
    """
    def get(self):
        start = time.time()
        text = self.get_argument("text")
        try:
            response = {}
            response["probabilities"] = self.application.detector.detect(text)
            response["elapsed_time"] = time.time() - start
            self.send_response(response)
        except Exception as e:
            self.application.log.exception(e)
            self.write_error(500, success=False, message="%s" % e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="port", default=8000,
                        help="Port where the REST server must listen",
                        type=int)
    args = parser.parse_args()

    http_server = tornado.httpserver.HTTPServer(Application('models/model.latin'))
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()