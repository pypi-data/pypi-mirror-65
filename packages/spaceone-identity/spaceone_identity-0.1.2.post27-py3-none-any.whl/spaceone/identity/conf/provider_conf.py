DEFAULT_PROVIDERS = [{
    'provider': 'aws',
    'name': 'AWS',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'account_id': {
                        'title': 'Account ID',
                        'type': 'string',
                        'minLength': 4
                    }
                },
                'required': ['account_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['aws_access_key', 'aws_assume_role']
    },
    'tags': {
        'color': '#FF9900',
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws.svg',
        'external_link_template': 'https://{{data.account_id}}.signin.aws.amazon.com/console'
    }
}, {
    'provider': 'google_cloud',
    'name': 'Google Cloud',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'sa_name': {
                        'title': 'Service Account',
                        'type': 'string',
                        'minLength': 4
                    },
                    'project_id': {
                        'title': 'Project ID',
                        'type': 'string',
                        'minLength': 4
                    }
                },
                'required': ['sa_name', 'project_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['google_application_credentials']
    },
    'tags': {
        'color': '#4285F4',
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/google_cloud.svg'
    }
}, {
    'provider': 'azure',
    'name': 'Microsoft Azure',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'subscription_id': {
                        'title': 'Subscription ID',
                        'type': 'string',
                        'minLength': 4
                    }
                },
                'required': ['subscription_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['azure_client_secret']
    },
    'tags': {
        'color': '#00BCF2',
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure.svg'
    }
}]
