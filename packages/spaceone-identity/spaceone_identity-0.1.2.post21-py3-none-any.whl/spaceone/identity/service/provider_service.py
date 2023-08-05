from spaceone.core import cache
from spaceone.core.service import *
from spaceone.identity.manager.provider_manager import ProviderManager


@authentication_handler
@authorization_handler
@event_handler
class ProviderService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_mgr: ProviderManager = self.locator.get_manager('ProviderManager')

    @transaction
    @check_required(['provider', 'name'])
    def create_provider(self, params):
        # TODO: validate a template data
        # TODO: validate a capability data
        return self.provider_mgr.create_provider(params)

    @transaction
    @check_required(['provider'])
    def update_provider(self, params):
        # TODO: validate a template data
        # TODO: validate a capability data
        return self.provider_mgr.update_provider(params)

    @transaction
    @check_required(['provider'])
    def delete_provider(self, params):
        self.provider_mgr.delete_provider(params['provider'])

    @transaction
    @check_required(['provider'])
    def get_provider(self, params):
        self._create_default_provider()
        return self.provider_mgr.get_provider(params['provider'])

    @transaction
    @append_query_filter(['provider', 'name'])
    def list_providers(self, params):
        self._create_default_provider()
        return self.provider_mgr.list_providers(params.get('query', {}))

    @cache.cacheable(key='provider:default:init', backend='local')
    def _create_default_provider(self):
        provider_vos, total_count = self.provider_mgr.list_providers()
        if total_count == 0:
            self.provider_mgr.create_default_providers()

        return True
