import pytest
import json

from wheelcms_axle.configuration import ConfigurationHandler
from wheelcms_users.models import ConfigurationHandler as UserConfigurationHandler

from django.contrib.auth.models import User

import mock

from twotest.fixtures import client, django_client

@pytest.fixture
def handler():
    patch_processors = mock.patch(
                       'django.template.context.get_standard_processors',
                       return_value=())
    patch_processors.start()
    patch_site = mock.patch('two.ol.base.BaseHandler.site',
                                 new_callable=mock.PropertyMock)
    patch_site.return_value = mock.Mock()
    patch_site.start()
    try:
        return ConfigurationHandler(request=mock.Mock())
    finally:
        patch_site.stop()
        patch_processors.stop()

class TestUserConfig(object):
    def test_nousers(self, handler):
        """ No users """
        userconf = UserConfigurationHandler()
        instance = mock.Mock()

        with mock.patch("django.contrib.auth.models.User.objects.all",
                        return_value=[]):
            data = json.loads(userconf.user_data(handler, instance).content)

            assert data['existing'] == []

    def test_user(self, handler):
        """ Single user with some role """
        userconf = UserConfigurationHandler()
        instance = mock.Mock()
        with mock.patch("django.contrib.auth.models.User.objects.all",
                        return_value=[
                          mock.Mock(id=1,
                                    username="u", first_name="f",
                                    last_name="l", email="e",
                                    is_active=True, is_superuser=False,
                                    roles=mock.Mock(**{"all.return_value":[
                                                    mock.Mock(**{"role.id":123})
                                                      ]
                                                      }
                                                    ))
                         ]):
            data = json.loads(userconf.user_data(handler, instance).content)

            assert len(data['existing']) == 1
            user = data['existing'][0]

            assert user['id'] == 1
            assert user['username'] == 'u'
            assert user['firstname'] == 'f'
            assert user['lastname'] == 'l'
            assert user['email'] == 'e'
            assert user['active']
            assert not user['superuser']
            assert user['roles'] == {'123':True}

    def test_save_user(self, handler, client):
        """ Adding a new user """
        userconf = UserConfigurationHandler()
        instance = mock.Mock()
        handler.request = mock.Mock(**{"method":"POST",
                                       "POST.get.return_value":
                                         json.dumps({ 'existing':[
                                           dict(state="added",
                                                id='added_1',
                                                username="new",
                                                firstname="first",
                                                lastname="last",
                                                email="email@email.com")

                                       ]})
                                      }
                                    )


        data = json.loads(userconf.user_data(handler, instance).content)

        user = User.objects.filter(username="new")
        assert user.count() == 1
        assert user[0].first_name == "first"
        assert user[0].last_name == "last"
        assert user[0].email == "email@email.com"

