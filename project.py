# MIT License
#
# Copyright (c) 2015-2021 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from typing import Optional

from Full_setup_tests_todomvc.helpers.pytest.settings import Option


class Config:

    # just an example
    # @Option.default('http://todomvc4tasj.herokuapp.com/')
    # def base_url(self):
    #     pass

    @Option.default(6.0)
    def timeout(self):
        pass

    @Option.default(True)
    def save_page_source_on_failure(self):
        pass

    @Option.default("yashaka")
    def author(self):
        pass

    def __init__(self, request):
        self.request = request

    # --- helpers --- #

    @classmethod
    def options(cls):
        return [Option.from_(field) for field in cls.__dict__.values()
                if Option.in_(field)]

    @classmethod
    def register(cls, parser):
        for option in cls.options():
            option.register(parser)


config: Optional[Config] = None  # to be set by pytest fixtures
