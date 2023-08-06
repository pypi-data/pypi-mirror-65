from .async_team import Team
from .async_executor import ThreadEventLoopPolicy
import asyncio
import nest_asyncio

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


class AsyncClient:
    """
    This is the asynchronous version on the main client class. It has the same paramters and the team method, but async.
    This means that it must be called with `await`.

    :param api_key: Your TOA API key. This is required, otherwise you will not be able to access the database.
    :type api_key: str
    :param application_name: The name of the application that you are using to access the API. \
    This can just be the name of your script.
    :type application_name: str

    """

    def __init__(self, api_key: str, application_name: str):
        self._headers = {
            "content-type": "application/json",
            "x-toa-key": api_key,
            "x-application-origin": application_name,
        }
        asyncio.set_event_loop_policy(ThreadEventLoopPolicy())
        loop = asyncio.get_event_loop_policy().get_event_loop()
        nest_asyncio.apply(loop)

    async def team(self, team_number: int):
        """
        Create an asynchronous :class:`~.async_team.Team` object.

        :param team_number: A valid First Tech Challenge team number.
        :type team_number: int
        :return: The Team object
        :rtype: :class:`~.async.Team`
        """
        return Team(team_number=team_number, headers=self._headers)
