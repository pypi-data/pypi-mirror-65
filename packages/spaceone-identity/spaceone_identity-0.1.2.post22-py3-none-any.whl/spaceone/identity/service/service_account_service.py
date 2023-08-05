from jsonschema import validate

from spaceone.core.service import *
from spaceone.core.error import *
from spaceone.identity.manager.service_account_manager import ServiceAccountManager
from spaceone.identity.manager.project_manager import ProjectManager
from spaceone.identity.manager.provider_manager import ProviderManager


@authentication_handler
@authorization_handler
@event_handler
class ServiceAccountService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_account_mgr: ServiceAccountManager = self.locator.get_manager('ServiceAccountManager')

    @transaction
    @check_required(['name', 'data', 'provider', 'domain_id'])
    def create_service_account(self, params):
        self._check_data(params['data'], params['provider'])

        if 'project_id' in params:
            params['project'] = self._get_project(params['project_id'], params['domain_id'])

        return self.service_account_mgr.create_service_account(params)

    @transaction
    @check_required(['service_account_id', 'domain_id'])
    def update_service_account(self, params):
        service_account_id = params['service_account_id']
        domain_id = params['domain_id']

        service_account_vo = self.service_account_mgr.get_service_account(service_account_id, domain_id)

        if 'data' in params:
            self._check_data(params['data'], service_account_vo.provider)

        if 'project_id' in params:
            params['project'] = self._get_project(params['project_id'], params['domain_id'])
            # TODO: Change all secrets project_id

        return self.service_account_mgr.update_service_account_by_vo(params, service_account_vo)

    @transaction
    @check_required(['service_account_id', 'domain_id'])
    def delete_service_account(self, params):
        self.service_account_mgr.delete_service_account(params['service_account_id'], params['domain_id'])

    @transaction
    @check_required(['service_account_id', 'domain_id'])
    def get_service_account(self, params):
        return self.service_account_mgr.get_service_account(params['service_account_id'], params['domain_id'])

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['service_account_id', 'name', 'provider', 'project_id', 'domain_id'])
    def list_service_accounts(self, params):
        return self.service_account_mgr.list_service_accounts(params.get('query', {}))

    def _check_data(self, data, provider):
        provider_mgr: ProviderManager = self.locator.get_manager('ProviderManager')
        provider_vo = provider_mgr.get_provider(provider)
        schema = provider_vo.template.get('service_account', {}).get('schema', [])
        try:
            validate(instance=data, schema=schema)
        except Exception as e:
            raise ERROR_INVALID_PARAMETER(key='data', reason=e.message)

    def _get_project(self, project_id, domain_id):
        project_mgr: ProjectManager = self.locator.get_manager('ProjectManager')
        return project_mgr.get_project(project_id, domain_id)
