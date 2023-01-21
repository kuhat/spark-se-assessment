import json
import unittest

from project.server import db
from project.server.models import User
from project.tests.base import BaseTestCase

#
# {
#     "email": "1111222@qq.com",
#     "password": "123455"
# }
#
# {
#     "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzQzMjI0NTIsImlhdCI6MTY3NDMyMjQ0Nywic3ViIjo1fQ.A20xnudRhD3fd8G5-KEo0UUtAK6ZVA0hzzJ2yDAd2us",
#     "message": "Successfully registered.",
#     "status": "success"
# }

class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
