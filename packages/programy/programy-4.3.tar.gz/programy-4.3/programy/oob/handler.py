"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-order
from programy.utils.logging.ylogger import YLogger
from programy.storage.factory import StorageFactory
from programy.oob.default import DefaultOutOfBandProcessor


class OOBHandler:

    def __init__(self):
        self._oobs = {}

    @property
    def default_oob(self):
        return self._oobs.get('default', None)

    @property
    def oobs(self):
        return self._oobs

    def add_oob(self, name, oob_class):
        self._oobs[name] = oob_class

    def empty(self):
        self._oobs.clear()

    def load_oob_processors(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.OOBS) is True:
            storage_engine = storage_factory.entity_storage_engine(StorageFactory.OOBS)
            oobs_store = storage_engine.oobs_store()
            oobs_store.load(self)
        else:
            YLogger.error(None, "No storage engine available for pattern_nodes!")

        if self._oobs.get('default', None) is None:
            self._oobs['default'] = DefaultOutOfBandProcessor()

    def oob_in_response(self, response):
        if response is not None:
            return "<oob>" in response

    def handle(self, client_context, response):
        if "<oob>" in response:
            response, oob = self.strip_oob(response)
            oob_response = self.process_oob(client_context, oob)
            response = response + " " + oob_response

        return response.strip()

    def strip_oob(self, response):
        match = re.compile(r"(.*)(<\s*oob\s*>.*<\/\s*oob\s*>)(.*)")
        groupings = match.match(response)
        if groupings is not None:
            front = groupings.group(1).strip()
            back = groupings.group(3).strip()
            response = ""
            if front != "":
                response = front + " "

            response += back
            oob = groupings.group(2)
            return response, oob

        return response, None

    def process_oob(self, client_context, oob_command):
        oob_content = ET.fromstring(oob_command)

        if oob_content.tag == 'oob':
            for child in oob_content.findall('./'):
                if child.tag in self._oobs:
                    oob_class = self._oobs[child.tag]
                    return oob_class.process_out_of_bounds(client_context, child)

                def_oob = self.default_oob
                if def_oob is not None:
                    def_oob.process_out_of_bounds(client_context, child)
                else:
                    YLogger.error (client_context, "No default oob defined")

        return ""
