from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.pycharm")
use_plugin("python.install_dependencies")
use_plugin("python.coverage")

default_task = "publish"


@init
def initialize(project):
    
    project.version = "0.1.1"
    
    project.build_depends_on('Tkinter', 'ttk', 'networkx')
    project.build_depends_on('scipy', 'PIL')
    project.build_depends_on('pympler', 'simpy', 'sklearn')
