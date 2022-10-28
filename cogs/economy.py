import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import BucketType
import random
import sqlite3
import asyncio
import time
import re

itemlist = ["<:mug:950689993867788338> mug:",
            "<:coffee_bean:951551479989301338> coffee bean:",
            ":milk: milk:",
            "<:pmilk:951741856264368128> premium milk",
            "<:sugar:951066869304029214> sugar:",
            ":spoon: spoon:",
            "<:gspoon:951731109312479243> golden spoon:",
            "<:teabag:957760498902900806> teabag",
            "<:hat:984285090190360657> mafia hat",
            "☕ common coffee",
            "<:rare_coffee:951551480215789658> rare coffee",
            "<:tea:959165836042588250> tea"]
itemID = ["mug",
          "bean",
          "milk",
          "pmilk",
          "sugar",
          "spoon",
          "gspoon",
          "teabag",
          "hat"]
itemvalue = [5000,  # mug
             1500,  # bean
             10000,  # milk
             50000,  # pmilk
             2500,  # sugar
             1000,  # spoon
             15000,  # gspoon
             5000,  # teabag
             500000]  # mafia hat
recipeList = ["ccoffee",
              "rcoffee",
              "tea"]
ccoffeeRecipeAmount = [1, 3, 1, 0, 2, 1, 0, 0]
rcoffeeRecipeAmount = [1, 7, 0, 1, 3, 0, 1, 0]
teaRecipeAmount = [1, 0, 1, 0, 3, 1, 0, 1]


def open_wallet(user: discord.Member):
    open_ingredients(user)
    open_recipes(user)
    open_mafia(user)

    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM wallets WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    else:
        sql = "INSERT INTO wallets(member_id, wallet, bank) VALUES(?,?,?)"
        val = (user.id, 500, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def open_ingredients(user: discord.Member):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    else:
        sql = "INSERT INTO ingredients(member_id, mug, bean, milk, pmilk, sugar, spoon, gspoon, teabag) VALUES(?,?,?,?,?,?,?,?,?)"
        val = (user.id, 0, 0, 0, 0, 0, 0, 0, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def open_recipes(user: discord.Member):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM recipes WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    else:
        sql = "INSERT INTO recipes(member_id, ccoffee, rcoffee, tea) VALUES(?,?,?,?)"
        val = (user.id, 0, 0, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def update_job(user: discord.Member, job):
    db = sqlite3.connect("kof_db.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * from wallets WHERE member_id = {user.id}")

    sql = f"UPDATE wallets SET job = ? WHERE member_id = ?"
    val = job, user.id

    cursor.execute(sql, val)
    db.commit()


def check_bal_greater_than(user: discord.Member, amount: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM wallets WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result[1] >= amount:
        return True
    return False


def add_bal(user: discord.Member, amount: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from wallets WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE wallets SET wallet = ? WHERE member_id = ?"
    val = (result[1] + amount, user.id)

    cursor.execute(sql, val)
    db.commit()


def remove_bal(user: discord.Member, amount: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from wallets WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE wallets SET wallet = ? WHERE member_id = ?"
    val = (result[1] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()


def add_item(user: discord.Member, amount: int, item: str, i: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM ingredients INNER JOIN recipes USING (member_id) WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if item in recipeList:
        sql = f"UPDATE recipes SET {item} = ? WHERE member_id = ?"
    else:
        sql = f"UPDATE ingredients SET {item} = ? WHERE member_id = ?"
    val = (int(result[i + 1]) + amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def remove_item(user: discord.Member, amount: int, item: str, i: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM ingredients INNER JOIN recipes USING (member_id) WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if item in recipeList:
        sql = f"UPDATE recipes SET {item} = ? WHERE member_id = ?"
    else:
        sql = f"UPDATE ingredients SET {item} = ? WHERE member_id = ?"
    val = (result[i + 1] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def add_crafted_item(user: discord.Member, amount: int, item: str, i: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM recipes WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE recipes SET {item} = ? WHERE member_id = ?"
    val = (int(result[i]) + amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def remove_crafted_item(user: discord.Member, amount: int, item: str, i: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM recipes WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE recipes SET {item} = ? WHERE member_id = ?"
    val = (int(result[i]) - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def open_mafia(user: discord.Member):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    else:
        sql = "INSERT INTO mafia(member_id, mafia_name, mafia_rank, heists) VALUES(?,?,?,?)"
        val = (user.id, 'none', 'none', 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def edit_mafia_name(user: discord.Member, title):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from mafia WHERE member_id = {user.id}")
    cursor.fetchone()

    sql = f"UPDATE mafia SET mafia_name = ? WHERE member_id = ?"
    val = (title, user.id)

    cursor.execute(sql, val)
    db.commit()


def edit_mafia_rank(user: discord.Member, target):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from mafia WHERE member_id = {user.id}")
    cursor.fetchone()

    sql = f"UPDATE mafia SET mafia_rank = ? WHERE member_id = ?"
    val = (target, user.id)

    cursor.execute(sql, val)
    db.commit()


def open_vault(mafname: str):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM mafias WHERE mafia_name = '{mafname}'")
    result = cursor.fetchone()

    if result:
        return
    else:
        sql = "INSERT INTO mafias(mafia_name, vault) VALUES(?,?)"
        val = (mafname, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def add_vault(mafname: str, amount: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from mafias WHERE mafia_name = '{mafname}'")
    result = cursor.fetchone()

    sql = f"UPDATE mafias SET vault = ? WHERE mafia_name = ?"
    val = (int(result[1]) + amount, mafname)

    cursor.execute(sql, val)
    db.commit()


def add_heist_completed(user: discord.Member, amount: int):
    db = sqlite3.connect('kof_db.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from mafia WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE mafia SET heists = ? WHERE member_id = ?"
    val = (int(result[3]) + amount, user.id)

    cursor.execute(sql, val)
    db.commit()


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="vote")
    async def vote(self, ctx):
        embed = discord.Embed(color=discord.Color.orange())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
        embed.add_field(name='Enjoying KoffeeBot?',
                        value="[Vote for me on top.gg!](https://top.gg/bot/901223515242508309/vote/)")
        await ctx.send(embed=embed)

    @commands.command(name="balance", aliases=['bal', 'wallet'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        open_wallet(member)

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {member.id}")
        result = cursor.fetchone()

        embed = discord.Embed(color=discord.Color.orange())
        embed.set_author(name=f"{member.name}'s Balance", icon=member.avatar)
        embed.add_field(name="Wallet:", value=f"<:KoffeeKoin:939562780363726868> {'{:,}'.format(result[1])}",
                        inline=False)
        embed.add_field(name="Bank:", value=f"<:KoffeeKoin:939562780363726868> {'{:,}'.format(result[2])}",
                        inline=False)
        embed.set_footer(text=f"Low on cash? Vote for me using 'kof vote' to earn a bit extra")
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)

    @commands.command(name='cheat')
    async def cheat(self, ctx, member: discord.Member, amount):
        open_wallet(member)
        user = ctx.author
        amount = int(amount)
        responses = ["no", "get lost!", "uhm...no", "You're not allowed to use this command :D"]

        if user.id == 465839240777826324:
            add_bal(member, amount)
            await ctx.send(f"Gave <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** to {member.name}")
        else:
            await ctx.send(random.choice(responses))

    @commands.command(name="beg")  # beg command
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        possibility = random.randint(1, 6)
        none = ["No money for you!",
                "Stop begging!",
                "Get lost!",
                "Away with you!",
                "Go get a job you useless begger!"]
        amount = random.randrange(1, 450)
        big_amount = random.randrange(800, 1100)

        if possibility == 3:
            return await ctx.send(
                random.choice(none)
            )
        if possibility == 6:
            add_bal(ctx.author, big_amount)
            return await ctx.send(f"Wow! You received a generous donation of <:KoffeeKoin:939562780363726868> *"
                                  f"*{'{:,}'.format(big_amount)}**")

        outcomes = [
            f"You got <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from a nice old lady",
            f"You received <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from a stranger",
            f"You begged your mom for <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}**"]

        add_bal(ctx.author, amount)
        await ctx.send(random.choice(outcomes))

    @commands.command(name="give")  # give money command
    @commands.cooldown(1, 10, BucketType.user)
    async def give(self, ctx, member: discord.Member, amount, item=None):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM ingredients INNER JOIN recipes USING (member_id) WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        all_items = itemID + recipeList

        open_wallet(ctx.author)
        open_wallet(member)

        if not str(amount).isnumeric():  # error checking
            return await ctx.send("Try typing a number next time!")
        amount = int(amount)
        if amount < 1:
            return await ctx.send("You can't give someone a negative amount!")

        if item is not None:  # item handling
            for i in range(len(all_items)):
                if item == all_items[i]:
                    if amount > result[i + 1]:
                        await ctx.send(f"You do not own {amount} `{all_items[i]}`. Try using the command correctly")
                        return
                    else:
                        add_item(member, amount, item, i)
                        remove_item(ctx.author, amount, item, i)
                        await ctx.send(f"Gave {amount} `{all_items[i]}` to {member.name}")
        else:
            if not check_bal_greater_than(ctx.author, amount):
                return await ctx.send("Your amount cannot be greater than your wallet")

            remove_bal(ctx.author, amount)
            add_bal(member, amount)
            await ctx.send(f"Gave <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** to {member.name}")

    @commands.command(name="steal", aliases=["rob"])  # steal money command
    @commands.cooldown(1, 60, BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        chance = [1, 2]
        steal_chance = random.choice(chance)
        open_wallet(ctx.author)
        open_wallet(member)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from wallets WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if member == ctx.author:
            self.client.get_command("steal").reset_cooldown(ctx)
            return await ctx.send("You cannot steal from yourself!")

        if result[1] < 500:
            self.client.get_command("steal").reset_cooldown(ctx)
            return await ctx.send(
                "You need at least <:KoffeeKoin:939562780363726868> **500** in your wallet to rob someone")

        cursor.execute(f"SELECT * from wallets WHERE member_id = {member.id}")
        result = cursor.fetchone()
        steal_money = random.choice(range(1, result[1]))

        if result[1] < 500 or result[1] == 0:
            self.client.get_command("steal").reset_cooldown(ctx)
            return await ctx.send(
                "Your target needs to have at least <:KoffeeKoin:939562780363726868> **500** in their wallet for you to rob "
                "them")

        if steal_chance == 1:
            remove_bal(member, steal_money)
            add_bal(ctx.author, steal_money)
            await ctx.send(f"You stole <:KoffeeKoin:939562780363726868> **{'{:,}'.format(steal_money)}** from {member}")
        else:
            remove_bal(ctx.author, 500)
            add_bal(member, 500)
            await ctx.send("You were caught and paid your victim <:KoffeeKoin:939562780363726868> **500**")

    @commands.command(name='heist', aliases=['bankrob'])
    @commands.cooldown(1, 21600, BucketType.user)
    async def heist(self, ctx, member: discord.Member):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from mafia WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        mafname = result[1]

        if result[2] != 'Boss':
            self.client.get_command("heist").reset_cooldown(ctx)
            return await ctx.send("Only the Boss can start a heist!")

        cursor.execute(f"SELECT * from mafia WHERE member_id = {member.id}")
        result = cursor.fetchone()
        if result[1] == mafname:
            self.client.get_command("heist").reset_cooldown(ctx)
            return await ctx.send(f"You can not heist someone from your own mafia")

        cursor.execute(f"SELECT * from wallets WHERE member_id = {member.id}")
        result = cursor.fetchone()
        bank_val = result[2]

        if member == ctx.author:
            self.client.get_command("heist").reset_cooldown(ctx)
            return await ctx.send("You can not rob your own bank account!")

        embed = discord.Embed(title="HEIST",
                              description=f"{ctx.author.mention} has decided to rob {member.mention}'s bank account\n"
                                          f"To join the heist please type `join heist` in chat.",
                              color=discord.Color.orange())
        await ctx.send(embed=embed)

        chance = random.randint(1, 3)
        heist_members = [ctx.author.name]
        death = [ctx.author]
        i = 0
        while i < 2:
            try:
                msg = await self.client.wait_for(event='message', timeout=7.0)
            except asyncio.TimeoutError:
                self.client.get_command("heist").reset_cooldown(ctx)
                return await ctx.send(f"Not enough people responded in time. You need 3 people to start a heist")
            else:
                if msg.content.startswith("join heist"):
                    if msg.author == member:
                        await ctx.send("You can not join a heist against you")
                        continue
                    cursor.execute(f"SELECT * from mafia WHERE member_id = {msg.author.id}")
                    result = cursor.fetchone()
                    if result[1] != mafname:
                        await ctx.send(f"Only members from {mafname} can join this heist")
                        continue
                    if msg.author.name not in heist_members:
                        heist_members.append(msg.author.name)
                        death.append(msg.author)
                    else:
                        continue
                    i += 1
                    await ctx.send(f"{msg.author.name} has joined the heist!")

        embed = discord.Embed(title="HEIST",
                              description=f"{heist_members[0]}, {heist_members[1]}, and {heist_members[2]}\nare attemping to break into {member.mention}'s bank account...",
                              color=discord.Color.orange())
        await ctx.send(embed=embed)
        time.sleep(5)
        dead = random.choice(death)
        outcome = "FAILURE"
        determine = f"You had been caught during the heist and were shot at gunpoint. `{dead.name}` did not survive"

        if chance == 2:
            amount = random.randrange(0, (bank_val - round(bank_val / 2, 0)))
            add_vault(mafname, amount)

            cursor.execute(f"SELECT * from wallets WHERE member_id = {member.id}")
            result = cursor.fetchone()
            sql = f"UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (result[2] - amount, member.id)
            cursor.execute(sql, val)
            db.commit()

            outcome = "SUCCESS"
            determine = f"You have collected a total amount of {amount} from your heist!"

            for person in death:
                add_heist_completed(person, 1)

        elif chance == 1 or chance == 0:
            cursor.execute(f"SELECT * from wallets WHERE member_id = {dead.id}")
            result = cursor.fetchone()
            remove_bal(dead, result[1])

            sql = f"UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (0, dead.id)
            cursor.execute(sql, val)
            db.commit()

        embed = discord.Embed(title=f"{outcome}", description=f"{determine}", color=discord.Color.orange())
        await ctx.send(embed=embed)

    @commands.command(name="dep", aliases=['deposit'])  # deposit command
    @commands.cooldown(1, 3, BucketType.user)
    async def dep(self, ctx, amount):
        sql = ''
        val = 0

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from wallets WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[1] == 0:
            return await ctx.send("You don't have any money to deposit")

        done = False
        amount = str(amount)
        if str(amount) == "all" or str(amount) == "max":
            sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (result[2] + result[1], ctx.author.id)
            await ctx.send(
                f"Successfully deposited <:KoffeeKoin:939562780363726868> **{'{:,}'.format(result[1])}** into your bank account")
            remove_bal(ctx.author, result[1])
            done = True
        if not done:
            try:
                amount = int(amount)
                assert amount > 0

            except AssertionError:
                return await ctx.send("You can not deposit negative money")
            except ValueError:
                return await ctx.send("Maybe try typing an actual number!")

            if result[1] < amount:
                return await ctx.send(
                    f"You cannot deposit more than <:KoffeeKoin:939562780363726868> **{'{:,}'.format(result[1])}**")

            sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (result[2] + amount, ctx.author.id)
            await ctx.send(
                f"Successfully deposited <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** into your bank account"
            )
            remove_bal(ctx.author, amount)

        cursor.execute(sql, val)
        db.commit()

    @commands.command(name='scam')  # scam command
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def scam(self, ctx):
        chance = [1, 2, 3]
        amount = random.randrange(500, 2000)

        if chance == 2:
            return await ctx.send("You went scamming and came home empty handed :(")
        else:
            await ctx.send(f"You scammed some guy for <:KoffeeKoin:939562780363726868> *"
                           f"*{'{:,}'.format(amount)}**")
            add_bal(ctx.author, amount)

    @commands.command(name="with", aliases=['withdraw'])  # withdraw money command
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def withdraw(self, ctx, amount: str):
        sql = ''
        val = 0

        open_wallet(user=ctx.author)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        amount = str(amount)
        if result[2] == 0:
            return await ctx.send(
                "You dont have any money in your bank :|"
            )

        done = False

        if str(amount) == "max" or str(amount) == "all":
            amount = result[2]
            await ctx.send(
                f"Successfully withdrawn <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from your bank account")
            sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (0, ctx.author.id)

            add_bal(ctx.author, result[2])
            done = True

        if not done:
            try:
                amount = int(amount)
                assert amount > 0

            except AssertionError:
                return await ctx.send("You can not deposit negative money")
            except ValueError:
                return await ctx.send(
                    "Maybe try typing an actual number next time!")

            if int(amount) > result[2]:
                return await ctx.send(
                    "You cannot withdraw an amount bigger than your bank balance :|")
            else:
                sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
                val = (result[2] - amount, ctx.author.id)
                add_bal(ctx.author, amount)
                await ctx.send(
                    f"Successfully withdrawn <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from your bank account"
                )

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(name="recipes", aliases=["recipe"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def recipes(self, ctx):
        embed = discord.Embed(title='Recipes', color=discord.Color.orange())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
        embed.add_field(name=":coffee: common coffee `ID: ccoffee`",
                        value="<:mug:950689993867788338> *mug: **1***\n"
                              "<:coffee_bean:951551479989301338> *coffee bean: **3***\n"
                              ":milk: *milk: **1***\n"
                              "<:sugar:951066869304029214> *sugar: **2***\n"
                              ":spoon: *spoon: **1***",
                        inline=False)

        embed.add_field(name="<:rare_coffee:951551480215789658> rare coffee `ID: rcoffee`",
                        value="<:mug:950689993867788338> *mug: **1***\n"
                              "<:coffee_bean:951551479989301338> *coffee bean: **7***\n"
                              "<:pmilk:951741856264368128> *premium milk: **1***\n"
                              "<:sugar:951066869304029214> *sugar: **3***\n"
                              "<:gspoon:951731109312479243> *golden spoon: **1***",
                        inline=False)

        embed.add_field(name="<:tea:959165836042588250> tea `ID: tea`",
                        value="<:mug:950689993867788338> *mug: **1***\n"
                              ":milk: *milk: **1***\n"
                              "<:sugar:951066869304029214> *sugar: **3***\n"
                              ":spoon: *spoon: **1***\n"
                              "<:teabag:957760498902900806> *teabag: **1***")
        await ctx.send(embed=embed)

    @commands.command(name='craft', aliases=["create"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def craft(self, ctx, item, amount=1):
        user = ctx.author
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {user.id}")
        result = cursor.fetchone()

        hasEnough = []

        if item == recipeList[0]:  # ccoffee
            for x in range(len(ccoffeeRecipeAmount)):
                if result[x + 1] >= ccoffeeRecipeAmount[x] * amount:
                    hasEnough.append(x)
            if len(hasEnough) == len(ccoffeeRecipeAmount):
                await ctx.send(f"You've crafted {amount} `common coffee`")
                add_crafted_item(user, amount, item, 1)
                remove_item(user, 1 * amount, itemID[0], 0)
                remove_item(user, 3 * amount, itemID[1], 1)
                remove_item(user, 1 * amount, itemID[2], 2)
                remove_item(user, 2 * amount, itemID[4], 4)
                remove_item(user, 1 * amount, itemID[5], 5)
            else:
                await ctx.send("You do not have enough ingredients to craft this item")

        elif item == recipeList[1]:  # rcoffee
            for x in range(len(rcoffeeRecipeAmount)):
                if result[x + 1] >= rcoffeeRecipeAmount[x] * amount:
                    hasEnough.append(x)
            if len(hasEnough) == len(rcoffeeRecipeAmount):
                await ctx.send(f"You've crafted {amount} `rare coffee`")
                add_crafted_item(user, amount, item, 2)
                remove_item(user, 1 * amount, itemID[0], 0)
                remove_item(user, 7 * amount, itemID[1], 1)
                remove_item(user, 1 * amount, itemID[3], 3)
                remove_item(user, 3 * amount, itemID[4], 4)
                remove_item(user, 1 * amount, itemID[6], 6)
            else:
                await ctx.send("You do not have enough ingredients to craft this item")

        elif item == recipeList[2]:  # tea
            for x in range(len(teaRecipeAmount)):
                if result[x + 1] >= teaRecipeAmount[x] * amount:
                    hasEnough.append(x)
            if len(hasEnough) == len(teaRecipeAmount):
                await ctx.send(f"You've crafted {amount} `tea`")
                add_crafted_item(user, amount, item, 3)
                remove_item(user, 1 * amount, itemID[0], 0)
                remove_item(user, 1 * amount, itemID[2], 2)
                remove_item(user, 3 * amount, itemID[4], 4)
                remove_item(user, 1 * amount, itemID[5], 5)
                remove_item(user, 1 * amount, itemID[7], 7)
            else:
                await ctx.send("You do not have enough ingredients to craft this item")
        else:
            await ctx.send("That is not a craftable item")

    @commands.command(name='use')  # use item
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def use(self, ctx, item):
        user = ctx.author
        amount = int(1)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {user.id}")
        result = cursor.fetchone()

        recipes = ["ccoffee", "rcoffee"]
        itemName = ["common coffee", "rare coffee"]
        for i in range(len(recipes)):
            if item == recipes[i]:
                if result[i + 10] < 1:
                    await ctx.send(f"You do not own any `{itemName[i]}`. Go and craft some")
                    break
                else:
                    await ctx.send(f"Used `{itemName[i]}`")
                    remove_item(ctx.author, amount, item, i + 7)
                    break
            else:
                await ctx.send("That is not a craftable item")
                continue

    @commands.command(name='shop')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shop(self, ctx, category=1):

        if category == 1:
            embed = discord.Embed(title='Shop 1', color=discord.Color.orange())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name="<:mug:950689993867788338> *mug:*  <:KoffeeKoin:939562780363726868> **5,000**",
                            value="ID: `mug`",
                            inline=False)
            embed.add_field(name="<:coffee_bean:951551479989301338> *coffee bean:*  <:KoffeeKoin:939562780363726868> "
                                 "**1,500**", value="ID: `bean`",
                            inline=False)
            embed.add_field(name=":milk: *milk:*  <:KoffeeKoin:939562780363726868> **10,000**", value="ID: `milk`",
                            inline=False)
            embed.add_field(name="<:sugar:951066869304029214> *sugar:*  <:KoffeeKoin:939562780363726868> **2,500**",
                            value="ID: `sugar`", inline=False)
            embed.add_field(name=":spoon: *spoon:*  <:KoffeeKoin:939562780363726868> **1,000**", value="ID: `spoon`",
                            inline=False)
            embed.set_footer(text='Shop 1/2')
            await ctx.send(embed=embed)
        if category == 2:
            embed = discord.Embed(title='Shop 2', color=discord.Color.orange())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name="<:gspoon:951731109312479243> *golden spoon:*  <:KoffeeKoin:939562780363726868> "
                                 "**15,000**", value="ID: `gspoon`", inline=False)
            embed.add_field(
                name="<:pmilk:951741856264368128> *premium milk:*  <:KoffeeKoin:939562780363726868> **50,000**",
                value="ID: `pmilk`", inline=False)
            embed.add_field(name="<:teabag:957760498902900806> teabag <:KoffeeKoin:939562780363726868> **5,000**",
                            value="ID: `teabag`", inline=False)
            embed.add_field(name="<:hat:984285090190360657> mafia hat <:KoffeeKoin:939562780363726868> **500,000**",
                            value="ID: `hat`", inline=False)
            embed.set_footer(text='Shop 2/2')
            await ctx.send(embed=embed)

    @commands.command(name='buy')  # buy command
    async def buy(self, ctx, item, amount=1):
        user = ctx.author
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {user.id}")
        result = cursor.fetchone()

        for i in range(len(itemID)):
            if item == itemID[i]:
                if itemvalue[i] * amount > result[1]:
                    return await ctx.send("Insufficient funds")
                await ctx.send(f"Purchased {amount} `{itemID[i]}` for <:KoffeeKoin:939562780363726868>**"
                               f"{'{:,}'.format(itemvalue[i] * amount)}**")
                remove_bal(ctx.author, itemvalue[i] * amount)
                add_item(ctx.author, amount, item, i)
                break

    @commands.command(name='sell')  # sell command
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def sell(self, ctx, item, amount=1):
        user = ctx.author
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {user.id}")
        result = cursor.fetchone()

        for i in range(len(itemID)):
            if item == itemID[i]:
                if int(amount) > int(result[i + 1]):
                    await ctx.send("You cannot sell more than you have")
                    return
                if result[i + 1] == 0:
                    await ctx.send("You have nothing to sell!")
                    return
                await ctx.send(f"Sold {amount} `{itemID[i]}` for <:KoffeeKoin:939562780363726868>"
                               f"**{'{:,}'.format(round((itemvalue[i] * amount / 2)))}**")
                add_bal(ctx.author, round(itemvalue[i] * amount / 2))
                remove_item(ctx.author, amount, item, i)
                break

    @commands.command(name='inventory', aliases=['inv'])  # inventory command
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def inventory(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients INNER JOIN recipes USING (member_id) WHERE member_id = {user.id}")
        result = cursor.fetchone()
        all_items = itemID + recipeList

        embed = discord.Embed(title=f"{user.name}'s inventory", color=discord.Color.orange())
        embed.set_thumbnail(url=user.iconavatar)
        inven = []
        for i in range(len(all_items)):
            if result[i + 1] != 0:
                inven.append(i)
        for i in inven:
            embed.add_field(name=f"{itemlist[i]}  {result[i + 1]}", value=f"ID: `{all_items[i]}`",
                            inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='job', aliases=['jobs', 'joblist'])  # job list
    async def job(self, ctx):
        embed = discord.Embed(title="Current available jobs",
                              description="`kof work [job]` to select a job\n"
                                          "`kof work` to start working\n"
                                          "`kof resign` to quit your current job",
                              color=discord.Color.orange())

        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name='Babysitter 👶',
                        value='Requires: <:tea:959165836042588250>\nSalary: <:KoffeeKoin:939562780363726868> **5,000**',
                        inline=False)
        embed.add_field(name='Teacher 🦉',
                        value='Requires: ☕\nSalary: <:KoffeeKoin:939562780363726868> **8,000**', inline=False)
        embed.add_field(name='Accountant 😢',
                        value='Requires: ☕\nSalary: <:KoffeeKoin:939562780363726868> **10,000**', inline=False)
        embed.add_field(name='Programmer 💻',
                        value='Requires: <:rare_coffee:951551480215789658>\nSalary: <:KoffeeKoin:939562780363726868> **15,000**',
                        inline=False)
        embed.add_field(name='Lawyer 💼',
                        value='Requires: <:rare_coffee:951551480215789658>\nSalary: <:KoffeeKoin:939562780363726868> **15,000**',
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='work')  # work command
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx, job=None):

        open_wallet(user=ctx.author)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets INNER JOIN recipes USING (member_id) WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        joblist = ['babysitter', 'teacher', 'accountant', 'programmer', 'lawyer']
        salary = [5000, 8000, 10000, 15000, 15000]
        fire_chance = random.randint(1, 20)
        tired_chance = random.randint(1, 20)

        if job is None:
            for i in range(len(joblist)):
                if result[3] == joblist[i]:

                    outcomes = [
                        f"You worked in your office for 2 hours and received <:KoffeeKoin:939562780363726868> **{'{:,}'.format(salary[i])}**",
                        f"Your boss was frustrated but you worked for him and got <:KoffeeKoin:939562780363726868> **{'{:,}'.format(salary[i])}**",
                        f"You begged your boss for <:KoffeeKoin:939562780363726868> **{'{:,}'.format(salary[i])}**",
                        f"You killed your boss and got <:KoffeeKoin:939562780363726868> **{'{:,}'.format(salary[i])}** from his wallet",
                        f"You finished a long day at work! You earned <:KoffeeKoin:939562780363726868> **{'{:,}'.format(salary[i])}** today"]
                    fire = ["You have have been fired from your job",
                            "Your boss was unhappy with your performance. You have been fired"]

                    if tired_chance == 9:
                        if result[3] == "babysitter":
                            await ctx.send(
                                f"You have used up all your <:tea:959165836042588250> `tea`. Without it you cannot work\n"
                                "You will need to craft a new form of energy and start looking for a job again")
                            update_job(ctx.author, 'unemployed')
                            remove_crafted_item(ctx.author, 1, "tea", 3)
                            self.client.get_command("work").reset_cooldown(ctx)
                            return
                        elif result[3] == "teacher":
                            await ctx.send(f"You have used up all your ☕ `ccoffee`. Without it you cannot work\n"
                                           "You will need to craft a new form of energy and start looking for a job again")
                            update_job(ctx.author, 'unemployed')
                            remove_crafted_item(ctx.author, 1, "ccoffee", 1)
                            self.client.get_command("work").reset_cooldown(ctx)
                            return
                        elif result[3] == "accountant":
                            await ctx.send(f"You have used up all your ☕ `ccoffee`. Without it you cannot work\n"
                                           "You will need to craft a new form of energy and start looking for a job again")
                            update_job(ctx.author, 'unemployed')
                            remove_crafted_item(ctx.author, 1, "ccoffee", 1)
                            self.client.get_command("work").reset_cooldown(ctx)
                            return
                        elif result[3] == "programmer":
                            await ctx.send(
                                f"You have used up all your <:rare_coffee:951551480215789658> `rcoffee`. Without it you cannot work\n"
                                "You will need to craft a new form of energy and start looking for a job again")
                            update_job(ctx.author, 'unemployed')
                            remove_crafted_item(ctx.author, 1, "rcoffee", 2)
                            self.client.get_command("work").reset_cooldown(ctx)
                            return
                        elif result[3] == "lawyer":
                            await ctx.send(
                                f"You have used up all your <:rare_coffee:951551480215789658> `rcoffee`. Without it you cannot work\n"
                                "You will need to craft a new form of energy and start looking for a job again")
                            update_job(ctx.author, 'unemployed')
                            remove_crafted_item(ctx.author, 1, "rcoffee", 2)
                            self.client.get_command("work").reset_cooldown(ctx)
                            return

                    if fire_chance == 19:
                        await ctx.send(random.choice(fire))
                        update_job(ctx.author, 'unemployed')
                        return
                    else:
                        add_bal(ctx.author, salary[i])
                        await ctx.send(random.choice(outcomes))
                        return

        elif job == 'babysitter':
            if result[3] != 'unemployed':
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send('You already have a job!')

            if result[6] < 1:
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send(
                    "You need to craft at least 1 <:tea:959165836042588250> `tea` to qualify for this job")
            else:
                await ctx.send("You are now a babysitter. Use `kof work` to start working")
                self.client.get_command("work").reset_cooldown(ctx)
                update_job(ctx.author, job)
                return

        elif job == 'teacher':
            if result[3] != 'unemployed':
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send('You already have a job!')

            if result[4] < 1:
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send("You need to craft at least 1 ☕ `ccoffee` to qualify for this job")
            else:
                await ctx.send("You are now a teacher. Use `kof work` to start working")
                self.client.get_command("work").reset_cooldown(ctx)
                update_job(ctx.author, job)
                return

        elif job == 'accountant':
            if result[3] != 'unemployed':
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send('You already have a job!')

            if result[4] < 1:
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send("You need to craft at least 1 ☕ `ccoffee` to qualify for this job")
            else:
                await ctx.send("You are now an accountant. Use `kof work` to start working")
                self.client.get_command("work").reset_cooldown(ctx)
                update_job(ctx.author, job)
                return

        elif job == 'programmer':
            if result[3] != 'unemployed':
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send('You already have a job!')

            if result[5] < 1:
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send("You need to craft at least 1 ☕ `rcoffee` to qualify for this job")
            else:
                update_job(ctx.author, job)
                await ctx.send("You are now a programmer. Use `kof work` to start working")
                self.client.get_command("work").reset_cooldown(ctx)
                return
        elif job == 'lawyer':
            if result[3] != 'unemployed':
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send('You already have a job!')

            if result[5] < 1:
                self.client.get_command("work").reset_cooldown(ctx)
                return await ctx.send("You need to craft at least 1 ☕ `rcoffee` to qualify for this job")
            else:
                await ctx.send("You are now a lawyer. Use `kof work` to start working")
                self.client.get_command("work").reset_cooldown(ctx)
                update_job(ctx.author, job)
                return

        if result[3] == 'unemployed':
            await ctx.send("You are currently unemployed. Use `kof jobs` to look for a job")
            self.client.get_command("work").reset_cooldown(ctx)
            return

    @commands.command(name='resign', aliases=['quit'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def resign(self, ctx):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[3] == 'unemployed':
            await ctx.send("You are already unemployed")
            return

        await ctx.send("You have quit your current job...you will need to wait an hour before choosing a new job")
        update_job(ctx.author, 'unemployed')

    @commands.command(name='daily')  # daily command
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        open_wallet(user=ctx.author)
        daily_amount = 25000
        await ctx.send(
            f"You have recieved your daily amount of <:KoffeeKoin:939562780363726868> **{'{:,}'.format(daily_amount)}**")
        add_bal(ctx.author, daily_amount)

    @commands.command(name='lucky', aliases=['luck'])  # lucky command
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def lucky(self, ctx):
        open_wallet(user=ctx.author)
        rand_int = random.randint(1, 6)
        luck_money = random.randint(500, 2500)
        random_items = ["mug",
                        "bean",
                        "milk",
                        "sugar",
                        "spoon",
                        "teabag"]
        random_item = random.choice(random_items)
        item_quantity = random.randint(1, 2)

        lucks = [f"You found <:KoffeeKoin:939562780363726868> **{'{:,}'.format(luck_money)}** on the ground!",
                 f"Mr. Beast just so happened to be in town. He gave you <:KoffeeKoin:939562780363726868> **{'{:,}'.format(luck_money)}**!",
                 f"You've won the lottery! You received <:KoffeeKoin:939562780363726868> **{'{:,}'.format(luck_money)}**",
                 f"You checked under your shoe and found <:KoffeeKoin:939562780363726868> **{'{:,}'.format(luck_money)}**!",
                 f"A strange bag falls out of the sky. You open it and find <:KoffeeKoin:939562780363726868> **{'{:,}'.format(luck_money)}**"]
        if rand_int == 2 or rand_int == 4:
            await ctx.send(random.choice(lucks))
            add_bal(ctx.author, luck_money)
        elif rand_int == 3:
            await ctx.send(f"Oh look! You found {item_quantity} `{random_item}`")
            add_item(ctx.author, item_quantity, random_item, random_items.index(random_item) + 1)
        else:
            await ctx.send("You're not feeling particularly lucky today")

    @commands.command(name='slots', aliases=["slot"])  # slot machine commands
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def slots(self, ctx, amount):
        outcomes = [":banana:", ":cherries:", ":candy:"]
        one = random.choice(outcomes)
        two = random.choice(outcomes)
        three = random.choice(outcomes)
        win = int(amount) * 7
        lose = ["Tough luck :(", "Rip your money lol", "Oof!"]

        if ctx.author.id == 397118054267355149:
            self.client.get_command("slots").reset_cooldown(ctx)

        try:
            amount = int(amount)
        except ValueError:
            self.client.get_command("slots").reset_cooldown(ctx)
            return await ctx.send(
                "Maybe try typing an actual number"
            )
        if amount < 500:
            self.client.get_command("slots").reset_cooldown(ctx)
            return await ctx.send(
                "You need at least <:KoffeeKoin:939562780363726868> **500** in your wallet to use the slot machine"
            )

        result = check_bal_greater_than(user=ctx.author, amount=amount)
        if result is False:
            self.client.get_command("slots").reset_cooldown(ctx)
            return await ctx.send(
                "Your amount cannot be greater than your wallet :|")

        em1 = discord.Embed(title="=-=-=-=-=-=\n"
                                  ":red_square: :red_square: :red_square: :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.orange())
        em1.set_author(name="Slot machine", icon=ctx.author.iconavatar)
        em2 = discord.Embed(title=f"=-=-=-=-=-=\n"
                                  f"{one} :red_square: :red_square: :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.orange())
        em2.set_author(name="Slot machine", icon=ctx.author.iconavatar)
        em3 = discord.Embed(title=f"=-=-=-=-=-=\n"
                                  f"{one} {two} :red_square: :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.orange())
        em3.set_author(name="Slot machine", icon=ctx.author.iconavatar)
        em4 = discord.Embed(title=f"=-=-=-=-=-=\n"
                                  f"{one} {two} {three} :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.orange())
        em4.set_author(name="Slot machine", icon=ctx.author.iconavatar)

        msg = await ctx.send(embed=em1)
        time.sleep(0.7)
        await msg.edit(embed=em2)
        time.sleep(0.7)
        await msg.edit(embed=em3)
        time.sleep(0.7)
        await msg.edit(embed=em4)

        if one == two == three:
            add_bal(ctx.author, win - amount)
            embed = discord.Embed(
                description=f"Congratulations!!! {ctx.author.mention}\nYou won <:KoffeeKoin:939562780363726868> **{'{:,}'.format(win)}**!",
                color=discord.Color.orange())
            embed.set_author(name="Slot machine", icon=ctx.author.iconavatar)
            await ctx.send(embed=embed)
        else:
            remove_bal(ctx.author, amount)
            embed = discord.Embed(description=random.choice(lose), color=discord.Color.orange())
            embed.set_author(name="Slot machine", icon=ctx.author.iconavatar)
            await ctx.send(embed=embed)

    @commands.command(name="rich", aliases=['leaderboard', 'lb'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rich(self, ctx):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets ORDER BY bank DESC")
        result = cursor.fetchall()

        guild = ctx.author.guild
        memberList = guild.members
        db_array = []
        member_array = []
        valid = []
        top_10 = []

        for i in range(len(result)):  # placing all members in the db into an array
            db_array.append(result[i][0])

        for i in range(len(memberList)):  # placing all members from guild into an array
            member_array.append(memberList[i].id)

        for i in range(len(db_array)):
            if db_array[i] in member_array:
                valid.append(db_array[i])

        if len(valid) < 10:
            return await ctx.send(
                "At least 10 people in this server need a KoffeeBot account/balance\nYou can open an account by typing `kof bal`")

        for i in range(len(valid)):
            user = await self.client.fetch_user(valid[i])
            top_10.append(user)
            if i > 9:
                break

        cursor.execute(
            f"SELECT * FROM wallets WHERE member_id IN ({top_10[0].id},{top_10[1].id},{top_10[2].id},{top_10[3].id},{top_10[4].id},{top_10[5].id},{top_10[6].id},{top_10[7].id},{top_10[8].id},{top_10[9].id}) ORDER BY bank DESC")
        result = cursor.fetchall()

        embed = discord.Embed(title=f"Top 10 Richest people in {guild}",
                              description=f"**1.** `{top_10[0].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[0][2])}\n"
                                          f"**2.** `{top_10[1].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[1][2])}\n"
                                          f"**3.** `{top_10[2].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[2][2])}\n"
                                          f"**4.** `{top_10[3].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[3][2])}\n"
                                          f"**5.** `{top_10[4].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[4][2])}\n"
                                          f"**6.** `{top_10[5].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[5][2])}\n"
                                          f"**7.** `{top_10[6].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[6][2])}\n"
                                          f"**8.** `{top_10[7].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[7][2])}\n"
                                          f"**9.** `{top_10[8].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[8][2])}\n"
                                          f"**10.** `{top_10[9].name}`: **<:KoffeeKoin:939562780363726868> {'{:,}**'.format(result[9][2])}\n",
                              color=discord.Color.orange())
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)

    @commands.command(name='mafia')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def mafia(self, ctx, action=None, target=None):
        user = ctx.author

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {user.id}")
        result = cursor.fetchone()
        open_mafia(user)

        if action == 'create':  # creating a mafia
            if result[9] < 1:  # lack of item
                return await ctx.send("You need a `mafia hat` to create a mafia")
            cursor.execute(f"SELECT * FROM wallets WHERE member_id = {user.id}")
            result = cursor.fetchone()
            if result[1] < 100000:  # insufficient cash
                return await ctx.send("You need <:KoffeeKoin:939562780363726868>**100,000** to create a mafia")
            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
            result = cursor.fetchone()
            if result[1] != 'none':  # already in a mafia
                return await ctx.send("You are already part of a mafia!")
            edit_mafia_name(user, target)
            edit_mafia_rank(user, 'Boss')
            open_vault(target)
            remove_bal(user, 100000)
            return await ctx.send(f"Created mafia: `{target}`")

        elif action == 'delete':  # deleting a mafia
            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
            result = cursor.fetchone()

            if result[1] == 'none':
                return await ctx.send("You are not currently in any mafia.")
            if result[2] != "Boss":
                return await ctx.send("Only the Boss can delete a mafia")

            await ctx.send(f"Are you sure you want to disband `{result[1]}` with all of its members? (yes/no)")
            maf_name = result[1]

            try:
                msg = await self.client.wait_for(event='message', timeout=10.0)
            except asyncio.TimeoutError:
                self.client.get_command("mafia").reset_cooldown(ctx)
                return await ctx.send(
                    f"You did not respond quick enough")
            else:
                if msg.content.startswith("yes"):
                    cursor.execute(f"SELECT * FROM mafia")
                    result = cursor.fetchall()

                    for i in range(len(result)):
                        if result[i][1] == maf_name:
                            user = await self.client.fetch_user(result[i][0])
                            edit_mafia_name(user, 'none')
                            edit_mafia_rank(user, 'none')
                            cursor.execute(f"DELETE FROM mafias WHERE mafia_name = '{maf_name}'")
                            db.commit()
                    return await ctx.send(f"You have disbanded your mafia: `{maf_name}`")
                elif msg.content.startswith("no"):
                    await msg.add_reaction("👍")
                    return

        elif action == 'leave':  # deleting a mafia
            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
            result = cursor.fetchone()

            if result[1] == 'none':
                return await ctx.send("You are not currently in any mafia.")
            elif result[2] == 'Boss':
                return await ctx.send(
                    "You cannot leave your own mafia. Either promote someone else to `Boss` or disband the entire mafia")

            edit_mafia_name(user, 'none')
            edit_mafia_rank(user, 'none')
            await ctx.send(f"You have left `{result[1]}`")

        elif action == 'invite':  # inviting to mafia
            target = target.strip('<@>')
            target = await self.client.fetch_user(target)

            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
            result = cursor.fetchone()
            if result[1] == 'none':
                return await ctx.send("You are not currently in any mafia. Create one to be able to invite other users")
            if result[2] == "Boss" or result[2] == "Recruiter":
                pass
            else:
                return await ctx.send("Only the Boss or a recruiter can invite people to the mafia")

            await ctx.send(f"{target.mention}! You have been invited to join {ctx.author.name}'s mafia: `{result[1]}`\n"
                           f"Type `accept` or `decline` in chat")

            def check(m):
                return m.author == target

            try:
                msg = await self.client.wait_for(event='message', check=check, timeout=10.0)
            except asyncio.TimeoutError:
                self.client.get_command("mafia").reset_cooldown(ctx)
                return await ctx.send(f"The person you tried to invite did not respond in time")
            else:
                if msg.content.startswith("decline"):
                    return await ctx.send(
                        f"{user.mention}, {target.name} has declined your invitation to join {result[1]}")
                elif msg.content.startswith("accept"):
                    open_mafia(target)
                    maf_name = result[1]

                    cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {target.id}")
                    result = cursor.fetchone()
                    if result[9] < 1:  # lack of item
                        return await ctx.send("You need a `mafia hat` to join a mafia")

                    cursor.execute(f"SELECT * FROM mafia WHERE member_id = {target.id}")
                    cursor.fetchone()
                    edit_mafia_name(target, maf_name)
                    edit_mafia_rank(target, "Member")
                    return await ctx.send(f"{target.name} has joined `{maf_name}`")

        elif action == 'kick':
            target = target.strip('<@>')
            target = await self.client.fetch_user(target)

            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {ctx.author.id}")
            result = cursor.fetchone()
            mafname = result[1]
            if result[1] == 'none':
                return await ctx.send(
                    "You aren't currently in any mafia. Join or create a mafia to view your mafia stats")
            if result[2] != "Boss":
                return await ctx.send("Only the Boss can kick members")
            elif target == ctx.author:
                return await ctx.send("You can not kick yourself")

            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {target.id}")
            result = cursor.fetchone()
            if result[1] != mafname:
                return await ctx.send("This person is not in your mafia")
            edit_mafia_name(target, 'none')
            edit_mafia_rank(target, 'none')
            await ctx.send(f"You kicked {target.name} from `{mafname}`")

        elif action is None:  # mafia stats
            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
            result = cursor.fetchone()
            maf_name = result[1]
            if result[1] == 'none':
                return await ctx.send(
                    "You aren't currently in any mafia. Join or create a mafia to view your mafia stats")

            embed = discord.Embed(title=f"<:hat:984285090190360657> {result[1]} Mafia <:hat:984285090190360657>",
                                  color=discord.Color.orange())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name='Profile', value=f"**`Title:`** {result[2]}\n**`Heists completed:`** {result[3]}",
                            inline=True)

            cursor.execute(f"SELECT * FROM mafias WHERE mafia_name = '{maf_name}'")
            result = cursor.fetchone()
            embed.add_field(name='Vault', value=f"<:KoffeeKoin:939562780363726868>{'{:,}'.format(result[1])}",
                            inline=False)

            cursor.execute(f"SELECT * FROM mafia WHERE mafia_name = '{maf_name}'")
            result = cursor.fetchall()
            owner = ""
            for i in range(len(result)):
                if result[i][2] == "Boss":
                    owner = await self.client.fetch_user(result[i][0])

            embed.add_field(name='Mafia Info', value=f'**`Boss:` **{owner.name}\n **`Total members:`** {len(result)}',
                            inline=True)
            await ctx.send(embed=embed)

    @commands.command(name='promote')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def promote(self, ctx, user: discord.Member):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM mafia WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[1] == 'none':
            return await ctx.send("You are not currently in a mafia")
        elif result[2] != 'Boss':
            return await ctx.send("Only the Boss can promote")
        elif user == ctx.author:
            return await ctx.send("You can not promote yourself")
        mafname = result[1]

        cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
        result = cursor.fetchone()
        if result[1] != mafname:
            return await ctx.send("This person is not in your mafia")
        elif result[2] == 'Member':
            edit_mafia_rank(user, 'Recruiter')
            return await ctx.send(f"Promoted {user.name} to rank `Recruiter`")

    @commands.command(name='demote')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def demote(self, ctx, user: discord.Member):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM mafia WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[1] == 'none':
            return await ctx.send("You are not currently in a mafia")
        elif result[2] != 'Boss':
            return await ctx.send("Only the Boss can demote")
        elif user == ctx.author:
            return await ctx.send("You can not demote yourself")
        mafname = result[1]

        cursor.execute(f"SELECT * FROM mafia WHERE member_id = {user.id}")
        result = cursor.fetchone()
        if result[1] != mafname:
            return await ctx.send("This person is not in your mafia")
        elif result[2] == 'Recruiter':
            edit_mafia_rank(user, 'Member')
            return await ctx.send(f"Demoted {user.name} to rank `Member`")

    @commands.command(name='vault')  # vault command
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def vault(self, ctx, action, amount):
        open_mafia(ctx.author)
        sql = ''
        val = ''

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM mafia WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()
        mafname = result[1]

        cursor.execute(
            f"SELECT * FROM wallets LEFT JOIN mafias WHERE member_id = {ctx.author.id} AND mafia_name = '{mafname}'")
        result = cursor.fetchone()

        if result[4] == 'none':
            return await ctx.send("You aren't currently in any mafia. Join or create a mafia")

        if action == 'dep' or action == 'deposit':  # deposit into vault
            if result[1] == 0:
                return await ctx.send("You don't have any money to deposit")

            done = False
            amount = str(amount)
            if str(amount) == "all" or str(amount) == "max":
                sql = "UPDATE mafias SET vault = ? WHERE mafia_name = ?"
                val = (result[5] + result[1], result[4])

                await ctx.send(
                    f"Successfully deposited <:KoffeeKoin:939562780363726868> **{'{:,}'.format(result[1])}** into your vault")
                remove_bal(ctx.author, result[1])

                done = True
            if not done:
                try:
                    amount = int(amount)
                    assert amount > 0

                except AssertionError:
                    return await ctx.send("You can not deposit negative money")
                except ValueError:
                    return await ctx.send("Maybe try typing an actual number!")

                if result[1] < amount:
                    return await ctx.send(
                        f"You cannot deposit more than <:KoffeeKoin:939562780363726868> **{'{:,}'.format(result[1])}**")

                sql = "UPDATE mafias SET vault = ? WHERE mafia_name = ?"
                val = (result[5] + amount, result[4])

                await ctx.send(
                    f"Successfully deposited <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** into your vault")
                remove_bal(ctx.author, amount)

            cursor.execute(sql, val)
            db.commit()

        elif action == 'with' or action == 'withdraw':  # withdraw from vault
            cursor.execute(f"SELECT * FROM mafia WHERE member_id = {ctx.author.id}")
            result = cursor.fetchone()

            if result[2] != 'Boss':
                return await ctx.send("Only the Boss can withdraw from the vault")

            cursor.execute(
                f"SELECT * FROM wallets LEFT JOIN mafias WHERE member_id = {ctx.author.id} AND mafia_name = '{mafname}'")
            result = cursor.fetchone()

            amount = str(amount)

            if result[5] == 0:
                return await ctx.send("You dont have any money in your vault :|")
            done = False

            if str(amount) == "max" or str(amount) == "all":
                amount = result[5]
                await ctx.send(
                    f"Successfully withdrawn <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from your vault")
                sql = "UPDATE mafias SET vault = ? WHERE mafia_name = ?"
                val = (0, result[4])

                add_bal(ctx.author, result[5])
                done = True

            if not done:
                try:
                    amount = int(amount)
                    assert amount > 0

                except AssertionError:
                    return await ctx.send("You can not deposit negative money")
                except ValueError:
                    return await ctx.send(
                        "Maybe try typing an actual number next time!")

                if int(amount) > result[5]:
                    return await ctx.send(
                        "You cannot withdraw an amount bigger than your vault balance :|")
                else:
                    sql = "UPDATE mafias SET vault = ? WHERE mafia_name = ?"
                    val = (result[5] - amount, mafname)
                    add_bal(ctx.author, amount)
                    await ctx.send(
                        f"Successfully withdrawn <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from your vault"
                    )

            cursor.execute(sql, val)
            db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id == 979427519742759002:
            data = message.content.split(" ")
            user = re.sub("\D", "", data[0])

            user_object = self.client.get_user(int(user)) or await self.client.fetch_user(int(user))
            user = user_object
            open_wallet(user)
            add_bal(user, 25000)

            embed = discord.Embed(title="KoffeeBot Vote Rewards", color=discord.Color.orange())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922598156842172508/923140639556775946/koffee4.png')
            embed.add_field(name="Thank you for voting for me :D",
                            value=f"You have received <:KoffeeKoin:939562780363726868>**25,000**")
            await user_object.send(embed=embed)
            await self.client.process_commands(message)


async def setup(client):
    await client.add_cog(Economy(client))
