import os
import yaml
from typing import Any, IO
from cerberus import Validator

class VarException(Exception):
    pass

class Loader(yaml.SafeLoader):
    """Customized YAML Loader"""

    def __init__(self, stream: IO) -> None:
        """Initialise Custom YAML Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

class VarFileManager:
    """ variable manager class """
    def __init__(self, f):
        self._set_vfile_schema()
        yaml.add_constructor('!env', self._env, Loader)
        with open(f) as vfile:
            self.vars = yaml.load(vfile, Loader=Loader)
        self._validate_vars()
    
    def _env(self, loader: Loader, node: yaml.Node) -> Any:
        """
        _env is a custom method passed to the yaml Loader to provide
        the ability to load yaml values from environment variables.
        """
        if node.value in os.environ:
            return os.environ[node.value]
        raise VarException("Undefined environment variable '%s' referenced in provided var file." % (node.value))
    
    def _validate_vars(self):
        """
        _validate_vars will validate the vars set by the provided var file according to the defined var file schema.
        """
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
            
            raise VarException(error_msg)

    def _set_vfile_schema(self):
        """ 
        _set_vfile_schema is an internal private method that simply defines the validation schema of a var file 
        """
        self.varfile_schema = {
            'url': {
                'type': 'string',
                'required': False
            },
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