import json
import requests

class TFEnterpriseVariableAPI():
    """ Terraform Enterprise Variable API wrapper """
    def __init__(self, token, org, workspace, url):
        self.url                      = url
        self.headers                  = {}
        self.headers["Authorization"] = "Bearer %s" % (token)
        self.headers["Content-Type"]  = "application/vnd.api+json"
        self.workspace_id             = self.get_workspace_id(org, workspace)

    def get_workspace_id(self, org, workspace):
        # NOTE: consider caching the results from this to minimize future requests
        workspaces = requests.get("%s/api/v2/organizations/%s/workspaces" % (self.url, org), headers=self.headers).json()
        for ws in workspaces['data']:
            if workspace == ws['attributes']['name']:
                return ws['id']
        return False

    def get_variables(self):
        """ returns a list of variables in the defined workspace. """
        return requests.get("%s/api/v2/workspaces/%s/vars" % (self.url, self.workspace_id), headers=self.headers).json()['data']

    # TODO: consider implementing
    # def get_variable(self):
    #     pass

    def create_variable(self, var):
        payload = {}
        payload['data'] = {}
        payload['data']['type'] = "vars"
        payload['data']['attributes'] = var
        r = requests.post("%s/api/v2/workspaces/%s/vars" % (self.url, self.workspace_id), headers=self.headers, json=payload)

    def update_variable(self, id, var):
        payload = {}
        payload['data'] = {}
        payload['data']['type'] = "vars"
        payload['data']['attributes'] = var
        r = requests.patch("%s/api/v2/workspaces/%s/vars/%s" % (self.url, self.workspace_id, id), headers=self.headers, json=payload)

    def delete_variable(self, id):
        r = requests.delete("%s/api/v2/workspaces/%s/vars/%s" % (self.url, self.workspace_id, id), headers=self.headers)