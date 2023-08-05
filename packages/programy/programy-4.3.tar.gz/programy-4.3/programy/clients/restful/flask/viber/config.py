"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial avatarions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.clients.restful.config import RestConfiguration
from programy.utils.substitutions.substitues import Substitutions


class ViberConfiguration(RestConfiguration):

    def __init__(self):
        RestConfiguration.__init__(self, "viber")
        self._name = None
        self._avatar = None
        self._webhook = None

    @property
    def name(self):
        return self._name

    @property
    def avatar(self):
        return self._avatar

    @property
    def webhook(self):
        return self._webhook

    def load_configuration_section(self, configuration_file, section, bot_root, subs: Substitutions = None):
        assert section is not None

        self._name = configuration_file.get_option(section, "name", missing_value="Program-y", subs=subs)
        self._avatar = configuration_file.get_option(section, "avatar", missing_value="http://viber.com/avatar.jpg",
                                                 subs=subs)
        self._webhook = configuration_file.get_option(section, "webhook",
                                                  missing_value="https://localhost:5000/api/viber/v1.0/ask", subs=subs)
        super(ViberConfiguration, self).load_configuration_section(configuration_file, section, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['name'] = "Program-Y"
            data['avatar'] = 'http://127.0.0.1/programy.png'
            data['webhook'] = 'https://127.0.0.1/api/viber/v1.0/ask'
        else:
            data['name'] = self._name
            data['avatar'] = self._avatar
            data['webhook'] = self._webhook

        super(ViberConfiguration, self).to_yaml(data, defaults)
