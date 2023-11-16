import json
import logging
import os
import shlex
from http import HTTPStatus

import dotenv
from discord import Intents
from discord.ext import commands

from dialogue import DialogueType
from enchantus_api_client import EnchantusAPIClient

logging.basicConfig(level=logging.DEBUG)

dotenv.load_dotenv('.env')


class DiscordBot:
    enchantus_client = None
    npcs = {}
    players = {}

    def __init__(self,
                 discord_auth_token):
        intents = Intents.default()
        intents.members = True
        intents.message_content = True
        self.enchantus_client = EnchantusAPIClient(api_token=os.environ['ENCHANTUS_API_TOKEN'])
        self.token = discord_auth_token
        self.bot = commands.Bot(command_prefix='/',
                                intents=intents,
                                description='A bot that generates images from text prompts using the Stable Diffusion '
                                            'model.',
                                help_command=None)

        @self.bot.command(name='createnpc', help='Creates an NPC with the provided properties')
        async def create_npc(ctx, *, message):
            message = message.strip()

            # First, use shlex.split to handle the name parameter
            command_args = shlex.split(message)

            name = None
            for arg in command_args:
                if arg.startswith('name='):
                    name = arg.split('=', 1)[1]
                    await ctx.send(f'Name: {name}')
                    break

            # Validate the name
            if name is None:
                await ctx.send('You must provide a name for the NPC')
                return

            # Sanitize the name and lower case it
            name = name.lower().replace('"', '')

            if name in self.npcs:
                await ctx.send(f'An NPC with the name {name} already exists')
                return

            # Extract the details part directly from the message
            # Find the start of the JSON string and extract it to the end of the message
            details_start = message.find('details=')
            if details_start == -1:
                await ctx.send('You must provide details for the NPC')
                return

            details_json_str = message[details_start + len('details='):].strip()
            await ctx.send(f'Details: {details_json_str}')

            # Convert the details string to a dictionary
            try:
                details = json.loads(details_json_str)
            except json.JSONDecodeError:
                await ctx.send('Invalid JSON format for NPC details')
                await ctx.send(details_json_str)
                return

            # Create the NPC
            entity, resp = self.enchantus_client.create_entity(name=name, details=details)

            if resp.status_code != HTTPStatus.CREATED:
                await ctx.send(f'Error creating NPC: {resp.status_code}')
                return

            self.npcs[name] = {'entity': entity, 'name': name, 'dialogue': []}

            await ctx.send(f'Created NPC {entity.name} with ID {entity.id}')

        # Talk command
        @self.bot.command(name='talk', help='Talk to an NPC')
        async def talk(ctx, *, message):
            message = message.strip()

            # Manually parsing the command
            if not message.startswith('npc='):
                await ctx.send("Please provide the NPC's name using the format: /talk npc=<name> <dialogue>")
                return

            try:
                npc_name_end = message.index(' ')
                npc_name = message[4:npc_name_end]
                content = message[npc_name_end + 1:]
                # await ctx.send(f'NPC Name: {npc_name}')
                # await ctx.send(f'Dialogue Content: {content}')
            except ValueError:
                await ctx.send("Error in parsing the command. Please check your format.")
                return

            # Sanitize the name and lower case it
            npc_name = npc_name.lower().replace('"', '')

            if npc_name not in self.npcs:
                await ctx.send(f'An NPC with the name {npc_name} does not exist')
                return

            if content is None or len(content) == 0:
                await ctx.send('You must provide dialogue for the NPC')
                return

            if self.players.get(ctx.author.id) is None:
                # Create the player
                player_entity, resp = self.enchantus_client.create_entity(name=str(ctx.author.id), details={})

                if resp.status_code != HTTPStatus.CREATED:
                    await ctx.send(f'Error creating player: {resp.status_code}')
                    return

                self.players[ctx.author.id] = player_entity

            # Get the NPC
            npc = self.npcs[npc_name]

            current_dialogues = npc['dialogue']
            latest_dialogue_id = current_dialogues[-1].id if len(current_dialogues) > 0 else None

            # await ctx.send(f'Latest dialogue ID: {latest_dialogue_id}')
            # await ctx.send(f'Adding dialogue "{content}" to NPC "{npc["name"]}"')

            # Add the player dialogue
            added_dialogue, resp = self.enchantus_client.add_dialogue(dialogue_type=DialogueType.PLAYER,
                                                                      content=content,
                                                                      actor_id=self.players[ctx.author.id].id,
                                                                      parent_id=latest_dialogue_id)

            if resp.status_code != HTTPStatus.CREATED:
                await ctx.send(f'Error creating dialogue: {resp.status_code}')
                return

            self.npcs[npc_name]['dialogue'].append(added_dialogue)

            # await ctx.send(f'Added dialogue {added_dialogue.content} to NPC {npc["name"]}')
            # await ctx.send('Generating NPC response with actor ID: ' + npc['entity'].id
            #               + ' and parent ID: ' + added_dialogue.id)

            async with ctx.typing():
                # Generate the NPC dialogue
                dialogue, resp = self.enchantus_client.generate_dialogue(actor_id=npc['entity'].id,
                                                                         parent_id=added_dialogue.id)

            if resp.status_code != HTTPStatus.CREATED:
                await ctx.send(f'Error creating dialogue: {resp.status_code}')
                return

            self.npcs[npc_name]['dialogue'].append(dialogue)

            await ctx.send(f'<{npc["name"]}> {dialogue.content}')

    def run(self):
        self.bot.run(self.token)


if __name__ == '__main__':
    bot = DiscordBot(discord_auth_token=os.environ['DISCORD_BOT_TOKEN'])
    bot.run()
