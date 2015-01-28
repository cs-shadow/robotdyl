from docutils import nodes
from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst import Directive
import docutils.parsers.rst.directives as directives

import re

from exceptions import NotImplementedError

def setup(app):
    app.add_directive('screenshot', Screenshot)

def _parse_focus(arg_str):
    """ Returns id and annotation after splitting input string.

    First argument should be the id. An optional annotation can follow.
    Everything after an initial space will be considered the annotation.
    """
    split_str = arg_str.split(' ', 1)
    if len(split_str) == 1:
        return {'id': split_str[0], 'annotation': ''}
    else:
        return {'id': split_str[0], 'annotation': split_str[1]}

def _parse_command(command):
    # Return a dictionary with
    #   action: the action type (if it's recognized)
    #   options: a list of options
    raise NotImplementedError()

def _parse_login(username, password, submit=""):
    # username and password are just strings, but cast submit to a bool
    # runhandler should be "_login_handler"
    raise NotImplementedError()

def _parse_nav_steps(arg_str):
    """ Here's how to specify the navigation steps:
        
        1. selector action [options] ["|" selector action [options]] ...
        2. aliased_action_sequence [options]

        selector will identify the element... for now we'll just implement
            selection by id e.g. "#username-field"
            "NEXT", which just sends a tab keystroke
            "SAME", which just stays focused on the element from the last action
        Where action could be one of "click", "send_keys", or "submit":
            click has no options and just clicks the element
            send_keys sends a sequence of keystrokes specified as a string by options
                (potentially with special characters representing tab, enter, etc.)
            submit submits a form and has no options
        Multiple actions on a page can be specified by putting a | separator,
            and specifying the action using the same syntax.

        aliased_action_sequence is one of a reserved keyword which aliases a common
            sequence of actions as above (or performs special actions unavailable by 
            the regular syntax) potentially with options. Available aliases:

            LOGIN username password [submit], which just navigates to the login page 
                and inputs the given username and password. Submits the form is submit
                is present, otherwise not.

        Returns a dictionary with:
            runhandler: reference to function invoked in the run method
            args:       a list of positional arguments passed to the runhandler function
    """
    # The alias with its parse function
    ALIASES = [("LOGIN", _parse_login)]

    # First check if we've been passed an aliased_action_sequence
    words = arg_str.split(' ')
    for e in ALIASES:
        if words[0] == e[0]:
            return e[1](*words[1:])

    commands = arg_str.split('|')
    parsed_commands = map(_parse_command, commands)
    many_commands = (len(commands) > 1)
    if many_commands:
        runhandler = "_commands_handler"
        args = parsed_commands
    else:
        runhandler = "_command_handler"
        args = parsed_commands[0]
    return { "runhandler":  runhandler,
             "args":        args}


class Screenshot(Image):
    """ Provides directive to include screenshot based on given options.

    Since it inherits from the Image directive, it can take Image options.
    Right now just stupidly spits out the additional options that I've included.
    If an image is given as an argument, it'll act just like a regular image
    directive.
    """
    required_arguments = 0
    optional_arguments = 1
    has_content = False

    #########################################################
    # Handlers will be invoked in the run method should     #
    # both return appropriate nodes and spawn a process     #
    # to generate the screenshot (once the script is ready).#
    #########################################################
    def _login_handler(self, username, password, submit):
        raise NotImplementedError()

    def _command_handler(self, action, *options):
        raise NotImplementedError()

    def _commands_handler(self, *commands):
        return map(_command_handler, commands)

    # Add options to the image directive.
    option_spec = Image.option_spec.copy()
    option_spec['url'] = directives.unchanged
    option_spec['user-role'] = directives.unchanged
    option_spec['navigation-steps'] = _parse_nav_steps
    option_spec['focus'] = _parse_focus

    def run(self):
        """ Returns list of nodes to appended as screenshot.

        Language xx can be set in conf.py or by:
        make SPHINXOPTS="-D language=xx" html
        Build language can be accessed from the BuildEnvironment.
        """
        # sphinx.environment.BuildEnvironment
        env = self.state.document.settings.env
        language = env.config.language
        return_nodes = []

        if len(self.arguments) == 1:
            (image_node,) = Image.run(self)
            return_nodes.append(image_node)

        return_nodes.append(nodes.Text("Language code is '%s'.  " % language))

        if 'focus' in self.options:
            return_nodes.append(nodes.Text("DOM id is '%s' and annotation is '%s'.  " % (self.options['focus']['id'], self.options['focus']['annotation'])))
        
        if 'user-role' in self.options:
            # Assign something to an instance variable so it can be used in other methods...
            pass
        else:
            # ...and have a default user
            pass
        
        if 'url' in self.options:
            # Assign something to an instance variable so it can be used in other methods
            pass

        if 'url' in self.options and 'navigation-steps' in self.options:
            runhandler = self.options['navigation-steps']['runhandler']
            args = self.options['navigation-steps']['runhandler']
            return_nodes.append(getattr(self, runhandler)(self, *args))

        return return_nodes
