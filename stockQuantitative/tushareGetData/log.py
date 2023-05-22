#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import logging
from logging.config import dictConfig
import os

logging_config = dict(
    version = 1,
    formatters = {
        'file': {
            'format': '%(asctime)s,%(levelname)s,%(filename)s,%(funcName)s,%(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S'},
        'console':{
            'format': '%(asctime)s\t%(levelname)s\t%(filename)s\t%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'}},
    handlers = {
        'file': {
            'class': "logging.FileHandler",
            'formatter': 'file',
            'level': logging.INFO,
            'filename':'log/'+time.strftime("%Y%m%d")+'.log'},
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.INFO,
            "formatter": "console",
            "stream": "ext://sys.stdout"}},
    loggers = {
        "fileoutput":{
            'handlers': ['file'],
            'level': logging.INFO,},
        "consoleoutput":{
            'handlers': ['console'],
            'level': logging.INFO,}},)

def logInit(loggersname):
    if not(os.path.exists("log")):
        os.mkdir("log")
    dictConfig(logging_config)
    return logging.getLogger(loggersname)

if __name__ == '__main__':
    test = logInit("consoleoutput")
    test.error("error")
    test.info("info")