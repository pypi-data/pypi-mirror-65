import os
import sys
import click
import json
from os import path
from .utils.varfile import VarFileManager, VarException
from .utils.api import TFEnterpriseVariableAPI
from tabulate import tabulate

@click.group()
def cli():
  pass

@cli.command()
@click.argument('org')
@click.argument('workspace')
@click.argument('envtoken')
@click.option('--url', 'url')
@click.option('--alias', 'alias')
def init(org, workspace, envtoken, url, alias):
  """ 
  initialize cli to work with a specific workspace\n
  ORG:        organization name\n
  ENVTOKEN:   environment variable to fetch api token from\n
  WORKSPACE:  name of the workspace to select for the current session\n
  URL:        option to provide self hosted Terraform Cloud url\n
  ALIAS:      option to alias the workspace name for CLI use.

  """
  if not envtoken in os.environ:
    print("VARIABLE ERROR: '%s' is not an exported environment variable" % (envtoken))
    sys.exit(1)
  
  session = {
    'org':       org,
    'url':       url or "https://app.terraform.io",
    'token':     os.environ[envtoken],
    'workspace': workspace
  }
  
  # write the session to the /tmp folder for the given workspace
  # TODO: add support for windows environments?
  session_path = "%s/%s.json" % ('/tmp', workspace)
  if alias:
    session_path = "%s/%s.json" % ('/tmp', alias)
  with open(session_path, 'w+') as session_file:
    json.dump(session, session_file)
  
  # verify file exist, and return a message indicating status of initialization
  if path.exists(session_path):
    print("Initalized!")
    sys.exit(0)
  else:
    print("Session initialization failed.")
    sys.exit(0)

# @cli.command()
# def add():
#   """ add a variable to the workspace """
#   pass

# @cli.command()
# def rem():
#   """ remove a variable from the workspace """
#   pass

@cli.command()
@click.argument('WORKSPACE')
def show(workspace):
  """ show variables in the workspace """
  session_path = "%s/%s.json" % ('/tmp', workspace)
  if not path.isfile(session_path):
    print("INIT ERROR: The %s workspace has not been initialized." % (workspace))
    sys.exit(1)
  
  # load the cached session
  with open(session_path, 'r') as session_file:
    session = json.load(session_file)

  # get the variables by making an api call
  api = TFEnterpriseVariableAPI(**session)
  
  variables = api.get_variables()
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
  sys.exit(0)

@cli.command()
@click.argument('varfile')
def sync(varfile):
  """ sync variables from a var file to the workspace """
  # load varfile
  vfile = VarFileManager(varfile)
  url = "https://app.terraform.io"
  if 'url' in vfile.vars:
    url = vfile.vars['url']

  session = {
    'org':       vfile.vars['organization'],
    'url':       url,
    'token':     os.environ[vfile.vars['envtoken']],
    'workspace': vfile.vars['workspace']
  }

  api = TFEnterpriseVariableAPI(**session)
  variables = api.get_variables()

  envvars = {}
  tfvvars = {}

  if vfile.vars['variables'] is None:
      vfile.vars['variables'] = []

  for k in variables:
      if k['attributes']['category'] == 'env':
          envvars[k['attributes']['key']] = k['id']
      if k['attributes']['category'] == 'terraform':
          tfvvars[k['attributes']['key']] = k['id']
  
  # # payload['data']['type'] = "vars"
  for var in vfile.vars['variables']:
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
          print("UPDATING ENV %s ..." % (var['key']))
          api.update_variable(envvars[var['key']], var)
          del envvars[var['key']]
      
      elif var['key'] in tfvvars.keys() and var['category'] == 'terraform':
          # we need to update the variable
          print("UPDATING TF %s ..." % (var['key']))
          api.update_variable(tfvvars[var['key']], var)
          del tfvvars[var['key']]
      
      elif var['key'] not in envvars and var['key'] not in tfvvars:
          # we need to create the variable
          print("CREATING %s ..." % var['key'])
          api.create_variable(var)
      else:
          print("shouldn't get here..")
          pass
  
  for var in envvars:
      print("REMOVING %s ..." % (var))
      api.delete_variable(envvars[var])
  
  for var in tfvvars:
      print("REMOVING %s ..." % (var))
      api.delete_variable(tfvvars[var])

def main():
    """Terraform Enterprise Variable Management CLI"""
    try:
      cli()
    except VarException as varerr:
      print("VARIABLE ERROR: %s" % (str(varerr)))
    except Exception as err:
      print("UNKNOWN ERROR: %s" % (str(err)))
    