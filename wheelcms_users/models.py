from two.ol.base import json
from json import loads as load_json

from drole.types import Role
from wheelcms_axle.models import Role as WheelRole

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from wheelcms_axle.actions import action
from wheelcms_axle.configuration import BaseConfigurationHandler
from wheelcms_axle.registries.configuration import configuration_registry


class ConfigurationHandler(BaseConfigurationHandler):
    id = "users_groups"
    label = "Users & Groups"
    model = None
    form = None

    @action
    @json
    def validate_username(self, handler, instance):
        username = handler.request.REQUEST.get('username', '')
        if username:
            if User.objects.filter(username=username).exists():
                return dict(isValid=False)
            try:
                UserCreationForm.base_fields['username'].validate(username)
                UserCreationForm.base_fields['username'].run_validators(username)
                return dict(isValid=True)
            except ValidationError:
                pass

        return dict(isValid=False)

    @action
    @json
    def user_data(self, handler, instance):
        if handler.request.method == "POST":
            data = load_json(handler.request.POST.get('data', "{}"))

            for user in data.get('existing', []):
                state = user.get('state', '')

                if state == 'deleted':
                    try:
                        User.objects.get(pk=user['id']).delete()
                    except (ValueError, User.DoesNotExist):
                        pass
                elif state in ("added", "modified"):
                    try:
                        u = User.objects.get(pk=user['id'])
                        u.username = user.get('username').strip()
                        u.first_name = user.get('firstname', '')
                        u.last_name = user.get('lastname', '')
                        u.email = user.get('email', '')
                        ## active?
                    except (ValueError, User.DoesNotExist):
                        u = User(username=user.get('username').strip(),
                                 first_name=user.get('firstname', ''),
                                 last_name=user.get('lastname', ''),
                                 email=user.get('email', ''))
                        u.save()

                    password = user.get('password', '').strip()
                    if password:
                        u.set_password(password)

                    u.roles.all().delete()

                    for role, isset in user.get('roles', {}).iteritems():
                        if isset:
                            WheelRole(role=Role(role), user=u).save()

                    u.save()

                ## roles


        users = User.objects.all()
        data = {}
        data['existing'] = [dict(id=u.id,
                              username=u.username,
                              firstname=u.first_name,
                              lastname=u.last_name,
                              email=u.email,
                              active=u.is_active,
                              superuser=u.is_superuser,
                              roles=dict((role.role.id, True)
                                         for role in u.roles.all())
                              ) for u in users]
        data['roles'] = [dict(id=role.id,
                              name=role.name,
                              description=role.description)
                         for role in Role.all()]

        return data

    def view(self, handler, instance):
        return handler.template("wheelcms_users/configure_users.html")

    def process(self, handler, instance):
        user_roles = handler.request.POST.getlist('users')
        for user_role in user_roles:
            data = json.loads(user_role)
            userid = data['id']
            roles = data['roles']

            try:
                u = User.objects.get(id=userid)
                u.roles.all().delete()
                for role in roles:
                    WheelRole(user=u, role=role).save()
            except User.DoesNotExist:
                continue

        return self.view(handler, instance)

configuration_registry.register(ConfigurationHandler)
