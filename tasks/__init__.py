from invoke import Collection

from . import cli
from . import data
from . import docker
from . import ffmpeg
from . import format_code
from . import func
from . import git
from . import imagemagick
from . import kernels
from . import lammps
from . import libpng
from . import lulesh
from . import tensorflow

ns = Collection(
    cli,
    data,
    docker,
    ffmpeg,
    format_code,
    func,
    git,
    imagemagick,
    kernels,
    lammps,
    libpng,
    lulesh,
    tensorflow,
)
