from ansible.errors import AnsibleFilterError

from jinja2 import Environment, StrictUndefined,DebugUndefined, Undefined

def retemplate(template, variables):
    env = Environment(undefined=StrictUndefined)
    return env.from_string(str(template)).render(variables)

class FilterModule(object):
    ''' URI filter '''

    def filters(self):
        return {
            'retemplate': retemplate
        }
