"""Convenience Python module for Cloud One Conformity

To use this module, you must set the following environment variables:

* `CC_API_KEY`
* `CC_REGION`

## Example

    from onnlogger import Loggers
    from pprint import pprint

    # Create a `Loggers` object and pass it into `Conformity`
    logger = Loggers(logger_name='Conformity', console_logger=True, log_level='INFO', log_file_path='/tmp/log')
    conformity = Conformity(logger)

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
               'id': 'fgsVSA_43',
               'relationships': {'organisation': {'data': {'id': 'asf34asdFs2',
                                                           'type': 'organisations'}}},
               'type': 'accounts'}]}

## Installation

    pip3 install onnconformity

## Contact

* Code: [onnconformity](https://github.com/OzNetNerd/onnconformity)
* Blog: [oznetnerd.com](https://oznetnerd.com)
* Email: [will@oznetnerd.com](mailto:will@oznetnerd.com)

"""

from .conformity import Conformity
