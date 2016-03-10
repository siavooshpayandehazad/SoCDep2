from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.pycharm")
use_plugin("python.install_dependencies")

# use_plugin("python.coverage")

default_task = ['install_dependencies', 'publish']

@init
def initialize(project):
    
    project.version = "0.1.1"
    project.depends_on('networkx')
    # project.depends_on('Tkinter')
    # project.depends_on('ttk')
    project.depends_on('scipy')
    project.depends_on('Pillow')
    project.depends_on('pympler')
    project.depends_on('simpy')
    project.depends_on('sklearn')
    project.depends_on('matplotlib')
    project.depends_on('Image')
