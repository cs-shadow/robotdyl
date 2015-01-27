from docutils import nodes
from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst import Directive
import docutils.parsers.rst.directives as directives

def setup(app):
    app.add_directive('screenshot', Screenshot)

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

    def _focus(arg_str):
        """ Returns id and annotation after splitting input string.

        First argument should be the id. An optional annotation can follow.
        Everything after an initial space will be considered the annotation.
        """
        split_str = arg_str.split(' ', 1)
        if len(split_str) == 1:
            return {'id': split_str[0], 'annotation': ''}
        else:
            return {'id': split_str[0], 'annotation': split_str[1]}

    option_spec = Image.option_spec.copy()
    option_spec['url'] = directives.unchanged
    option_spec['focus'] = _focus

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

        if 'url' in self.options:
            return_nodes.append(nodes.Text("URL is '%s'.  " % self.options['url']))
        if 'focus' in self.options:
            return_nodes.append(nodes.Text("DOM id is '%s' and annotation is '%s'.  " % (self.options['focus']['id'], self.options['focus']['annotation'])))

        return return_nodes
