# -*- coding: utf-8 -*-

import sys
import re
import hashlib
from .six import reraise
from .log import logger


def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    # force the import name to automatically convert to strings
    # __import__ is not able to handle unicode strings in the fromlist
    # if the module is a package
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            module = import_string(module_name)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        if not silent:
            t, v, tb = sys.exc_info()
            reraise(t, v, tb)


class TextHandlerBase(object):

    @classmethod
    def handle(cls, content):
        raise NotImplementedError()


class TextHandlerPokio(TextHandlerBase):

    @classmethod
    def handle_bak(cls, content):
        """
        :param content:
        :return:
        """
        pattern = re.compile('[[](.*?)[]]', re.S)
        res_list = re.findall(pattern, content)
        if not res_list or len(res_list) < 3:
            return ''
        new_content = content
        tmp_text = new_content.replace(res_list[1], '')
        tmp_text = tmp_text.replace(res_list[2], '')
        logger.info('trace debug tmp_text: %s', tmp_text)
        return hashlib.md5(tmp_text).hexdigest()

    @classmethod
    def handle(cls, content):
        """
        :param content:
        :return:
        """
        pattern = re.compile(r'\[\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3}\]\[\d{1,6}:\d+\]', re.S)
        res_list = re.findall(pattern, content)
        if not res_list:
            return ''
        new_content = content
        tmp_text = new_content.replace(res_list[0], '', 1)

        return hashlib.md5(tmp_text).hexdigest()




