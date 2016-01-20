from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.pycharm")
use_plugin("python.install_dependencies")
# use_plugin("python.coverage")

default_task = "publish"


@init
def initialize(project):
    
    project.version = "0.1.1"
    project.build_depends_on('networkx')
    project.build_depends_on('Tkinter')
    project.build_depends_on('ttk')
    project.build_depends_on('scipy')
    project.build_depends_on('PIL', url='https://github.com/python-pillow/Pillow/archive/master.zip')
    project.build_depends_on('pympler')
    project.build_depends_on('simpy')
    project.build_depends_on('sklearn')
