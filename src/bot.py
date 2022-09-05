from nextcord.ext import commands
from nextcord import Intents
from nextcord import Embed

from googletrans import Translator
import language_tool_python


class Meta:
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


class Zeta(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         command_prefix=Meta.COMMAND_PREFIX,
                         intents=Meta.get_intents(message_content=True),
                         **kwargs)

        self.add_commands()

    async def on_ready(self):
        print(f'[INFO] Client {self.user} is ready!')

    def add_commands(self):
        @self.command(name='translate', aliases=['يترجم'], pass_context=True)
        @Meta.sentencecriterion
        async def translate(ctx, msg):
            async def show_help_card():
                TITLE = '!translate | يترجم!'
                DESCRIPTION = (
                    '**__How to use?__**\n'
                    '!translate *Hello, Mr. Zeta!*\n'
                    '!يترجم *مرحبا سيد زيتا!*'
                )
                COLOR = 0xFAAD14

                embed = Embed(title=TITLE,
                              description=DESCRIPTION,
                              color=COLOR)
                await ctx.reply(embed=embed)

            ARABIC = 'ar'
            ENGLISH = 'en'

            if not msg:
                if ctx.message.reference is not None:
                    msg = ctx.message.reference.resolved.content
                else:
                    await show_help_card()
                    return

            translator = Translator(service_urls=['translate.google.com'])
            meta_info = translator.detect(msg)
            if meta_info.lang == ENGLISH:
                translation = translator.translate(msg, dest=ARABIC)
                await ctx.reply(translation.text)
            elif meta_info.lang == ARABIC:
                translation = translator.translate(msg, dest=ENGLISH)
                await ctx.reply(translation.text)
            else:
                await ctx.reply(f'Failed to translate: {msg}')

        @self.command(name='grammar', pass_context=True)
        @Meta.sentencecriterion
        async def grammar(ctx, msg):
            async def show_help_card():
                TITLE = '!grammar'
                DESCRIPTION = (
                    '**__How to use?__**\n'
                    '!grammar *These is my book.*\n'
                )
                COLOR = 0xD3ADF7

                embed = Embed(title=TITLE,
                              description=DESCRIPTION,
                              color=COLOR)
                await ctx.reply(embed=embed)

            LANG = 'en-US'

            if not msg:
                if ctx.message.reference is not None:
                    msg = ctx.message.reference.resolved.content
                else:
                    await show_help_card()
                    return

            with language_tool_python.LanguageTool(LANG) as lang_tool:
                possible_matches = lang_tool.check(msg)
                corrected_text = language_tool_python.utils.correct(msg, possible_matches)
                await ctx.reply(corrected_text)
