#  logger-mixin test_logger_mixin.py (Last Modified 3/10/20, 8:45 AM)
#  Copyright (C) 2020 Daniel Sullivan (daniel.sullivan@state.mn.us
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

from logger_mixin import LoggerMixin

import pytest


@pytest.mark.incremental
class TestLoggerMixin(object):

    @staticmethod
    def return_class():
        class TestClass(LoggerMixin):
            pass

        tc = TestClass()
        return tc

    def test_init(self):
        LoggerMixin.init_logging()

    def test_logger(self):
        tc = self.return_class()
        tc.logger.warning('Warning')
        tc.logger.info('Info')

    def test_log_and_raise(self):
        tc = self.return_class()
        e = Exception('Exception!')
        with pytest.raises(Exception):
            tc.log_and_raise(e)
