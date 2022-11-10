from invoke import Collection

from . import data
from . import docker
from . import format_code
from . import git
from . import lammps

ns = Collection(
    data,
    docker,
    format_code,
    git,
    lammps,
)
