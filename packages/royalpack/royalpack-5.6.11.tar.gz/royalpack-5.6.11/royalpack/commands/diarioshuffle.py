from typing import *
from royalnet.commands import *
from royalnet.utils import *
from ..tables import Diario
from sqlalchemy import func


class DiarioshuffleCommand(Command):
    name: str = "diarioshuffle"

    description: str = "Cita una riga casuale del diario."

    aliases = ["dis", "dishuffle", "dish"]

    syntax = ""

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        DiarioT = self.alchemy.get(Diario)
        entry: List[Diario] = await asyncify(
            data.session
                .query(DiarioT)
                .order_by(func.random())
                .limit(1)
                .one_or_none
        )
        if entry is None:
            raise CommandError("Nessuna riga del diario trovata.")
        await data.reply(f"ℹ️ {entry}")
