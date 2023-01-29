from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: swat.az.vf_marvin_inventory
    author:
      - Oscar Rylin oscar.rylin@donkey.com
    plugin_type: inventory
    short_description: Returns Ansible inventory from Marvin
    description: Returns Ansible inventory from Marvin
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['swat.az.vf_marvin_inventory']
      api_url:
        description: URI towards AnsibleInventory REST interface
        required: false
      vf_identifier:
        description: SLA, VT, CA, VF-identifier (see docs)
        required: false
'''

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError
import json
import requests

class InventoryModule(BaseInventoryPlugin):
    NAME = 'swat.az.vf_marvin_inventory'

    def verify_file(self, path):
        '''Marvin configuration file?
        '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            #base class verifies that file exists 
            #and is readable by current user
            if path.endswith(('marvin.yaml', 'marvin.yml')):
                valid = True
            return valid

    def parse(self, inventory, loader, path, cache):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)
        try:
            # Store the options from the YAML file
            self.plugin = self.get_option('plugin')
            self.api_url = self.get_option('api_url')
            self.vf_identifier = self.get_option('vf_identifier')
        except Exception as e:
            raise AnsibleParserError('All correct options required: {}'.format(e))

        self._populate()


    def _get_marvin_data(self):
        #response = requests.get(self.api_url)
        #if response.status_code != 200:
        #raise ValueError(f"Failed to fetch data from API. Status code: {response.status_code}")
        #return json.loads(response.text)
        return false

    def _populate(self):
        file = open('/tmp/json.txt')
        d = file.read()
        data = json.loads(d)
        file.close()

        for item in data['servers']:
            hostname = item['PrimaryNodeName']
            self.inventory.add_host(hostname)
            self.inventory.set_variable(hostname, 'env', item['BMC_Environment'])
            self.inventory.set_variable(hostname, 'osfamily', item['BMC_OS_OperatingSystem'])


