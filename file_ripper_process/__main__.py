import json
import sys
import unittest
from time import sleep

import requests

from .process import execute_process


class OhGnarlyIntegrationTests(unittest.TestCase):
    """Test that ohgnarly api is running and we can call it"""
    def test_call_oh_gnarly_api(self):
        """Basic smoke test that ohgnarly api is running by calling /users endpoint to get users"""
        headers = {'sender': 'ohGnarlyChat', 'api-key': 'M1lxUG7MdBbvsaPEjono+w=='}
        users = json.loads(requests.get('https://ohgnarly3.herokuapp.com/users', headers=headers).text)
        aaron = users[0]
        self.assertEqual('asmitty92', aaron['userName'])
        darin = users[1]
        self.assertEqual('djmurtle', darin['userName'])


if __name__ == "__main__":
    try:
        while True:
            execute_process(sys.argv[1])
            sleep(5 * 60)
    except KeyboardInterrupt:
        print('Stopping file_ripper....')
    except IndexError:
        print('No definitions file provided at command line. Running unit tests.....')
        unittest.main()
