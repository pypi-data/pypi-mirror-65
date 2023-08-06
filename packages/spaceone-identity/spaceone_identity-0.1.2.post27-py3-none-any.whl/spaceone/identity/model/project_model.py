# -*- coding: utf-8 -*-

from datetime import datetime
from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel
from spaceone.identity.model.user_model import User
from spaceone.identity.model.project_group_model import ProjectGroup


class Project(MongoModel):
    project_id = StringField(max_length=40, generate_id='project', unique=True)
    name = StringField(max_length=255)
    state = StringField(max_length=20, default='ACTIVE')
    # template = ReferenceField('Template', reverse_delete_rule=CASCADE, null=True) # TODO: Template service is NOT be implemented yet
    project_group = ReferenceField('ProjectGroup', reverse_delete_rule=CASCADE, null=True, default=None)
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_by = StringField(max_length=255, null=True)
    created_at = DateTimeField(auto_now_add=True)
    deleted_at = DateTimeField(default=None, null=True)

    meta = {
        'updatable_fields': [
            'name',
            'state',
            'project_group',
            # TODO: Template service is NOT be implemented yet
            # 'template',
            'tags',
            'deleted_at'
        ],
        'exact_fields': [
            'project_id',
            'state',
            'domain_id'
        ],
        'minimal_fields': [
            'project_id',
            'name',
            'state',
        ],
        'change_query_keys': {
            'project_group_id': 'project_group.project_group_id'
        },
        'reference_query_keys': {
            'project_group': ProjectGroup
        },
        'ordering': ['name'],
        'indexes': [
            'project_id',
            'state',
            'project_group',
            'domain_id'
        ]
    }

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.filter(state__ne='DELETED')

    def append(self, key, data):
        if key == 'members':
            data.update({
                'project': self
            })

            ProjectMemberMap.create(data)
        else:
            super().append(key, data)

        return self

    def remove(self, key, data):
        if key == 'members':
            query = {
                'filter': [{
                    'k': 'project',
                    'v': self,
                    'o': 'eq'
                }, {
                    'k': 'user',
                    'v': data,
                    'o': 'eq'
                }]
            }

            member_map_vos, map_count = ProjectMemberMap.query(**query)
            member_map_vos.delete()
        else:
            super().remove(key, data)

        return self

    def delete(self):
        self.update({
            'state': 'DELETED',
            'deleted_at': datetime.utcnow()
        })


class ProjectMemberMap(MongoModel):
    project = ReferenceField('Project', reverse_delete_rule=CASCADE)
    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    roles = ListField(ReferenceField('Role'))
    labels = ListField(StringField(max_length=255))

    meta = {
        'reference_query_keys': {
            'project': Project,
            'user': User
        },
        'change_query_keys': {
            'project_id': 'project.project_id',
            'project_name': 'project.name',
            'user_id': 'user.user_id',
            'user_name': 'user.name',
            'email': 'user.email',
            'mobile': 'user.mobile',
            'language': 'user.language',
            'timezone': 'user.timezone'
        },
        'indexes': [
            'project',
            'user'
        ]
    }
