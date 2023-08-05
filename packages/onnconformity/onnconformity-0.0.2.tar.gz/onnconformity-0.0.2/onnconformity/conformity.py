import os
import sys
import requests
import json
from pprint import pformat

CONFORMITY_ACCOUNT_ID = '717210094962'
CC_REGIONS = [
    'eu-west-1',
    'ap-southeast-2',
    'us-west-2',
]


class Conformity:
    def __init__(self, logger):
        """Description:
            Convenience Python module for Cloud One Conformity

        Args:
            logger (onnlogger.Loggers): An instance of `onnlogger.Loggers`

        Example:
            Example usage:

                from onnlogger import Loggers

                logger = Loggers(logger_name='Conformity', console_logger=True, log_level='INFO', log_file_path='/tmp/log')
                conformity = Conformity(logger)
        """
        self.logger = logger

        try:
            self.logger.entry('info', 'Obtaining required environment variables...')
            self.cc_region = os.environ['CC_REGION'].lower()

            if self.cc_region not in CC_REGIONS:
                sys.exit('Error: Please ensure "CC_REGION" is set to a region which is supported by Cloud Conformity')

            self.api_key = os.environ['CC_API_KEY']

        except KeyError:
            sys.exit('Error: Please ensure all environment variables are set')

        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'ApiKey ' + self.api_key
        }

        self.org_id = self._get_org_id()

    def delete_subscription(self, conformity_id) -> dict:
        """Delete a Conformity subscription

        Args:
            conformity_id (str): Subscription ID

        Example:
            Example usage:

                deleted_subscription = conformity.delete_subscription('57KARHFRW')
                print(deleted_subscription)
                {'meta': {'status': 'sent'}}

        Returns:
            dict

        """
        self.logger.entry('info', f'Deleting subscription ID {conformity_id}...')
        account_endpoint = f'https://{self.cc_region}-api.cloudconformity.com/v1/accounts/{conformity_id}'
        resp = requests.delete(account_endpoint, headers=self.headers)
        resp_json = json.loads(resp.text)
        self._check_error(resp_json)

        self.logger.entry('debug', 'Done')
        return resp_json

    def list_subscriptions(self) -> dict:
        """List Conformity subscriptions

        Args:
            conformity_id (str): Subscription ID

        Example:
            Example usage:

                from pprint import pprint
                subscriptions = conformity.list_subscriptions()
                pprint(subscriptions)
                {'data': [{'attributes': {'access': None,
                          'awsaccount-id': '123456789012',
                          'cloud-type': 'aws',
                          'cost-package': True,
                          'created-date': 1585526686560,
                          'environment': None,
                          'has-real-time-monitoring': True,
                          'last-checked-date': 1585711290751,
                          'last-monitoring-event-date': None,
                          'last-notified-date': 1585711291075,
                          'name': 'Demo',
                          'security-package': True,
                          'tags': None},
                'id': 'dg4Sfsw23',
                'relationships': {'organisation': {'data': {'id': 'dsaer28hw',
                                                            'type': 'organisations'}}},
                'type': 'accounts'}]}

        Returns:
            dict
        """

        self.logger.entry('info', 'Getting list of Conformity subscriptions...')
        account_endpoint = f'https://{self.cc_region}-api.cloudconformity.com/v1/accounts/'

        resp = requests.get(account_endpoint, headers=self.headers)
        resp_json = json.loads(resp.text)
        self._check_error(resp_json)

        self.logger.entry('info', f'Found subscriptions:\n{pformat(resp_json)}')

        return resp_json

    @staticmethod
    def _check_error(json_payload) -> None:
        error_message = json_payload.get('Message') or json_payload.get('errors')

        if error_message:
            sys.exit(f'Error: {error_message}')

    def _get_org_id(self) -> str:
        """Gets the Conformity ID

        Example:
            Example usage:

            org_id = conformity._get_org_id()
            print(org_id)
            g34242f5y-2345-345g-234d-gi473bdlfng7

        Returns:
            str
        """
        self.logger.entry('info', 'Getting Conformity Organization ID...')
        org_endpoint = f'https://{self.cc_region}-api.cloudconformity.com/v1/organisation/external-id/'
        resp = requests.get(org_endpoint, headers=self.headers)
        resp_json = json.loads(resp.text)
        self._check_error(resp_json)

        org_id = resp_json['data']['id']
        self.logger.entry('debug', {org_id})

        return org_id

    def check_subscription_exists(self, aws_account_id) -> dict:
        """Checks if a Conformity subscription exists for an AWS account

        Note: `list_subscriptions()` is called  every time as CC does not prevent users from creating multiple
        subscriptions for the same account/ARN

        Args:
            aws_account_id (str): AWS account ID

        Example:
            Example usage:

                from pprint import pprint

                existing_account = conformity.check_subscription_exists('098765432109')
                pprint(existing_account)
                {'attributes': {'access': None,
                             'awsaccount-id': '098765432109',
                             'cloud-type': 'aws',
                             'cost-package': False,
                             'created-date': 1585780981170,
                             'environment': '',
                             'has-real-time-monitoring': False,
                             'name': 'Lab1',
                             'security-package': True,
                             'settings': {'rules': []},
                             'status': 'ACTIVE',
                             'tags': None},
                'id': '462FSFGGR',
                'relationships': {'organisation': {'data': {'id': 'sdes23216',
                                                            'type': 'organisations'}}},
                'type': 'accounts'}}

        Returns:
            dict
        """
        self.logger.entry('info', f'Checking if AWS account ID {aws_account_id} already has a Conformity '
                                  f'subscription...')

        list_of_subscriptions = self.list_subscriptions()

        for entry in list_of_subscriptions['data']:
            aws_id = entry['attributes'].get('awsaccount-id')

            if not aws_id:
                continue

            if aws_id == aws_account_id:
                self.logger.entry('debug', f'It does exist:\n{pformat(entry)}')

                return entry

            self.logger.entry('debug', f'AWS account ID {aws_account_id} does not have a Conformity subscription')

            return dict()

    def create_subscription(self, aws_account_id, role_arn, account_name, account_env='', cost_package=False,
                            rtm=False) -> dict:
        """Description:
            Create a Conformity subscription for an AWS account

        Note: `list_subscriptions()` is called  every time as CC does not prevent users from creating multiple
        subscriptions for the same account/ARN

        Args:
            aws_account_id (str): AWS account ID
            role_arn (str): Role ARN for Conformity's access
            account_name (str): Conformity account name
            account_env (str): Conformity account environment name
            cost_package (bool): Enable cost package
            rtm (bool): Enable RTM package

        Example:
            Example usage:

                new_subscription = conformity.create_subscription('098765432109', 'arn:aws:iam::098765432109:role/CloudConformity', 'Lab1')
                pprint(new_subscription)
                {'data': {'attributes': {'access': None,
                         'awsaccount-id': '098765432109',
                         'cloud-type': 'aws',
                         'cost-package': False,
                         'created-date': 1585780981170,
                         'environment': '',
                         'has-real-time-monitoring': False,
                         'name': 'Lab1',
                         'security-package': True,
                         'settings': {'rules': []},
                         'status': 'ACTIVE',
                         'tags': None},
                'id': '462FSFGGR',
                'relationships': {'organisation': {'data': {'id': 'sdefgw3r6',
                                                            'type': 'organisations'}}},
                'type': 'accounts'}}

        Returns:
            dict
        """
        subscription_exists = self.check_subscription_exists(aws_account_id)

        if subscription_exists:
            self.logger.entry('debug', f'Skipping subscription creation for for AWS account ID {aws_account_id} as it '
                                       f'is not required')

        self.logger.entry('info', f'Creating Conformity subscription for AWS account ID {aws_account_id}...')

        account_endpoint = f'https://{self.cc_region}-api.cloudconformity.com/v1/accounts/'

        cost_package = cost_package.upper() if cost_package else False
        rtm = rtm.upper() if rtm else False

        data = {
            'data': {
                'type': 'accounts',
                'attributes': {
                    'name': account_name,
                    'environment': account_env,
                    'access': {
                        'keys': {
                            'roleArn': role_arn,
                            'externalId': self.org_id,
                        }
                    },
                    'costPackage': cost_package,
                    'hasRealTimeMonitoring': rtm,
                }
            }
        }

        data = json.dumps(data)
        self.logger.entry('debug', f'Sending payload:\n{pformat(data)}')

        resp = requests.post(account_endpoint, headers=self.headers, data=data)
        resp_json = json.loads(resp.text)
        self._check_error(resp_json)

        self.logger.entry('debug', f'Done:\n{pformat(resp_json)}')
        return resp_json
