from invoke import Collection

from . import docker
from . import format_code
from . import git
from . import lammps

ns = Collection(
    docker,
    format_code,
    git,
    lammps,
)
