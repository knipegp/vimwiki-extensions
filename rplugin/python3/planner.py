import enum
from enum import Enum
import logging
from typing import List

import pynvim


class _AutoName(Enum):
    """Set auto values as their variable name

    Copied from https://docs.python.org/3/library/enum.html#using-automatic-values
    """

    def _generate_next_value_(name, start, count, last_values):
        return name


class PlannerTags(_AutoName):
    """Enumerate the possible tags used by the Planner"""

    todo = enum.auto()
    waiting = enum.auto()
    backlog = enum.auto()
    done = enum.auto()
    cancelled = enum.auto()


@pynvim.plugin
class Planner(object):
    """Display Vimwiki notes in a planner"""

    default_planner_tags: List[PlannerTags] = list(PlannerTags)

    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim
        self.logger = logging.Logger(__name__)

    @pynvim.command("ViewPlanner")
    def view_planner(self):
        self.nvim.api.command("VimwikiMakeDiaryNote")
        self.nvim.api.command("VimwikiRebuildTags")
        self.logger.info(' '.join([str(tag) for tag in self.default_planner_tags]))
        self.nvim.api.command(
            f"VimwikiGenerateTagLinks {' '.join([tag.value for tag in self.default_planner_tags])}"
        )
