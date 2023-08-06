#  logger-mixin __init__.py (Last Modified 3/10/20, 8:37 AM)
#  Copyright (C) 2020 Daniel Sullivan (daniel.sullivan@state.mn.us)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import logging.config
from copy import deepcopy

LOGGING_CONFIG = {
    'version':    1,
    'formatters': {
        'detailed': {
            'class':  'logging.Formatter',
            'format': '%(asctime)s %(threadName)s %(name)-5s {%(module)-10s:%(lineno)-3d} %(levelname)-8s %(message)s'
        },
        'shorter':  {

            'class':  'logging.Formatter',
            'format': '%(asctime)s %(levelname)-8s %(message)s'
        }
    },
    'handlers':   {
        'console':   {
            'class':     'logging.StreamHandler',
            'level':     'INFO',
            'formatter': 'shorter'
        },
        'file':      {
            'class':     'logging.FileHandler',
            'level':     'DEBUG',
            'formatter': 'detailed',
            'filename':  'debug.log',
            'mode':      'w'
        },
        'warn_file': {
            'class':     'logging.FileHandler',
            'level':     'WARNING',
            'formatter': 'detailed',
            'filename':  'warning.log',
            'mode':      'w'
        }
    },
    'root':       {
        'level':    'DEBUG',
        'handlers': ['console', 'file', 'warn_file']
    },
}


class LoggerMixin(object):
    _logger = None  # type: logging.Logger

    @property
    def logger(self):
        # type: () -> logging.Logger
        if self._logger:
            return self._logger
        name = '.'.join([
            self.__class__.__module__,
            self.__class__.__name__
        ])
        self._logger = logging.getLogger(name)
        return self._logger

    def log_and_raise(self, e):
        """

        Args:
            e (BaseException):
        """
        self.logger.exception(e)
        raise e

    @classmethod
    def init_logging(cls, console_loglevel=logging.INFO):
        lc = deepcopy(LOGGING_CONFIG)
        lc['handlers']['console']['level'] = logging.getLevelName(console_loglevel)
        logging.config.dictConfig(lc)


__all__ = ['LoggerMixin']
