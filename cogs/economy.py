import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import sqlite3
import asyncio
import re

itemlist = ["<:mug:950689993867788338> mug:",
            "<:coffee_bean:951551479989301338> coffee bean:",
            ":milk: milk:",
            "<:pmilk:951741856264368128> premium milk",
            "<:sugar:951066869304029214> sugar:",
            ":spoon: spoon:",
            "<:gspoon:951731109312479243> golden spoon:",
            "<:teabag:957760498902900806> teabag",
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
          "teabag"]

itemvalue = [5000,  # mug
             1500,  # bean
             10000,  # milk
             50000,  # pmilk
             2500,  # sugar
             1000,  # spoon
             15000,  # gspoon
             5000]  # teabag

recipeList = ["ccoffee",
              "rcoffee",
              "tea"]

ccoffeeRecipeAmount = [1, 3, 1, 0, 2, 1, 0, 0]
rcoffeeRecipeAmount = [1, 7, 0, 1, 3, 0, 1, 0]
teaRecipeAmount = [1, 0, 1, 0, 3, 1, 0, 1]


def open_wallet(user: discord.Member):
    open_ingredients(user)
    open_recipes(user)

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


work_cd = app_commands.Cooldown(1, 3600)
steal_cd = app_commands.Cooldown(1, 60)
slots_cd = app_commands.Cooldown(1, 30)


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    def work_cooldown(interaction: discord.Interaction):
        return work_cd

    def steal_cooldown(interaction: discord.Interaction):
        return steal_cd

    def slots_cooldown(interaction: discord.Interaction):
        return slots_cd


    @app_commands.command(name="vote", description="Vote for KoffeeBot and receive a reward")
    async def vote(self, interactin: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        embed.add_field(name='Enjoying KoffeeBot?',
                        value="[Vote for me on top.gg!](https://top.gg/bot/901223515242508309/vote/)")
        await interactin.response.send_message(embed=embed)

    @app_commands.command(name="balance", description="View your current balance")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        open_wallet(member)

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {member.id}")
        result = cursor.fetchone()

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name=f"{member.name}'s Balance", icon_url=member.avatar)
        embed.add_field(name="Wallet:", value=f"<:KoffeeKoin:939562780363726868> {'{:,}'.format(result[1])}", inline=False)
        embed.add_field(name="Bank:", value=f"<:KoffeeKoin:939562780363726868> {'{:,}'.format(result[2])}", inline=False)
        embed.set_footer(text=f"Low on cash? Vote for me using /vote to earn a bit extra ;D")
        embed.set_thumbnail(url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='cheat', description="Magically enter some money into someone's wallet")
    @app_commands.describe(member="The uesr who's wallet needs money", amount="The amount of money you wish to give this user")
    async def cheat(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        open_wallet(member)
        user = interaction.user
        amount = int(amount)
        responses = ["no", "get lost!", "uhm...no", "You're not allowed to use this command :D", "Yeah no :)"]

        if user.id == 465839240777826324:
            add_bal(member, amount)
            await interaction.response.send_message(f"Gave <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** to {member.name}", ephemeral=True)
        else:
            embed = discord.Embed(title="BigLlama's totally cool and secret cheat command", description=random.choice(responses))
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="beg", description="Beg the rich for some money")  # beg command
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def beg(self, interaction: discord.Interaction):
        possibility = random.randint(1, 6)
        none = ["No money for you!",
                "Stop begging!",
                "Get lost!",
                "Away with you!",
                "Go get a job you useless begger!"]
        amount = random.randrange(1, 450)
        big_amount = random.randrange(800, 1100)

        if possibility == 3:
            await interaction.response.send_message(random.choice(none))
            return
        if possibility == 6:
            add_bal(interaction.user, big_amount)
            await interaction.response.send_message(f"Wow! You received a "
                f"generous donation of <:KoffeeKoin:939562780363726868> **{'{:,}'.format(big_amount)}**")
            return

        outcomes = [
            f"You got <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from a nice old lady",
            f"You received <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from a stranger",
            f"You begged your mom for <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}**"]

        add_bal(interaction.user, amount)
        await interaction.response.send_message(random.choice(outcomes))

    @app_commands.command(name="give", description="Give someone money or an item")  # give money command
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    async def give(self, interaction: discord.Interaction, member: discord.Member, amount: int, item: str = None):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM ingredients INNER JOIN recipes USING (member_id) WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()
        all_items = itemID + recipeList

        open_wallet(interaction.user)
        open_wallet(member)

        if amount < 0:
            embed = discord.Embed(title="Negative values", description="You can not use negative values!")
            await interaction.response.send_message(embed=embed)
            return

        if item is not None:  # item handling
            for i in range(len(all_items)):
                if item == all_items[i]:
                    if amount > result[i + 1]:
                        await interaction.response.send_message(f"You do not own {amount} `{all_items[i]}`. Try using the command correctly")
                        return
                    else:
                        add_item(member, amount, item, i)
                        remove_item(interaction.user, amount, item, i)
                        await interaction.response.send_message(f"Gave {amount} `{all_items[i]}` to {member.name}")
        else:
            if not check_bal_greater_than(interaction.user, amount):
                embed = discord.Embed(title="Incorrect Amount", description="You can not give more than you have")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                await interaction.response.send_message(embed=embed)
                return

            remove_bal(interaction.user, amount)
            add_bal(member, amount)
            await interaction.response.send_message(f"Gave <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** to {member.name}")

    @app_commands.command(name="steal", description="Attempt to steal money from someone's wallet")  # steal money command
    @app_commands.describe(member="You user you wish to rob")
    @app_commands.checks.dynamic_cooldown(steal_cooldown)
    async def steal(self, interaction: discord.Interaction, member: discord.Member):
        chance = [1, 2]
        steal_chance = random.choice(chance)
        open_wallet(interaction.user)
        open_wallet(member)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from wallets WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()

        if member == interaction.user:
            app_commands.Cooldown.reset(steal_cd)
            embed = discord.Embed(title="Member Error", description="You cannot steal from yourself!", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if result[1] < 500:
            app_commands.Cooldown.reset(steal_cd)
            embed = discord.Embed(title="Money Requirements",
                                  description="You need at least <:KoffeeKoin:939562780363726868> **500** in your wallet to rob someone",
                                  color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        cursor.execute(f"SELECT * from wallets WHERE member_id = {member.id}")
        result = cursor.fetchone()

        if result[1] < 500:
            app_commands.Cooldown.reset(steal_cd)
            await interaction.response.send_message("Your target needs to have at least <:KoffeeKoin:939562780363726868> **500** in their wallet for you to rob them", ephemeral=True)
            return

        steal_money = random.choice(range(1, result[1]))

        if steal_chance == 1:
            remove_bal(member, steal_money)
            add_bal(interaction.user, steal_money)
            await interaction.response.send_message(f"You stole <:KoffeeKoin:939562780363726868> **{'{:,}'.format(steal_money)}** from {member}")
        else:
            remove_bal(interaction.user, 500)
            add_bal(member, 500)
            embed = discord.Embed(title="You Were Caught!", description="You were caught and paid your victim <:KoffeeKoin:939562780363726868> **500**")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed)


    @app_commands.command(name="deposit", description="Deposit money into your bank account")  # deposit command
    @app_commands.describe(amount="Enter an amount, or use max/all to deposit all your money")
    async def dep(self, interaction: discord.Interaction, amount: str):
        sql = ''
        val = 0

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from wallets WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()

        if result[1] == 0:
            embed = discord.Embed(title="Out of Money", description="You don't have any money to deposit")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        done = False
        amount = str(amount)
        if str(amount) == "all" or str(amount) == "max":
            sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (result[2] + result[1], interaction.user.id)
            await interaction.response.send_message(
                f"Successfully deposited <:KoffeeKoin:939562780363726868> **{'{:,}'.format(result[1])}** into your bank account")
            remove_bal(interaction.user, result[1])
            done = True
        if not done:
            try:
                amount = int(amount)
                assert amount > 0

            except AssertionError:
                embed = discord.Embed(title="Negative Amount",
                                      description="You can not deposit a negative amount",
                                      color=discord.Color.blue())
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            except ValueError:
                embed = discord.Embed(title="Value Error", description="Maybe try typing an actual number!")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if result[1] < amount:
                await interaction.response.send_message(
                    f"You cannot deposit more than <:KoffeeKoin:939562780363726868> **{'{:,}'.format(result[1])}**")
                return

            sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (result[2] + amount, interaction.user.id)
            remove_bal(interaction.user, amount)

            embed = discord.Embed(title="Bank",
                                  description=f"Successfully deposited <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** into your bank account",
                                  color=discord.Color.blue())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            embed.set_footer(text="You can /deposit max|all to deposit all your money immediately")
            await interaction.response.send_message(embed=embed)

        cursor.execute(sql, val)
        db.commit()

    @app_commands.command(name='scam', description="Scam people for their money")  # scam command
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def scam(self, interaction: discord.Interaction):
        chance = [1, 2, 3]
        amount = random.randrange(500, 2000)

        if chance == 2:
            desc = "You went scamming and came home empty handed :("
        else:
            desc = f"You scammed some guy for <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}**"
            add_bal(interaction.user, amount)

        embed = discord.Embed(title="Scam", description=desc)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="withdraw", description="Withdraw from your bank account into your wallet")  # withdraw money command
    @app_commands.describe(amount="The amount of money you wish to withdraw")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        sql = ''
        val = 0

        open_wallet(user=interaction.user)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()

        if int(amount) < 0:
            embed = discord.Embed(title="Negative values", description="You can not use negative values!")
            await interaction.response.send_message(embed=embed)
            return

        amount = str(amount)
        if result[2] == 0:
            embed = discord.Embed(title="Out of Money", description="You dont have any money in your bank :|")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        done = False

        if str(amount) == "max" or str(amount) == "all":
            amount = result[2]
            await interaction.response.send_message(
                f"Successfully withdrawn <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from your bank account")
            sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
            val = (0, interaction.user.id)

            add_bal(interaction.user, result[2])
            done = True

        if not done:
            try:
                amount = int(amount)
                assert amount > 0

            except AssertionError:
                embed = discord.Embed(title="Negative Amount", description="You can not deposit a negative amount")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            except ValueError:
                embed = discord.Embed(title="Value Error", description="Maybe try typing an actual number!")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if int(amount) > result[2]:
                desc = "You cannot withdraw an amount bigger than your bank balance :|"
                ephemeral = True
            else:
                desc = f"Successfully withdrawn <:KoffeeKoin:939562780363726868> **{'{:,}'.format(amount)}** from your bank account"
                ephemeral = False

                sql = "UPDATE wallets SET bank = ? WHERE member_id = ?"
                val = (result[2] - amount, interaction.user.id)
                add_bal(interaction.user, amount)

            embed = discord.Embed(title="Withdraw", description=desc, color=discord.Color.blue())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @app_commands.command(name="recipes", description="Displays all current recipes to craft items")
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    async def recipes(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Recipes', color=discord.Color.blue())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='craft', description="Craft an item")
    @app_commands.describe(item="The item you wish to craft", amount="The amount of items you wish to craft")
    @app_commands.choices(item=[
        Choice(name="Common Coffee", value="ccoffee"),
        Choice(name="Rare Coffee", value="rcoffee"),
        Choice(name="Tea", value="tea")])
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    async def craft(self, interaction: discord.Interaction, item: str, amount: int = 1):
        user = interaction.user
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {user.id}")
        result = cursor.fetchone()

        hasEnough = []

        if amount < 0:
            embed = discord.Embed(title="Negative values", description="You can not use negative values!")
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(title="Insuffiecient items", description="You do not have enough items to craft this item")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')

        if item == recipeList[0]:  # ccoffee
            for x in range(len(ccoffeeRecipeAmount)):
                if result[x + 1] >= ccoffeeRecipeAmount[x] * amount:
                    hasEnough.append(x)
            if len(hasEnough) == len(ccoffeeRecipeAmount):
                await interaction.response.send_message(f"You've crafted {amount} `common coffee`")
                add_crafted_item(user, amount, item, 1)
                remove_item(user, 1 * amount, itemID[0], 0)
                remove_item(user, 3 * amount, itemID[1], 1)
                remove_item(user, 1 * amount, itemID[2], 2)
                remove_item(user, 2 * amount, itemID[4], 4)
                remove_item(user, 1 * amount, itemID[5], 5)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)

        elif item == recipeList[1]:  # rcoffee
            for x in range(len(rcoffeeRecipeAmount)):
                if result[x + 1] >= rcoffeeRecipeAmount[x] * amount:
                    hasEnough.append(x)
            if len(hasEnough) == len(rcoffeeRecipeAmount):
                await interaction.response.send_message(f"You've crafted {amount} `rare coffee`")
                add_crafted_item(user, amount, item, 2)
                remove_item(user, 1 * amount, itemID[0], 0)
                remove_item(user, 7 * amount, itemID[1], 1)
                remove_item(user, 1 * amount, itemID[3], 3)
                remove_item(user, 3 * amount, itemID[4], 4)
                remove_item(user, 1 * amount, itemID[6], 6)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)

        elif item == recipeList[2]:  # tea
            for x in range(len(teaRecipeAmount)):
                if result[x + 1] >= teaRecipeAmount[x] * amount:
                    hasEnough.append(x)
            if len(hasEnough) == len(teaRecipeAmount):
                await interaction.response.send_message(f"You've crafted {amount} `tea`")
                add_crafted_item(user, amount, item, 3)
                remove_item(user, 1 * amount, itemID[0], 0)
                remove_item(user, 1 * amount, itemID[2], 2)
                remove_item(user, 3 * amount, itemID[4], 4)
                remove_item(user, 1 * amount, itemID[5], 5)
                remove_item(user, 1 * amount, itemID[7], 7)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Item does not exist", description="That is not a craftable item")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='shop', description="Opens up the KoffeeBot shop")
    @app_commands.choices(page=[
        Choice(name="Page 1", value=1),
        Choice(name="Page 2", value=2)])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shop(self, interaction: discord.Interaction, page: int):
        if page == 1:
            embed = discord.Embed(title='Koffee Mart', color=discord.Color.blue())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')

            embed.add_field(name="<:mug:950689993867788338> *mug:*  <:KoffeeKoin:939562780363726868> **5,000**",
                            value="ID: `mug`",
                            inline=False)
            embed.add_field(name="<:coffee_bean:951551479989301338> *coffee bean:* <:KoffeeKoin:939562780363726868> **1,500**",
                            value="ID: `bean`",
                            inline=False)
            embed.add_field(name=":milk: *milk:*  <:KoffeeKoin:939562780363726868> **10,000**",
                            value="ID: `milk`",
                            inline=False)
            embed.add_field(name="<:sugar:951066869304029214> *sugar:*  <:KoffeeKoin:939562780363726868> **2,500**",
                            value="ID: `sugar`",
                            inline=False)
            embed.add_field(name=":spoon: *spoon:*  <:KoffeeKoin:939562780363726868> **1,000**",
                            value="ID: `spoon`",
                            inline=False)
            embed.set_footer(text='Page 1/2')
            await interaction.response.send_message(embed=embed)

        if page == 2:
            embed = discord.Embed(title='Koffee Mart', color=discord.Color.blue())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')

            embed.add_field(name="<:gspoon:951731109312479243> *golden spoon:*  <:KoffeeKoin:939562780363726868> **15,000**",
                            value="ID: `gspoon`",
                            inline=False)
            embed.add_field(name="<:pmilk:951741856264368128> *premium milk:*  <:KoffeeKoin:939562780363726868> **50,000**",
                            value="ID: `pmilk`",
                            inline=False)
            embed.add_field(name="<:teabag:957760498902900806> teabag <:KoffeeKoin:939562780363726868> **5,000**",
                            value="ID: `teabag`",
                            inline=False)
            embed.set_footer(text='Page 2/2')
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name='buy', description="Buy an item from the KoffeeBot shop")  # buy command
    @app_commands.describe(item="The item you wish to purchase", amount="The amount of items you wish to purchase")
    @app_commands.choices(item=[
        Choice(name="Mug", value="mug"),
        Choice(name="Coffee Beans", value="bean"),
        Choice(name="Milk", value="milk"),
        Choice(name="Premium Milk", value="pmilk"),
        Choice(name="Sugar", value="sugar"),
        Choice(name="Spoon", value="spoon"),
        Choice(name="Golden Spoon", value="gspoon"),
        Choice(name="Tea Bag", value="teabag")])
    async def buy(self, interaction: discord.Interaction, item: str, amount: int = 1):

        if amount <= 0:
            embed = discord.Embed(title="Invalid Amount", description="Please enter a positive number for the amount.",
                                  color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
            return

        user = interaction.user
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {user.id}")
        result = cursor.fetchone()

        for i in range(len(itemID)):
            if item == itemID[i]:
                title = "Purchase Successful"
                desc = f"Purchased {amount} `{itemID[i]}` for <:KoffeeKoin:939562780363726868>** {'{:,}'.format(itemvalue[i] * amount)}**"

                error = False
                if itemvalue[i] * amount > result[1]:
                    title = "Insufficient Funds"
                    desc = f"You do not have enough <:KoffeeKoin:939562780363726868> in your wallet to make this purchase"
                    error = True

                embed = discord.Embed(title=title, description=desc, color=discord.Color.blue())
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                await interaction.response.send_message(embed=embed)

                if not error:
                    remove_bal(interaction.user, itemvalue[i] * amount)
                    add_item(interaction.user, amount, item, i)
                    break

    @app_commands.command(name='sell', description="Sell an item")  # sell command
    @app_commands.describe(item="The item you wish to sell", amount="The amount of items you wish to sell")
    @app_commands.choices(item=[
        Choice(name="Mug", value="mug"),
        Choice(name="Coffee Beans", value="bean"),
        Choice(name="Milk", value="milk"),
        Choice(name="Premium Milk", value="pmilk"),
        Choice(name="Sugar", value="sugar"),
        Choice(name="Spoon", value="spoon"),
        Choice(name="Golden Spoon", value="gspoon"),
        Choice(name="Tea Bag", value="teabag")])
    async def sell(self, interaction: discord.Interaction, item: str, amount: int = 1):
        user = interaction.user
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients WHERE member_id = {user.id}")
        result = cursor.fetchone()

        for i in range(len(itemID)):
            if item == itemID[i]:
                title = "Selling"
                desc = f"Sold {amount} `{itemID[i]}` for <:KoffeeKoin:939562780363726868>**{'{:,}'.format(round((itemvalue[i] * amount / 2)))}**"

                error = False
                if result[i + 1] == 0:
                    desc = "You do not own this item!"
                    error = True
                if int(amount) > int(result[i + 1]):
                    desc = "You cannot sell more items than you have in your inventory!"
                    error = True

                embed = discord.Embed(title=title, description=desc, color=discord.Color.blue())
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                await interaction.response.send_message(embed=embed)

                if not error:
                    add_bal(interaction.user, round(itemvalue[i] * amount / 2))
                    remove_item(interaction.user, amount, item, i)
                    break

    @app_commands.command(name='inventory', description="Opens up your inventory")  # inventory command
    @app_commands.describe(user="The user who's inventory you wish to view")
    @app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id, i.user.id))
    async def inventory(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ingredients INNER JOIN recipes USING (member_id) WHERE member_id = {user.id}")
        result = cursor.fetchone()
        all_items = itemID + recipeList

        print(result)

        embed = discord.Embed(title=f"{user.name}'s inventory", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar)
        inven = []

        for i in range(len(all_items)):
            if result[i + 1] != 0:
                inven.append(i)

        print(inven)
        for i in inven:
            embed.add_field(name=f"{itemlist[i]}  {result[i + 1]}", value=f"ID: `{all_items[i]}`",
                            inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='joblist', description="Shows all current available jobs")  # job list
    async def joblist(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Current available jobs",
                              description="```/job to select a job\n"
                                          "/work to start working\n"
                                          "/resign to quit your current job```",
                              color=discord.Color.blue())

        embed.set_thumbnail(url=interaction.guild.icon)
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

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="job", description="Apply to a job type") # assign a new job
    @app_commands.choices(job=[
        Choice(name="Babysitter", value="babysitter"),
        Choice(name="Teacher", value="teacher"),
        Choice(name="Accountant", value="accountant"),
        Choice(name="Programmer", value="programmer"),
        Choice(name="Lawyer", value="lawyer")])
    async def job(self, interaction: discord.Interaction, job: str):

        open_wallet(user=interaction.user)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM wallets INNER JOIN recipes USING (member_id) WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()

        result_iter = [6, 4, 4, 5, 5]
        joblist = ['babysitter', 'teacher', 'accountant', 'programmer', 'lawyer']
        needed_item = ["<:tea:959165836042588250> `tea`", "☕ `ccoffee`", "☕ `ccoffee`",
                       "<:rare_coffee:951551480215789658> `rcoffee`", "<:rare_coffee:951551480215789658> `rcoffee`"]

        for i, jobtype in enumerate(joblist):
            if job == jobtype:
                if result[3] != 'unemployed':
                    await interaction.response.send_message('You already have a job!')
                    return

                if result[result_iter[i]] < 1:
                    await interaction.response.send_message(f"You need to craft at least 1 {needed_item[i]} to qualify for this job")
                    return
                else:
                    update_job(interaction.user, job)
                    embed = discord.Embed(title="Jobs", description=f"Your jobtitle is now: **{jobtype}**. Use `/work` to start working")
                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
                    await interaction.response.send_message(embed=embed)
                    return

    @app_commands.command(name='work', description="Start working at your job")  # work command
    @app_commands.checks.dynamic_cooldown(work_cooldown)
    async def work(self, interaction: discord.Interaction):

        open_wallet(user=interaction.user)
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets INNER JOIN recipes USING (member_id) WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()

        joblist = ['babysitter', 'teacher', 'accountant', 'programmer', 'lawyer']
        craft_list = ["tea", "ccoffee", "ccoffee", "rcoffee", "rcoffee"]
        remove_pos = [3, 1, 1, 2, 2]
        needed_item = ["<:tea:959165836042588250> `tea`", "☕ `ccoffee`", "☕ `ccoffee`",
                       "<:rare_coffee:951551480215789658> `rcoffee`", "<:rare_coffee:951551480215789658> `rcoffee`"]

        salary = [5000, 8000, 10000, 15000, 15000]
        fire_chance = random.randint(1, 20)
        tired_chance = random.randint(1, 20)

        if result[3] == 'unemployed':
            embed = discord.Embed(title="Unemployed", description="You are currently unemployed. Use `/joblist` to look for a job")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            await interaction.response.send_message(embed=embed)
            app_commands.Cooldown.reset(work_cd)
            return

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
                    for x, jobtype in enumerate(joblist):
                        if result[3] == jobtype:
                            await interaction.response.send_message(
                                f"You have used up all your {needed_item[x]}. Without it you cannot work\n"
                                "You will need to craft a new form of energy and start looking for a job again")
                            update_job(interaction.user, 'unemployed')
                            remove_crafted_item(interaction.user, 1, craft_list[x], remove_pos[x])
                            self.client.get_command("work").reset_cooldown(interaction)
                            return

                if fire_chance == 19:
                    await interaction.response.send_message(random.choice(fire))
                    update_job(interaction.user, 'unemployed')
                    return
                else:
                    add_bal(interaction.user, salary[i])
                    await interaction.response.send_message(random.choice(outcomes))
                    return

    @app_commands.command(name='resign', description="Quit your job") # quit current job
    async def resign(self, interaction: discord.Interaction):
        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets WHERE member_id = {interaction.user.id}")
        result = cursor.fetchone()

        if result[3] == 'unemployed':
            desc = "You are already unemployed"
        else:
            desc = "You have quit your current job...you will need to wait an hour before choosing a new job"
            update_job(interaction.user, 'unemployed')

        embed = discord.Embed(title="Resign?", description=desc)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='daily', description="Receive your daily amount of money")  # daily command
    @app_commands.checks.cooldown(1, 86400.0, key=lambda i: (i.guild_id, i.user.id))
    async def daily(self, interaction: discord.Interaction):
        open_wallet(user=interaction.user)
        daily_amount = 25000
        await interaction.response.send_message(
            f"You have recieved your daily amount of <:KoffeeKoin:939562780363726868> **{'{:,}'.format(daily_amount)}**")
        add_bal(interaction.user, daily_amount)

    @app_commands.command(name='lucky', description="Is it your lucky day?")  # lucky command
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def lucky(self, interaction: discord.Interaction):
        open_wallet(user=interaction.user)
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
            desc = random.choice(lucks)
            add_bal(interaction.user, luck_money)
        elif rand_int == 3:
            desc = f"Oh look! You found {item_quantity} `{random_item}`"
            add_item(interaction.user, item_quantity, random_item, random_items.index(random_item) + 1)
        else:
            desc = "You're not feeling particularly lucky today"

        embed = discord.Embed(title="Lucky", description=desc)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='slots', description="The AMAZING slot machine!")  # slot machine commands
    @app_commands.describe(amount="The amount of money you wish to bet. Minimum 500 required")
    @app_commands.checks.dynamic_cooldown(slots_cooldown)
    async def slots(self, interaction: discord.Interaction, amount: int):
        outcomes = [":banana:", ":cherries:", ":candy:"]
        one = random.choice(outcomes)
        two = random.choice(outcomes)
        three = random.choice(outcomes)
        win = int(amount) * 7
        lose = ["Tough luck :(", "Rip your money lol", "Oof!"]

        if amount < 500:
            app_commands.Cooldown.reset(slots_cd)
            await interaction.response.send_message("You need at least "
            "<:KoffeeKoin:939562780363726868> **500** in your wallet to use the slot machine", ephemeral=True)
            return

        result = check_bal_greater_than(user=interaction.user, amount=amount)
        if result is False:
            app_commands.Cooldown.reset(slots_cd)
            await interaction.response.send_message("Your amount cannot be greater than your wallet :|", ephemeral=True)
            return

        em1 = discord.Embed(title="=-=-=-=-=-=\n"
                                  ":red_square: :red_square: :red_square: :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.blue())
        em1.set_author(name="Slot machine", icon_url=interaction.user.avatar)
        em2 = discord.Embed(title=f"=-=-=-=-=-=\n"
                                  f"{one} :red_square: :red_square: :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.blue())
        em2.set_author(name="Slot machine", icon_url=interaction.user.avatar)
        em3 = discord.Embed(title=f"=-=-=-=-=-=\n"
                                  f"{one} {two} :red_square: :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.blue())
        em3.set_author(name="Slot machine", icon_url=interaction.user.avatar)
        em4 = discord.Embed(title=f"=-=-=-=-=-=\n"
                                  f"{one} {two} {three} :round_pushpin:\n"
                                  "=-=-=-=-=-=", color=discord.Color.blue())
        em4.set_author(name="Slot machine", icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=em1)
        await interaction.edit_original_response(embed=em2)
        await interaction.edit_original_response(embed=em3)
        await interaction.edit_original_response(embed=em4)

        if one == two == three:
            add_bal(interaction.user, win - amount)
            embed = discord.Embed(
                description=f"Congratulations!!! {interaction.user.mention}\nYou won <:KoffeeKoin:939562780363726868> **{'{:,}'.format(win)}**!",
                color=discord.Color.blue())
            embed.set_author(name="Slot machine", icon_url=interaction.user.avatar)
            await interaction.followup.send(embed=embed)
        else:
            remove_bal(interaction.user, amount)
            embed = discord.Embed(description=random.choice(lose), color=discord.Color.blue())
            embed.set_author(name="Slot machine", icon_url=interaction.user.avatar)
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="leaderboard", description="Shows the top 10 Richest KoffeeBot users")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()

        db = sqlite3.connect('kof_db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM wallets ORDER BY bank DESC")
        result = cursor.fetchall()

        guild = interaction.user.guild
        top_10 = []

        for db_user in result:
            for member in guild.members:
                if member.id == db_user[0]:
                    user = await self.client.fetch_user(member.id)
                    top_10.append(user)
            if len(top_10) == 10:
                break

        if len(top_10) < 10:
            await interaction.response.send_message("At least 10 people in this server need a "
                "KoffeeBot account/balance\nYou can open an account by using `/balance`")
            return

        cursor.execute(
            f"SELECT * FROM wallets WHERE member_id IN "
            f"({top_10[0].id},{top_10[1].id},{top_10[2].id},"
            f"{top_10[3].id},{top_10[4].id},{top_10[5].id},"
            f"{top_10[6].id},{top_10[7].id},{top_10[8].id},"
            f"{top_10[9].id}) ORDER BY bank DESC")
        result = cursor.fetchall()

        embed = discord.Embed(title=f"Top 10 Richest people in {guild}", color=discord.Color.blue())
        embed.add_field(name="Member <:rare_coffee:951551480215789658>", value='\n'.join(f"**{i+1})** {user.name}" for i, user in enumerate(top_10)), inline=True)
        embed.add_field(name="> Money <:KoffeeKoin:939562780363726868>", value='\n'.join(f"> {'{:,}'.format(result[i][1] + result[i][2])}" for i in range(len(top_10))), inline=True)
        embed.set_thumbnail(url=interaction.guild.icon)

        await interaction.followup.send(embed=embed)


    # @app_commands.command(name="profile", description="Display your KoffeeBot profile")
    # @app_commands.describe(member="The user whose profile you wish to view")
    # async def profile(self, interaction: discord.Interaction, member: discord.Member = None):
    #     if member is None:
    #         member = interaction.user
    #
    #     name, nick, id, status = str(member), member.display_name, str(member.id), str(member.status).upper()


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id == 979427519742759002:
            data = message.content.split(" ")
            user = re.sub("\D", "", data[0])

            user_object = self.client.get_user(int(user)) or await self.client.fetch_user(int(user))
            user = user_object
            open_wallet(user)
            add_bal(user, 25000)

            embed = discord.Embed(title="KoffeeBot Vote Rewards", color=discord.Color.blue())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/922909643053871175/1088540971421159454/koffee.png')
            embed.add_field(name="Thank you for voting for me :D",
                            value=f"You have received <:KoffeeKoin:939562780363726868>**25,000**")
            await user_object.send(embed=embed)
            await self.client.process_commands(message)


async def setup(client):
    await client.add_cog(Economy(client))
