"""Plugins Module.

This Module provides the interface for extending the functionality
of Markdown Meta Extension by adding custom CallableHandler objects.

Common CallableHandler objects are included and imported here.

Author:
    Martin Schorfmann
Since:
    2020-01-26
Version:
    2020-02-25
"""

import markdown_meta_extension.plugins.file_system_plugin
import markdown_meta_extension.plugins.package_plugin
import markdown_meta_extension.plugins.module_plugin
import markdown_meta_extension.plugins.jinja_template_plugin
from .spec import CallableWrapper, CallableHandler

# TODO: Implement call behavior for lists (i.e. for-each)
