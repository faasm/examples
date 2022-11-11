from invoke import Collection

from . import cli
from . import data
from . import docker
from . import format_code
from . import git
from . import lammps
from . import lulesh

ns = Collection(
    cli,
    data,
    docker,
    format_code,
    git,
    lammps,
    lulesh,
)
