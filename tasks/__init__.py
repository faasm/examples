from invoke import Collection

from . import git
from . import lammps

ns = Collection(
    git,
    lammps,
)
