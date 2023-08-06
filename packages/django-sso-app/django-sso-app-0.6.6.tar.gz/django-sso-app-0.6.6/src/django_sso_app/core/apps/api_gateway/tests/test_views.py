import json

import jwt
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status

from .....backend.tests.factories import UserTestCase

User = get_user_model()


class TestApiGateway(UserTestCase):

    def check_gateway_is_enabled(self):
        pass
