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


    @commands.command(name="dex", aliases=["pokemon", "mon"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def getPokemonSpecies(self, ctx: commands.Context, *args):
        mon = ''
        for i in range(len(args)):
            if i == 0:
                mon += args[i].lower()
            else:
                mon += "-" + args[i].lower()
        mon = mon.replace(".", "")
        client = aiopoke.AiopokeClient()
        pokemon = await client.get_pokemon_species(mon)
        # print(pokemon.evolution_chain)
        pokemonType = await client.get_pokemon(mon)
        # evochain = await client.get_evolution_chain(pokemon.evolution_chain.id)
        # print(evochain.chain)
        # print(evochain.chain.evolves_to[0].species.name.title())

        damageFrom = {}
        damageTo = {}
        for i in range(len(pokemonType.types)):
            type = await client.get_type(pokemonType.types[i].type.name.lower())
            for i in range(len(type.damage_relations.double_damage_from)):
                if type.damage_relations.double_damage_from[i].name in damageFrom:
                    damageFrom[type.damage_relations.double_damage_from[i].name] *= 2
                else:
                    damageFrom[type.damage_relations.double_damage_from[i].name] = 2
                
            for i in range(len(type.damage_relations.half_damage_from)):
                if type.damage_relations.half_damage_from[i].name in damageFrom:
                    damageFrom[type.damage_relations.half_damage_from[i].name] *= 0.5
                else:
                    damageFrom[type.damage_relations.half_damage_from[i].name] = 0.5

            for i in range(len(type.damage_relations.no_damage_from)):
                if type.damage_relations.no_damage_from[i].name in damageFrom:
                    damageFrom[type.damage_relations.no_damage_from[i].name] *= 0
                else:
                    damageFrom[type.damage_relations.no_damage_from[i].name] = 0

            for i in range(len(type.damage_relations.double_damage_to)):
                if type.damage_relations.double_damage_to[i].name in damageTo:
                    damageTo[type.damage_relations.double_damage_to[i].name] *= 2
                else:
                    damageTo[type.damage_relations.double_damage_to[i].name] = 2
                
            for i in range(len(type.damage_relations.half_damage_to)):
                if type.damage_relations.half_damage_to[i].name in damageTo:
                    damageTo[type.damage_relations.half_damage_to[i].name] *= 0.5
                else:
                    damageTo[type.damage_relations.half_damage_to[i].name] = 0.5

            for i in range(len(type.damage_relations.no_damage_to)):
                if type.damage_relations.no_damage_to[i].name in damageTo:
                    damageTo[type.damage_relations.no_damage_to[i].name] *= 0
                else:
                    damageTo[type.damage_relations.no_damage_to[i].name] = 0

        # print(damageFrom)
        # print(damageTo)
        generation = pokemon.generation.id
        generationInfo = await client.get_generation(generation)

        await client.close()

        
        region = generationInfo.main_region.name.title() + f", Gen. {generationInfo.main_region.id}"
        # print(region)

        weaknesses = ''
        for key in damageFrom:
            if damageFrom[key] >= 2:
                if weaknesses == '': 
                    weaknesses += key.title()
                else:
                    weaknesses += ", " + key.title()

        resistant = ''
        for key in damageFrom:
            if (damageFrom[key] == 0.5) or (damageFrom[key] == 0.25):
                if resistant == '':
                    resistant += key.title()
                else:
                    resistant += ", " + key.title()
        # print(weaknesses)
        # print(resistant)

        pokeHeight = int(pokemonType.height) * 0.33
        pokeWeight = int(pokemonType.weight) * 0.22

        # print(pokeHeight)
        # print(pokeWeight)


        en_flag = False
        while not en_flag:
            entry = random.choice(pokemon.flavor_text_entries)
            if entry.language.name == "en":
                en_flag = True 

        specialty = ''
        if pokemon.is_baby:
            if specialty == '':
                specialty += "Baby"
            else:
                specialty += ", Baby"
        if pokemon.is_legendary:
            if specialty == '':
                specialty += "Legendary"
            else:
                specialty += ", Legendary"
        if pokemon.is_mythical:
            if specialty == '':
                specialty += "Mythical"
            else:
                specialty += ", Mythical"
        if specialty == '':
            specialty = 'None'

        if pokemon.evolves_from_species != None:
            evolved = pokemon.evolves_from_species.name.title()
        else:
            evolved = "None"

        pokeTyping = ''
        for i in range(len(pokemonType.types)):
            if i == 0:
                pokeTyping += pokemonType.types[i].type.name.title()
            else:
                pokeTyping += ", " + pokemonType.types[i].type.name.title()

        embed = discord.Embed(title=f"Information about {pokemon.name.replace('-', ' ').title()}", description=f" ")
        embed.set_thumbnail(url=f"https://raw.githubusercontent.com/makayla-moster/QuelaBot/main/cog_modules/pokemon/official-artwork/{pokemon.id}.png")
        
        embed.add_field(name="ID", value=pokemon.id)
        embed.add_field(name="Type(s)", value=pokeTyping)
        embed.add_field(name="Weak against", value=weaknesses)
        embed.add_field(name='Region', value=region)
        if pokemon.habitat != None:
            embed.add_field(name="Habitat", value=pokemon.habitat.name.replace('-', ' ').title())
        else:
            embed.add_field(name="Habitat", value="N/A")
        embed.add_field(name="Strong against", value=resistant)
        embed.add_field(name="Size", value=f"{round(pokeHeight, 2)} ft., {round(pokeWeight, 2)} lbs.")
        embed.add_field(name="Evolves from", value=evolved)
        embed.add_field(name="Other Attributes", value=specialty)
        embed.add_field(name=f"Pokémon {entry.version.name.replace('-', ' ').title()} flavor text", value=entry.flavor_text.replace("\n", " ").replace("\x0c", " "), inline=False)
        embed.set_footer(
                text=f"{ctx.author.name}",
                icon_url=ctx.author.display_avatar.url,
            )
        await ctx.send(embed=embed)

    @getPokemonSpecies.error
    async def getPokemonSpecies_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You can only get info on 1 Pokémon every 15 seconds. Try again in {round(error.retry_after, 2)} seconds."
            )

    # getPokeInfo.start()

async def setup(bot: commands.Bot):
    await bot.add_cog(Pokemon(bot))
