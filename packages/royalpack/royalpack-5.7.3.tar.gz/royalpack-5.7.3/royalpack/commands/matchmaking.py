import datetime
import re
import dateparser
import typing
import asyncio
from telegram import Bot as PTBBot
from telegram import Message as PTBMessage
from telegram import InlineKeyboardMarkup as InKM
from telegram import InlineKeyboardButton as InKB
from telegram.error import BadRequest, Unauthorized
from royalnet.commands import *
from royalnet.serf.telegram import TelegramSerf as TelegramBot
from royalnet.serf.telegram import escape as telegram_escape
from royalnet.utils import asyncify, sleep_until, sentry_async_wrap
from royalnet.backpack.tables import User
from ..tables import MMEvent, MMResponse
from ..types import MMChoice, MMInterfaceDataTelegram


class MatchmakingCommand(Command):
    name: str = "matchmaking"

    description: str = "Cerca persone per una partita a qualcosa!"

    syntax: str = "[ {ora} ] {nome}\n[descrizione]"

    aliases = ["mm", "lfg"]

    tables = {MMEvent, MMResponse}

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        # Find all relevant MMEvents and run them
        session = self.alchemy.Session()
        mmevents = (
            session
            .query(self.alchemy.get(MMEvent))
            .filter(self.alchemy.get(MMEvent).interface == self.interface.name,
                    self.alchemy.get(MMEvent).datetime > datetime.datetime.now())
            .all()
        )
        for mmevent in mmevents:
            self.interface.loop.create_task(self._run_mmevent(mmevent.mmid))

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        # Create a new MMEvent and run it
        if self.interface.name != "telegram":
            raise UnsupportedError(f"{self.interface.prefix}matchmaking funziona solo su Telegram. Per ora.")
        author = await data.get_author(error_if_none=True)

        try:
            timestring, title, description = args.match(r"\[\s*([^]]+)\s*]\s*([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        except InvalidInputError:
            timestring, title, description = args.match(r"\s*(.+?)\s*\n\s*([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        try:
            dt: typing.Optional[datetime.datetime] = dateparser.parse(timestring, settings={
                "PREFER_DATES_FROM": "future"
            })
        except OverflowError:
            dt = None
        if dt is None:
            await data.reply("⚠️ La data che hai specificato non è valida.")
            return
        if dt <= datetime.datetime.now():
            await data.reply("⚠️ La data che hai specificato è nel passato.")
            return
        mmevent: MMEvent = self.alchemy.get(MMEvent)(creator=author,
                                                     datetime=dt,
                                                     title=title,
                                                     description=description,
                                                     interface=self.interface.name)
        data.session.add(mmevent)
        await data.session_commit()
        self.loop.create_task(self._run_mmevent(mmevent.mmid))
        await data.reply(f"✅ Matchmaking creato!")

    _mmchoice_values = {
        MMChoice.YES: 4,
        MMChoice.LATE_SHORT: 3,
        MMChoice.LATE_MEDIUM: 2,
        MMChoice.LATE_LONG: 1,
        MMChoice.MAYBE: 0,
        MMChoice.NO: -1
    }

    def _gen_mm_message(self, mmevent: MMEvent) -> str:
        text = f"🌐 [{mmevent.datetime.strftime('%Y-%m-%d %H:%M')}] [b]{mmevent.title}[/b]\n"
        if mmevent.description:
            text += f"{mmevent.description}\n"
        text += "\n"
        for response in sorted(mmevent.responses, key=lambda r: -self._mmchoice_values[r.choice]):
            response: MMResponse
            text += f"{response.choice.value} {response.user}\n"
        return text

    @staticmethod
    def _gen_telegram_keyboard(mmevent: MMEvent):
        if mmevent.datetime <= datetime.datetime.now():
            return None
        return InKM([
            [
                InKB(f"{MMChoice.YES.value} Ci sarò!",
                     callback_data=f"mm{mmevent.mmid}_YES"),
                InKB(f"{MMChoice.MAYBE.value} Forse...",
                     callback_data=f"mm{mmevent.mmid}_MAYBE"),
            ],
            [
                InKB(f"{MMChoice.LATE_SHORT.value} 10 min",
                     callback_data=f"mm{mmevent.mmid}_LATE_SHORT"),
                InKB(f"{MMChoice.LATE_MEDIUM.value} 30 min",
                     callback_data=f"mm{mmevent.mmid}_LATE_MEDIUM"),
                InKB(f"{MMChoice.LATE_LONG.value} 60 min",
                     callback_data=f"mm{mmevent.mmid}_LATE_LONG"),
            ],
            [
                InKB(f"{MMChoice.NO.value} Non mi interessa.",
                     callback_data=f"mm{mmevent.mmid}_NO"),
            ]
        ])

    async def _update_telegram_mm_message(self, client: PTBBot, mmevent: MMEvent):
        try:
            await self.interface.serf.api_call(client.edit_message_text,
                                               chat_id=self.config["Matchmaking"]["mm_chat_id"],
                                               text=telegram_escape(self._gen_mm_message(mmevent)),
                                               message_id=mmevent.interface_data.message_id,
                                               parse_mode="HTML",
                                               disable_web_page_preview=True,
                                               reply_markup=self._gen_telegram_keyboard(mmevent))
        except BadRequest:
            pass

    def _gen_mm_telegram_callback(self, client: PTBBot, mmid: int, choice: MMChoice):
        async def callback(data: CommandData):
            author = await data.get_author(error_if_none=True)
            # Find the MMEvent with the current session
            mmevent: MMEvent = await asyncify(data.session.query(self.alchemy.get(MMEvent)).get, mmid)
            mmresponse: MMResponse = await asyncify(
                data.session.query(self.alchemy.get(MMResponse)).filter_by(user=author, mmevent=mmevent).one_or_none)
            if mmresponse is None:
                mmresponse = self.alchemy.get(MMResponse)(user=author, mmevent=mmevent, choice=choice)
                data.session.add(mmresponse)
            else:
                mmresponse.choice = choice
            await data.session_commit()
            await self._update_telegram_mm_message(client, mmevent)
            await data.reply(f"{choice.value} Messaggio ricevuto!")

        return callback

    @staticmethod
    def _gen_event_start_message(mmevent: MMEvent):
        text = f"🚩 L'evento [b]{mmevent.title}[/b] è iniziato!\n\n"
        for response in mmevent.responses:
            response: MMResponse
            text += f"{response.choice.value} {response.user}\n"
        return text

    @staticmethod
    def _gen_unauth_message(user: User):
        return f"⚠️ Non sono autorizzato a mandare messaggi a [b]{user.username}[/b]!\n" \
               f"{user.telegram.mention()}, apri una chat privata con me e mandami un messaggio!"

    @sentry_async_wrap()
    async def _run_mmevent(self, mmid: int):
        """Run a MMEvent."""
        # Open a new Alchemy Session
        session = self.alchemy.Session()
        # Find the MMEvent with the current session
        mmevent: MMEvent = await asyncify(session.query(self.alchemy.get(MMEvent)).get, mmid)
        if mmevent is None:
            raise ValueError("Invalid mmid.")
        # Ensure the MMEvent hasn't already started
        if mmevent.datetime <= datetime.datetime.now():
            raise ValueError("MMEvent has already started.")
        # Ensure the MMEvent interface matches the current one
        if mmevent.interface != self.interface.name:
            raise ValueError("Invalid interface.")
        # If the matchmaking message hasn't been sent yet, do so now
        if mmevent.interface_data is None:
            if self.interface.name == "telegram":
                bot: TelegramBot = self.interface.serf
                client: PTBBot = bot.client
                # Send the keyboard
                message: PTBMessage = await self.interface.serf.api_call(
                    client.send_message,
                    chat_id=self.config["Matchmaking"]["mm_chat_id"],
                    text=telegram_escape(
                        self._gen_mm_message(mmevent)),
                    parse_mode="HTML",
                    disable_webpage_preview=True,
                    reply_markup=self._gen_telegram_keyboard(mmevent)
                )
                # Store message data in the interface data object
                mmevent.interface_data = MMInterfaceDataTelegram(chat_id=self.config["Matchmaking"]["mm_chat_id"],
                                                                 message_id=message.message_id)
                await asyncify(session.commit)
            else:
                raise UnsupportedError()
        # Register handlers for the keyboard events
        if self.interface.name == "telegram":
            bot: TelegramBot = self.interface.serf
            client: PTBBot = bot.client
            bot.register_keyboard_key(f"mm{mmevent.mmid}_YES", key=KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.YES.value}",
                text="Ci sarò!",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.YES)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_LATE_SHORT", key=KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.LATE_SHORT.value}",
                text="10 min",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.LATE_SHORT)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_LATE_MEDIUM", key=KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.LATE_MEDIUM.value}",
                text="30 min",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.LATE_MEDIUM)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_LATE_LONG", key=KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.LATE_LONG.value}",
                text="60 min",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.LATE_LONG)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_MAYBE", key=KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.MAYBE.value}",
                text="Forse...",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.MAYBE)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_NO", key=KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.NO.value}",
                text="Non mi interessa.",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.NO)
            ))
        else:
            raise UnsupportedError()
        # Sleep until the time of the event
        await sleep_until(mmevent.datetime)
        # Notify the positive answers of the event start
        if self.interface.name == "telegram":
            bot: TelegramBot = self.interface.serf
            client: PTBBot = bot.client
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_YES")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_MAYBE")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_LATE_SHORT")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_LATE_MEDIUM")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_LATE_LONG")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_NO")
            for response in mmevent.responses:
                if response.choice == MMChoice.NO:
                    return
                try:
                    await self.interface.serf.api_call(client.send_message,
                                                       chat_id=response.user.telegram[0].tg_id,
                                                       text=telegram_escape(self._gen_event_start_message(mmevent)),
                                                       parse_mode="HTML",
                                                       disable_webpage_preview=True)
                except Unauthorized:
                    await self.interface.serf.api_call(client.send_message,
                                                       chat_id=self.config["Telegram"]["main_group_id"],
                                                       text=telegram_escape(self._gen_unauth_message(response.user)),
                                                       parse_mode="HTML",
                                                       disable_webpage_preview=True)
        else:
            raise UnsupportedError()
        # Delete the event message
        if self.interface.name == "telegram":
            await self.interface.serf.api_call(client.delete_message,
                                               chat_id=mmevent.interface_data.chat_id,
                                               message_id=mmevent.interface_data.message_id)
        # The end!
        await asyncify(session.close)
