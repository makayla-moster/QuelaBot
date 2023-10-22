import discord
from discord.ext import commands
import asyncio 
import os 
import aiopoke 
import json


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
        type = await client.get_type(arg1)
        await client.close()
        # type = await client.get_type(grass)
        print(type.name)
        print(type.damage_relations)
        # print(type.damage_relations.double_damage_from)
        ddf = ''
        for i in range(len(type.damage_relations.double_damage_from)):
            # print(type.damage_relations.double_damage_from[i].name)
            ddf += type.damage_relations.double_damage_from[i].name + ", "
        embed = discord.Embed(title=f"Information about the {arg1.capitalize()} type", description=f" ")
        embed.add_field(name="Double Damage From", value=ddf, inline = False)
        ddt = ''
        for i in range(len(type.damage_relations.double_damage_to)):
            # print(type.damage_relations.double_damage_to[i].name)
            ddt += type.damage_relations.double_damage_to[i].name + ", "
        embed.add_field(name="Double Damage To", value=ddt, inline = False)
        hdf = ''
        for i in range(len(type.damage_relations.half_damage_from)):
            # print(type.damage_relations.half_damage_from[i].name)
            hdf += type.damage_relations.half_damage_from[i].name + ", "
        embed.add_field(name="Half Damage From", value=hdf, inline = False)
        hdt = ''
        for i in range(len(type.damage_relations.half_damage_to)):
            # print(type.damage_relations.half_damage_to[i].name)
            hdt += type.damage_relations.half_damage_to[i].name + ", "
        embed.add_field(name="Half Damage To", value=hdt, inline = False)
        ndf = ''
        for i in range(len(type.damage_relations.no_damage_from)):
            # print(type.damage_relations.no_damage_from[i].name)
            ndf += type.damage_relations.no_damage_from[i].name + ", "
        embed.add_field(name="No Damage From", value=ndf, inline = False)
        ndt = ''
        for i in range(len(type.damage_relations.no_damage_to)):
            # print(type.damage_relations.no_damage_to[i].name)
            ndt += type.damage_relations.no_damage_to[i].name + ", "
        embed.add_field(name="No Damage To", value=ndt, inline = False)
        await ctx.send(embed=embed)



async def setup(bot: commands.Bot):
    await bot.add_cog(Pokemon(bot))