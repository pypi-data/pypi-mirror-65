import aiohttp
import json

# MIT License
#
# Copyright (c) 2020 Yash Karandikar
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


async def request(target: str, headers: dict):
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"https://theorangealliance.org/api{target}"
        async with session.get(url) as resp:
            if resp.status != 200:
                try:
                    data = json.loads(await resp.text())
                except json.decoder.JSONDecodeError:
                    raise WebException(await resp.text())
                else:
                    raise WebException(data["_message"])
            data = json.loads(await resp.text())

    return data


class WebException(Exception):
    def __init__(self, message: str):
        if message == "The supplied API key was not found.":
            message = "The supplied API key was invalid."
        self.message = message
        super().__init__(message)
