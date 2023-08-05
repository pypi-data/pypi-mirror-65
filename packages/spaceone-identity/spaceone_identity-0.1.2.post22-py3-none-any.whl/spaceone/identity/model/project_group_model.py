# -*- coding: utf-8 -*-

from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel
from spaceone.identity.model.user_model import User


class ProjectGroup(MongoModel):
    project_group_id = StringField(max_length=40, generate_id='pg', unique=True)
    name = StringField(max_length=255)
    parent_project_group = ReferenceField('self', null=True, default=None)
    # template = ReferenceField('Template', null=True)                  # TODO: Template service is NOT be implemented yet
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_by = StringField(max_length=255, null=True)
    created_at = DateTimeField(auto_now_add=True)

    meta = {
        'updatable_fields': [
            'name',
            # TODO: Template service is NOT be implemented yet
            # 'template',
            'parent_project_group',
            'tags'
        ],
        'exact_fields': [
            'project_group_id',
            'domain_id'
        ],
        'minimal_fields': [
            'project_group_id',
            'name'
        ],
        'change_query_keys': {
            'parent_project_group_id': 'parent_project_group.project_group_id'
        },
        'reference_query_keys': {},
        'ordering': ['name'],
        'indexes': [
            'project_group_id',
            'parent_project_group',
            'domain_id'
        ]
    }

    def append(self, key, data):
        if key == 'members':
            data.update({
                'project_group': self
            })

            ProjectGroupMemberMap.create(data)
        else:
            super().append(key, data)

        return self

    def remove(self, key, data):
        if key == 'members':
            query = {
                'filter': [{
                    'k': 'project_group',
                    'v': self,
                    'o': 'eq'
                }, {
                    'k': 'user',
                    'v': data,
                    'o': 'eq'
                }]
            }

            member_map_vos, map_count = ProjectGroupMemberMap.query(**query)
            member_map_vos.delete()
        else:
            super().remove(key, data)

        return self


class ProjectGroupMemberMap(MongoModel):
    project_group = ReferenceField('ProjectGroup', reverse_delete_rule=CASCADE)
    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    roles = ListField(ReferenceField('Role'))
    labels = ListField(StringField(max_length=255))

    meta = {
        'reference_query_keys': {
            'project_group': ProjectGroup,
            'user': User
        },
        'change_query_keys': {
            'project_group_id': 'project_group.project_group_id',
            'project_group_name': 'project_group.name',
            'user_id': 'user.user_id',
            'user_name': 'user.name',
            'email': 'user.email',
            'mobile': 'user.mobile',
            'language': 'user.language',
            'timezone': 'user.timezone'
        },
        'indexes': [
            'project_group',
            'user'
        ]
    }


ProjectGroup._meta['reference_query_keys']['parent_project_group'] = ProjectGroup
