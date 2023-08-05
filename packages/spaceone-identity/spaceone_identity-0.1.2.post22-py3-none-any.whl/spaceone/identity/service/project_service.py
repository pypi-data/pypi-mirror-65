# -*- coding: utf-8 -*-
import logging
from spaceone.core.service import *
from spaceone.identity.error.error_project import *
from spaceone.identity.manager.project_manager import ProjectManager
from spaceone.identity.manager.project_group_manager import ProjectGroupManager
from spaceone.identity.manager.role_manager import RoleManager
from spaceone.identity.manager.user_manager import UserManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class ProjectService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.project_mgr: ProjectManager = self.locator.get_manager('ProjectManager')

    @transaction
    @check_required(['name', 'project_group_id', 'domain_id'])
    def create(self, params):
        params['created_by'] = self.transaction.get_meta('user_id')

        if 'project_group_id' in params:
            project_group_mgr: ProjectGroupManager = self.locator.get_manager('ProjectGroupManager')
            params['project_group'] = project_group_mgr.get_project_group(params['project_group_id'],
                                                                          params['domain_id'])

        if 'template_data' in params:
            # TODO: Template service is NOT be implemented yet
            pass

        return self.project_mgr.create_project(params)

    @transaction
    @check_required(['project_id', 'domain_id'])
    def update(self, params):
        domain_id = params['domain_id']

        project_vo = self.project_mgr.get_project(params['project_id'], domain_id)

        if 'project_group_id' in params:
            project_group_mgr: ProjectGroupManager = self.locator.get_manager('ProjectGroupManager')
            params['project_group'] = project_group_mgr.get_project_group(params['project_group_id'], domain_id)

        if 'template_id' in params:
            # TODO: Template service is NOT be implemented yet
            pass

        return self.project_mgr.update_project_by_vo(params, project_vo)

    @transaction
    @check_required(['project_id', 'domain_id'])
    def delete(self, params):
        project_vo = self.project_mgr.get_project(params['project_id'], params['domain_id'])

        self._check_exist_resource(params)
        self.project_mgr.delete_project_by_vo(project_vo)

    @transaction
    @check_required(['project_id', 'user_id', 'domain_id'])
    def add_member(self, params):
        domain_id = params['domain_id']
        project_id = params['project_id']

        project_vo = self.project_mgr.get_project(project_id, domain_id)

        user_vo = self._get_user(params['user_id'], domain_id)

        if self._is_exist_member(project_id, user_vo, domain_id):
            raise ERROR_ALREADY_EXIST_USER_IN_PROJECT(user_id=user_vo.user_id,
                                                      project_id=project_id)

        roles = self._get_roles(params.get('roles', []), domain_id)
        labels = list(set(params.get('labels', [])))

        self._check_role_type(user_vo.roles, roles)

        project_vo = self.project_mgr.add_member(project_vo, user_vo, roles, labels)

        return {
            'project': project_vo,
            'user': user_vo,
            'roles': roles,
            'labels': labels
        }

    @transaction
    @check_required(['project_id', 'user_id', 'domain_id'])
    def modify_member(self, params):
        domain_id = params['domain_id']
        project_id = params['project_id']

        project_vo = self.project_mgr.get_project(project_id, domain_id)
        user_vo = self._get_user(params['user_id'], domain_id)

        if not self._is_exist_member(project_id, user_vo, domain_id):
            raise ERROR_NOT_FOUND_USER_IN_PROJECT(user_id=user_vo.user_id,
                                                  project_id=project_id)

        roles = self._get_roles(params.get('roles', []), domain_id)
        labels = list(set(params.get('labels', [])))

        self._check_role_type(user_vo.roles, roles)

        project_vo = self.project_mgr.modify_member(project_vo, user_vo, roles, labels)

        return {
            'project': project_vo,
            'user': user_vo,
            'roles': roles,
            'labels': labels
        }

    @transaction
    @check_required(['project_id', 'user_id', 'domain_id'])
    def remove_member(self, params):
        domain_id = params['domain_id']
        project_id = params['project_id']

        project_vo = self.project_mgr.get_project(project_id, domain_id)
        user_vo = self._get_user(params['user_id'], domain_id)

        if not self._is_exist_member(project_id, user_vo, domain_id):
            raise ERROR_NOT_FOUND_USER_IN_PROJECT(user_id=user_vo.user_id,
                                                  project_id=project_id)

        self.project_mgr.remove_member(project_vo, user_vo)

    @transaction
    @check_required(['project_id', 'domain_id'])
    def get(self, params):
        return self.project_mgr.get_project(params['project_id'], params['domain_id'])

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['project_id', 'name', 'project_group_id', 'domain_id'])
    def list(self, params):
        return self.project_mgr.list_projects(params.get('query', {}))

    @transaction
    @check_required(['project_id', 'domain_id'])
    @append_query_filter(['user_id', 'domain_id'])
    def list_members(self, params):
        query = params.get('query', {})

        project_vo = self.project_mgr.get_project(params['project_id'], params['domain_id'])
        user_mgr: UserManager = self.locator.get_manager('UserManager')
        user_vos, total_count = user_mgr.list_users(query)

        _query = {
            'filter': [{
                'k': 'project',
                'v': project_vo,
                'o': 'eq'
            }, {
                'k': 'user',
                'v': list(user_vos),
                'o': 'in'
            }]
        }

        prj_map_vos, total_count = self.project_mgr.list_project_maps(_query)

        members = []
        for user_vo in user_vos:
            for prj_map_vo in prj_map_vos:
                if user_vo == prj_map_vo.user:
                    _dic = {
                        'project': prj_map_vo.project,
                        'user': user_vo,
                        'roles': prj_map_vo.roles,
                        'labels': prj_map_vo.labels
                    }

                    members.append(_dic )
                    break

        return members, len(members)

    def _get_roles(self, role_ids, domain_id):
        role_mgr: RoleManager = self.locator.get_manager('RoleManager')
        role_vos, total_count = role_mgr.list_roles({
            'filter': [{
                'k': 'role_id',
                'v': role_ids,
                'o': 'in'
            }, {
                'k': 'domain_id',
                'v': domain_id,
                'o': 'eq'
            }]
        })

        if len(role_ids) != total_count:
            raise ERROR_NOT_FOUND(key='roles', value=str(role_ids))

        return role_vos

    def _check_exist_resource(self, params):
        # TODO: Check exist resource in project group
        pass

    def _get_user(self, user_id, domain_id):
        user_mgr: UserManager = self.locator.get_manager('UserManager')
        return user_mgr.get_user(user_id, domain_id)

    def _is_exist_member(self, project_id, user_vo, domain_id):
        query_filter = [
            {'k': 'project_id', 'v': project_id, 'o': 'eq'},
            {'k': 'user', 'v': user_vo, 'o': 'eq'}
        ]

        project_map_vos, total_count = self.project_mgr.list_project_maps({'filter': query_filter})
        if total_count == 0:
            return False
        else:
            return True

    @staticmethod
    def _check_role_type(user_role_vos, project_role_vos):
        for role_vo in user_role_vos:
            if role_vo.role_type == 'SYSTEM':
                raise ERROR_SYSTEM_ROLE_USER()

        for role_vo in project_role_vos:
            if role_vo.role_type != 'PROJECT':
                raise ERROR_ONLY_PROJECT_ROLE_TYPE_ALLOWED()
