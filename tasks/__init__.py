from invoke import Collection

from . import cli
from . import docker
from . import format_code
from . import git
from . import lammps

ns = Collection(
    cli,
    docker,
    format_code,
    git,
    lammps,
)
