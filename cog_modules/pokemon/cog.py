import discord
from discord.ext import commands
import asyncio 
import os 
import aiopoke 
import json
import random


class Pokemon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="test")
    async def testing(self, ctx: commands.Context): 
        await ctx.send("hi!")

    @commands.command(name="ability")
    async def getAbility(self, ctx: commands.Context):
        client = aiopoke.AiopokeClient()
        ability = await client.get_ability(1)
        generation = await ability.generation.fetch()

        print(ability, generation)
        await client.close()

    @commands.command(name="type")
    async def getType(self, ctx: commands.Context, arg1):
        client = aiopoke.AiopokeClient()
        type = await client.get_type(arg1.lower())
        await client.close()
        ddf = ''
        if len(type.damage_relations.double_damage_from) == 0:
            ddf += "None"
        else:
            for i in range(len(type.damage_relations.double_damage_from)):
                if len(type.damage_relations.double_damage_from) == 1:
                    ddf += type.damage_relations.double_damage_from[i].name.capitalize()
                elif i < (len(type.damage_relations.double_damage_from)-1):
                    ddf += type.damage_relations.double_damage_from[i].name.capitalize() + ", "
                else:
                    ddf += "and " + type.damage_relations.double_damage_from[i].name.capitalize()
        embed = discord.Embed(title=f"Information about the {arg1.capitalize()} type", description=f" ")
        embed.add_field(name="Double Damage From", value=ddf, inline = False)
        ddt = ''
        if len(type.damage_relations.double_damage_to) == 0:
                ddt += "None"
        else:
            for i in range(len(type.damage_relations.double_damage_to)):
                if len(type.damage_relations.double_damage_to) == 1:
                    ddt += type.damage_relations.double_damage_to[i].name.capitalize()
                elif i  < (len(type.damage_relations.double_damage_to)-1):
                    ddt += type.damage_relations.double_damage_to[i].name.capitalize() + ", "
                else:
                    ddt += "and " + type.damage_relations.double_damage_to[i].name.capitalize()
        embed.add_field(name="Double Damage To", value=ddt, inline = False)
        hdf = ''
        if len(type.damage_relations.half_damage_from) == 0:
            hdf += "None"
        else:
            for i in range(len(type.damage_relations.half_damage_from)):
                if len(type.damage_relations.half_damage_from) == 1:
                    hdf += type.damage_relations.half_damage_from[i].name.capitalize()
                elif i < (len(type.damage_relations.half_damage_from)-1):
                    hdf += type.damage_relations.half_damage_from[i].name.capitalize() + ", "
                else:
                    hdf += "and " + type.damage_relations.half_damage_from[i].name.capitalize()
        embed.add_field(name="Half Damage From", value=hdf, inline = False)
        hdt = ''
        if len(type.damage_relations.half_damage_to) == 0:
                hdt += "None"
        else:
            for i in range(len(type.damage_relations.half_damage_to)):
                if len(type.damage_relations.half_damage_to) == 1:
                    hdt += type.damage_relations.half_damage_to[i].name.capitalize()
                elif i < (len(type.damage_relations.half_damage_to)-1):
                    hdt += type.damage_relations.half_damage_to[i].name.capitalize() + ", "
                else:
                    hdt += "and " + type.damage_relations.half_damage_to[i].name.capitalize()
        embed.add_field(name="Half Damage To", value=hdt, inline = False)
        ndf = ''
        if len(type.damage_relations.no_damage_from) == 0:
                ndf += "None"
        else:
            for i in range(len(type.damage_relations.no_damage_from)):
                if len(type.damage_relations.no_damage_from) == 1:
                    ndf += type.damage_relations.no_damage_from[i].name.capitalize()
                elif i < (len(type.damage_relations.no_damage_from)-1):
                    ndf += type.damage_relations.no_damage_from[i].name.capitalize() + ", "
                else:
                    ndf += "and " + type.damage_relations.no_damage_from[i].name.capitalize()
        embed.add_field(name="No Damage From", value=ndf, inline = False)
        ndt = ''
        if (len(type.damage_relations.no_damage_to)) == 0:
            ndt += "None"
        else:
            for i in range(len(type.damage_relations.no_damage_to)):
                if (len(type.damage_relations.no_damage_to))== 1:
                    ndt += type.damage_relations.no_damage_to[i].name.capitalize()
                elif i < (len(type.damage_relations.no_damage_to)-1):
                    ndt += type.damage_relations.no_damage_to[i].name.capitalize() + ", "
                else:
                    ndt += "and " + type.damage_relations.no_damage_to[i].name.capitalize()
        embed.add_field(name="No Damage To", value=ndt, inline = False)
        await ctx.send(embed=embed)

    # @commands.command(name="pokemon")
    # @commands.cooldown(1, 15, commands.BucketType.user)
    # async def getPokemon(self, ctx: commands.Context, *args):
    #     mon = ''
    #     for i in range(len(args)):
    #         if i == 0:
    #             mon += args[i].lower()
    #         else:
    #             mon += "-" + args[i].lower()
    #     print(mon)
    #     mon = mon.replace(".", "")
    #     client = aiopoke.AiopokeClient()
    #     pokemon = await client.get_pokemon_species(mon)
    #     await client.close()
    #     print(pokemon)

    #     en_flag = False
    #     while not en_flag:
    #         entry = random.choice(pokemon.flavor_text_entries)
    #         if entry.language.name == "en":
    #             en_flag = True 
    #     print(entry)

    #     # file = discord.File(f"./official-artwork/{pokemon.id}.png", filename=f"{pokemon.id}.png")
    #     embed = discord.Embed(title=f"Information about {pokemon.name.replace('-', ' ').title()}", description=f" ")
    #     # embed.set_image(url=f"attachment://{pokemon.id}.png")
    #     # embed.set_thumbnail(url=f"https://github.com/PokeAPI/sprites/tree/master/sprites/pokemon/other/official-artwork/{pokemon.id}.png")
    #     embed.add_field(name="ID", value=pokemon.id)
    #     embed.add_field(name=f"Pokémon {entry.version.name.replace('-', ' ').title()} flavor text", value=entry.flavor_text.replace("\n", " ").replace("\x0c", " "), inline=False)
    #     embed.set_footer(
    #         text=f"{ctx.author.name}",
    #         icon_url=ctx.author.display_avatar.url,
    #     )
    #     await ctx.send(embed=embed)

    @commands.command(name="pokemon")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def getPokemon(self, ctx: commands.Context, *args):
        mon = ''
        for i in range(len(args)):
            if i == 0:
                mon += args[i].lower()
            else:
                mon += "-" + args[i].lower()
        print(mon)
        mon = mon.replace(".", "")
        client = aiopoke.AiopokeClient()
        pokemon = await client.get_pokemon_species(mon)
        await client.close()
        print("close client")
        # print(pokemon)

        en_flag = False
        while not en_flag:
            entry = random.choice(pokemon.flavor_text_entries)
            if entry.language.name == "en":
                en_flag = True 
        print("flavortext")

        if pokemon.evolves_from_species != None:
            evolved = pokemon.evolves_from_species.name.title()
        else:
            evolved = "None"

        print("evolution")

        embed = discord.Embed(title=f"Information about {pokemon.name.replace('-', ' ').title()}", description=f" ")
        # file = discord.File(f"official-artwork/{pokemon.id}.png", filename="image.png")
        # embed.set_thumbnail(url="attachment://image.png")
        # print("image")
        embed.add_field(name="ID", value=pokemon.id)
        print(pokemon.id)
        print(pokemon.habitat)
        if pokemon.habitat != None:
            embed.add_field(name="Habitat? ", value=pokemon.habitat.name.title())
            print(pokemon.habitat.name.title())
        else:
            embed.add_field(name="Habitat?", value="N/A")
        print("habitat")
        embed.add_field(name="Baby Pokémon?", value=pokemon.is_baby)
        print("--")
        # print("baby " + pokemon.is_baby)
        embed.add_field(name="Evolves from", value=evolved)
        print("evolve " + evolved)
        embed.add_field(name="Legendary?", value=pokemon.is_legendary)
        # print("legendary " + pokemon.is_legendary)
        embed.add_field(name="Mythical?", value=pokemon.is_mythical)
        # print("mythical " + pokemon.is_mythical)
        embed.add_field(name=f"Pokémon {entry.version.name.replace('-', ' ').title()} flavor text", value=entry.flavor_text.replace("\n", " ").replace("\x0c", " "), inline=False)
        print("flavortext2 " + entry.flavor_text.replace("\n", " ").replace("\x0c", " "))
        embed.set_footer(
                text=f"{ctx.author.name}",
                icon_url=ctx.author.display_avatar.url,
            )
        print("finalize embed")
        await ctx.send(embed=embed)
        await ctx.send(file = discord.File(f"./official-artwork/{pokemon.id}.png", filename="image.png"))
        print("send embed")

    @getPokemon.error
    async def getPokemon_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You can only get info on 1 Pokémon every 15 seconds. Try again in {round(error.retry_after, 2)} seconds."
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(Pokemon(bot))