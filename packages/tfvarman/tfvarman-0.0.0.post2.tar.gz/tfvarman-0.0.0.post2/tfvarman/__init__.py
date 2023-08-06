import os
import yaml
import json
import requests
from tabulate import tabulate
from typing import Any, IO
from cerberus import Validator

class Loader(yaml.SafeLoader):
    """Customized YAML Loader"""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

def _config_env(loader: Loader, node: yaml.Node) -> Any:
        """set value of key at node from environment variable"""
        if node.value in os.environ:
            return os.environ[node.value]
        raise Exception("Undefined environment variable '%s' referenced in provided var file." % (node.value))

class TFVarMan:

    def __init__(self, args, url='https://app.terraform.io'):
        self.args = args
        self.url = url

        # define schema for varfile
        self.varfile_schema = {
            'envtoken': {
                'type': 'string',
                'required': True
            },
            'organization': {
                'type': 'string',
                'required': True
            },
            'workspace': {
                'type': 'string',
                'required': True
            },
            'variables': {
                'type': 'list',
                'required': True,
                'nullable': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'key': {
                            'type': 'string',
                            'required': True
                        },
                        'value': {
                            'type': 'string',
                            'required': True
                        },
                        'category': {
                            'type': 'string',
                            'allowed': ['env', 'terraform'],
                            'default': 'terraform'
                        },
                        'description': {
                            'type': 'string'
                        },
                        'hcl': {
                            'type': 'boolean',
                            'default': False
                        },
                        'sensitive': {
                            'type': 'boolean',
                            'default': False
                        }
                    }

                },
            }
        }

        yaml.add_constructor('!env', _config_env, Loader)
        
        with open(args['<varfile>']) as vfile:
            self.vars = yaml.load(vfile, Loader=Loader)
        
        # validate var file
        self.validator = Validator(self.varfile_schema)
        
        if not self.validator.validate(self.vars):
            error_msg = "The provided var file has the following errors: \n"
            # print(self.validator.errors)
            for k in self.validator.errors:
                if k == 'variables':
                    # error_msg += "\n%s: %s\n" % (k, self.validator.errors[k][0])
                    error_msg += "\n%s:\n" % (k)
                    for msg in self.validator.errors[k]:
                        for idx in msg:
                            for err in msg[idx]:
                                for k in err:
                                    error_msg += "%s) %s: %s\n" % (idx + 1, k, err[k][0])
                else:
                    error_msg += "\n%s: %s\n" % (k, self.validator.errors[k][0])
            
            raise Exception(error_msg)
        
        if self.vars['envtoken'] not in os.environ:
            raise Exception("provided token key '%s' is not a valid environment variable." % (self.vars['envtoken']))
        self.token = os.environ[self.vars['envtoken']]
        self.headers = {
            "Authorization": "Bearer %s" % (self.token),
            "Content-Type": "application/vnd.api+json"
        }
        
    def _get_ws_id(self):
        
        self.workspaces = requests.get("%s/api/v2/organizations/%s/workspaces" % (self.url, self.vars['organization']), headers=self.headers).json()
        for ws in self.workspaces['data']:
            if self.vars['workspace'] == ws['attributes']['name']:
                return ws['id']
    
    def _get_variables_in_ws(self):
        # TODO: add checks to ensure variables were returned successfully
        return requests.get("%s/api/v2/workspaces/%s/vars" % (self.url, self._get_ws_id()), headers=self.headers).json()['data']
    
    def _create_variable_in_ws(self, var):
        # TODO: add var validation to this method
        payload = {}
        payload['data'] = {}
        payload['data']['type'] = "vars"
        payload['data']['attributes'] = var
        r = requests.post("%s/api/v2/workspaces/%s/vars" % (self.url, self._get_ws_id()), headers=self.headers, json=payload)
    
    def _update_variable_in_ws(self, var_id, new_var):
        payload = {}
        payload['data'] = {}
        payload['data']['type'] = "vars"
        payload['data']['attributes'] = new_var
        r = requests.patch("%s/api/v2/workspaces/%s/vars/%s" % (self.url, self._get_ws_id(), var_id), headers=self.headers, json=payload)

    def _remove_variable_in_ws(self, var_id):
        r = requests.delete("%s/api/v2/workspaces/%s/vars/%s" % (self.url, self._get_ws_id(), var_id), headers=self.headers)

    def sync(self):
        """
        sync will sync the variables that are defined in the provided varfile with the defined workspace.
        If the variable does not exist, it will be created.
        If the variable already exist, it will be replaced.
        If the variable exist in the workspace, but is not defined in the varfile, it will be removed.
        """
        # GET A LIST OF CURRENT VARIABLES
        variables = self._get_variables_in_ws()
        # if the variable already exist, we'll issue an update command
        # if there are variables we are adding, we'll issue a create command
        # if there are variables we are removing, we'll issue a delete command.
        # The provided varfile will be considered the source of truth.
        envvars = {}
        tfvvars = {}

        if self.vars['variables'] is None:
            self.vars['variables'] = []

        for k in variables:
            if k['attributes']['category'] == 'env':
                envvars[k['attributes']['key']] = k['id']
            if k['attributes']['category'] == 'terraform':
                tfvvars[k['attributes']['key']] = k['id']
        
        # # payload['data']['type'] = "vars"
        for var in self.vars['variables']:
            if 'category' not in var.keys():
                var['category'] = 'terraform'
            if 'description' not in var.keys():
                var['description'] = ''
            if 'hcl' not in var.keys():
                var['hcl'] = False
            if 'sensitive' not in var.keys():
                var['sensitive'] = False

            if var['key'] in envvars.keys() and var['category'] == 'env':
                # we need to update the variable
                print("UPDATING %s ..." % (var['key']))
                self._update_variable_in_ws(envvars[var['key']], var)
                del envvars[var['key']]
            
            elif var['key'] in tfvvars.keys() and var['category'] == 'terraform':
                # we need to update the variable
                print("UPDATING %s ..." % (var['key']))
                self._update_variable_in_ws(tfvvars[var['key']], var)
                del tfvvars[var['key']]
            
            elif var['key'] not in envvars and var['key'] not in tfvvars:
                # we need to create the variable
                print("CREATING %s ..." % var['key'])
                self._create_variable_in_ws(var)
            else:
                print("shouldn't get here..")
                pass
        
        for var in envvars:
            print("REMOVING %s ..." % (var))
            self._remove_variable_in_ws(envvars[var])
        
        for var in tfvvars:
            print("REMOVING %s ..." % (var))
            self._remove_variable_in_ws(tfvvars[var])


    def show(self):
        """
        show will show the available variables in the defined workspace
        """
        variables = self._get_variables_in_ws()
        headers = ['Key', 'Value', 'Sensitive', 'Type', 'HCL']
        envdata = []
        tfvdata = []
        for k in variables:
            if k['attributes']['category'] == 'env':
                envdata.append([
                    k['attributes']['key'],
                    k['attributes']['value'],
                    k['attributes']['sensitive'],
                    k['attributes']['category'],
                    k['attributes']['hcl']
                ])
            if k['attributes']['category'] == 'terraform':
                tfvdata.append([
                    k['attributes']['key'],
                    k['attributes']['value'],
                    k['attributes']['sensitive'],
                    k['attributes']['category'],
                    k['attributes']['hcl']
                ])

        print("TERRAFORM VARIABLES:\n")
        print(tabulate(tfvdata, headers=headers))
        print("\n")
        print("ENVIRONMENT VARIABLES:\n")
        print(tabulate(envdata, headers=headers))
