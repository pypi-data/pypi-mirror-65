# Imports go here!
from .diario import Diario
from .wikipages import WikiPage
from .bios import Bio
from .reminders import Reminder
from .triviascores import TriviaScore
from .leagueoflegends import LeagueOfLegends
from .fiorygi import Fiorygi
from .steam import Steam
from .dota import Dota
from .fiorygitransactions import FiorygiTransaction
from .brawlhalla import Brawlhalla
from .polls import Poll
from .pollcomments import PollComment
from .pollvotes import PollVote
from .brawlhalladuos import BrawlhallaDuo

# Enter the tables of your Pack here!
available_tables = [
    Diario,
    WikiPage,
    Bio,
    Reminder,
    TriviaScore,
    LeagueOfLegends,
    Fiorygi,
    Steam,
    Dota,
    FiorygiTransaction,
    Brawlhalla,
    Poll,
    PollComment,
    PollVote,
    BrawlhallaDuo,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__name__ for table in available_tables]
