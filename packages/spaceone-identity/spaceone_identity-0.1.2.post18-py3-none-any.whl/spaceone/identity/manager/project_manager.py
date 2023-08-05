# -*- coding: utf-8 -*-
import logging
from spaceone.core.manager import BaseManager
from spaceone.identity.model.project_model import Project, ProjectMemberMap
from spaceone.identity.model.project_group_model import ProjectGroup

_LOGGER = logging.getLogger(__name__)


class ProjectManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_model: Project = self.locator.get_model('Project')
        self.project_group_model: ProjectGroup = self.locator.get_model('ProjectGroup')
        self.project_map_model: ProjectMemberMap = self.locator.get_model('ProjectMemberMap')

    def create_project(self, params):
        def _rollback(project_vo):
            _LOGGER.info(f'[create_project._rollback] Delete project : {project_vo.name} ({project_vo.project_id})')
            project_vo.delete()

        project_vo: Project = self.project_model.create(params)
        self.transaction.add_rollback(_rollback, project_vo)

        return project_vo

    def update_project(self, params):
        return self.update_project_by_vo(params, self.get_project_group(params['project_id'],
                                                                        params['domain_id']))

    def update_project_by_vo(self, params, project_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[update_project._rollback] Revert Data : {old_data["name"]} ({old_data["project_id"]})')
            project_vo.update(old_data)

        self.transaction.add_rollback(_rollback, project_vo.to_dict())

        return project_vo.update(params)

    def delete_project(self, project_id, domain_id):
        self.delete_project_by_vo(self.get_project(project_id, domain_id))

    def add_member(self, project_vo, user_vo, roles, labels):
        def _rollback(old_data):
            _LOGGER.info(f'[add_member._rollback] Revert Data : {old_data["name"]} ({old_data["project_id"]})')
            project_vo.update(old_data)

        self.transaction.add_rollback(_rollback, project_vo.to_dict())

        return project_vo.append('members', {
            'user': user_vo,
            'roles': roles,
            'labels': labels
        })

    def modify_member(self, project_vo, user_vo, roles, labels):
        def _rollback(old_data):
            _LOGGER.info(f'[modify_member._rollback] Revert Data : {old_data["name"]} ({old_data["project_id"]})')
            project_vo.update(old_data)

        self.transaction.add_rollback(_rollback, project_vo.to_dict())

        project_map_vos, map_total_count = self.project_map_model.query({
            'filter': [{
                'k': 'project',
                'v': project_vo,
                'o': 'eq'
            }, {
                'k': 'user',
                'v': user_vo,
                'o': 'eq'
            }]
        })

        project_map_vo = project_map_vos[0]
        project_map_vo.update({
            'roles': roles,
            'labels': labels
        })

        return project_vo

    def remove_member(self, project_vo, user_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[remove_member._rollback] Revert Data : {old_data["name"]} ({old_data["project_id"]})')
            project_vo.update(old_data)

        self.transaction.add_rollback(_rollback, project_vo.to_dict())

        project_vo.remove('members', user_vo)

    def get_project(self, project_id, domain_id):
        return self.project_model.get(project_id=project_id, domain_id=domain_id)

    def list_projects(self, query):
        return self.project_model.query(**query)

    def list_project_maps(self, query):
        return self.project_map_model.query(**query)

    @staticmethod
    def delete_project_by_vo(project_vo):
        project_vo.delete()

