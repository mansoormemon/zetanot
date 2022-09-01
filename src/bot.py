from nextcord.ext import commands
from nextcord import Intents
from nextcord import Embed

from googletrans import Translator


class Zeta(commands.Bot):
    COMMAND_PREFIX = '!'

    @staticmethod
    def get_intents(presences=False, members=False, message_content=False):
        intents = Intents.default()
        intents.presences = presences
        intents.members = members
        intents.message_content = message_content
        return intents

    @staticmethod
    def sentencecriterion(func):
        async def impl(ctx, *args):
            await func(ctx, ' '.join(args).strip())
        return impl

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         command_prefix=Zeta.COMMAND_PREFIX,
                         intents=Zeta.get_intents(message_content=True),
                         **kwargs)

        self.add_commands()

    async def on_ready(self):
        print(f'[INFO] Client {self.user} is ready!')

    def add_commands(self):
        @self.command(aliases=['translate', 'يترجم'], pass_context=True)
        @Zeta.sentencecriterion
        async def translate(ctx, msg):
            ARABIC = 'ar'
            ENGLISH = 'en'

            if not msg:
                embed = Embed(title='!translate | يترجم!',
                            description='**__How to use?__**\n'
                                        '!translate *Hello, Mr. Zeta!*\n'
                                        '!يترجم *مرحبا سيد زيتا!*',
                            color=0xFAAD14)
                await ctx.reply(embed=embed)
                return

            translator = Translator(service_urls=['translate.google.com'])
            meta = translator.detect(msg)
            if meta.lang == ENGLISH:
                translation = translator.translate(msg, dest=ARABIC)
                await ctx.reply(translation.text)
            elif meta.lang == ARABIC:
                translation = translator.translate(msg, dest=ENGLISH)
                await ctx.reply(translation.text)
            else:
                await ctx.reply(f'Failed to translate: {msg}')
