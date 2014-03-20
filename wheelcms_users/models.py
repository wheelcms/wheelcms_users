import json

from drole.types import Role
from wheelcms_axle.models import Role as WheelRole

from django.contrib.auth.models import User

from wheelcms_axle.configuration import BaseConfigurationHandler
from wheelcms_axle.registries.configuration import configuration_registry


class ConfigurationHandler(BaseConfigurationHandler):
    id = "users_groups"
    label = "Users & Groups"
    model = None
    form = None

    def view(self, handler, instance):
        users = User.objects.all()
        data = {}
        data['users'] = [dict(id=u.id,
                              username=u.username,
                              firstname=u.first_name,
                              lastname=u.last_name,
                              active=u.is_active,
                              superuser=u.is_superuser,
                              roles=dict((role.role.id, True)
                                         for role in u.roles.all())
                              ) for u in users]
        # import pdb; pdb.set_trace()
        
        data['roles'] = [dict(id=role.id, name=role.name, description=role.description) for role in Role.all()]

        data['groups'] = []
        handler.context['userdata'] = json.dumps(data)

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
