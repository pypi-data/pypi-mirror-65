"""
 * methods
 * Copyright(c) 2013-2014 TJ Holowaychuk
 * Copyright(c) 2015-2016 Douglas Christopher Wilson
 * Copyright(c) 2020-2020 Braian Staimer
 * MIT Licensed
"""

methods = [
    'get',
    'post',
    'put',
    'head',
    'delete',
    'options',
    'trace',
    'copy',
    'lock',
    'mkcol',
    'move',
    'purge',
    'propfind',
    'proppatch',
    'unlock',
    'report',
    'mkactivity',
    'checkout',
    'merge',
    'm-search',
    'notify',
    'subscribe',
    'unsubscribe',
    'patch',
    'search',
    'connect'
]


def getHttpMethods(uppercase=False):
    if(uppercase == False):
        return methods
    return list(map(lambda x: x.upper(), methods))
