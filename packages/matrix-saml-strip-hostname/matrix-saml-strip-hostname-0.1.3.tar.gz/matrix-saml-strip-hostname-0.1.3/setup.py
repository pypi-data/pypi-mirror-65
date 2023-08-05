# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_saml_strip_hostname']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'matrix-saml-strip-hostname',
    'version': '0.1.3',
    'description': 'SAML mapping provider to strip hostnames from mxids',
    'long_description': "=============================\nMatrix SAML hostname stripper\n=============================\n\nThis mapping provider strips the ``@domain.com`` part from UIDs coming from a SAML2\nidentity provider (IDP). This is useful for example when `using Google Apps as\nan IDP <https://support.google.com/a/answer/6087519?hl=en>`_, to avoid getting\nMatrix IDs like ``jane.doe=40domain.com@domain.com`` (instead you'll get\n``jane.doe@domain.com``).\n\n**Note:** At the time of this writing, the `support for user-configurable\nmapping providers <https://github.com/matrix-org/synapse/pull/6411>`_ hasn't\nbeen released yet. You will probably have to wait for Synapse 1.7 or 1.8, or\ninstall an unreleased version of Synapse.\n\n------------\nInstallation\n------------\n\nRun the following command in the same virtual environment of your Synapse install:\n\n``pip install matrix-saml-strip-hostname``\n\nThen edit the ``homeserver.yaml`` file on your Synapse install to use the new\nmapping provider::\n\n  saml2_config:\n    user_mapping_provider:\n      module: matrix_saml_strip_hostname.mapping_providers.StripHostnameSamlMappingProvider\n\n-------------\nConfiguration\n-------------\n\nThis mapper inherits from `the default mapping provider\n<https://github.com/matrix-org/synapse/blob/fc316a4894912f49f5d0321e533aabca5624b0ba/docs/saml_mapping_providers.md#synapses-default-provider>`_.\nIt will first strip the hostname, and then pass the result to the\n``synapse.handlers.saml_handler.DefaultSamlMappingProvider`` mapping provider.\nThere is no support for disabling this post-processing.\n\nRefer to `the default configuration file\n<https://github.com/matrix-org/synapse/blob/fc316a4894912f49f5d0321e533aabca5624b0ba/docs/sample_config.yaml#L1272>`_\nfor configuration options for the default provider.\n",
    'author': 'Sylvain Fankhauser',
    'author_email': 'sephi@fhtagn.top',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sephii/matrix-saml-strip-hostname',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
