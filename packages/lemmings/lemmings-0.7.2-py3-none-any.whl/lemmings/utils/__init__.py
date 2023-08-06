from lemmings.utils.colors import *
from lemmings.utils.const import *
from lemmings.utils.coroutine import *
from lemmings.utils.influx import *
from lemmings.utils.parsing import *
from lemmings.utils.prometheus import *
from lemmings.utils.timer import *
from lemmings.utils.utils import *


def _num(num):
    return f"{num:4d}"
    # return Color.underline(f"{num:4d}")
    # return Color.back(Color.cyan, f"{num:4d}")