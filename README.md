# Escordia - Open RPG System

Escordia is a free and open RPG system made from scratch and built with Python. The project was originally based on a Discord bot I programmed in 2021/2022 and aims to provide an open system to build RPG Discord Bots with Python.

![rpg_icon](https://user-images.githubusercontent.com/75074498/233842763-3ad5c2fe-106e-41f0-b7a7-cf98d3abc7d1.png)

## Project Overview

Escordia is currently capable of:
- Creating and keeping track of RPG characters made by users. These characters have their own stats, inventory, job, skills, etc.
- Managing concurrent battles and dungeons.
- Divide a map in areas, each area having different enemies, items and dungeons.
- Managing a ton of items with different stat alterations that characters can equip.
- Managing skills that both player and enemies can use in combat.
- Having a complex job system in which each job has its own skills, preferred weapons, experience, level and requisites.
- In-game shops that vary depending on the character's current area.
- Destroying user's items at choice in order to exchange them for permanent stat upgrades.
- Managing buffs and debuffs while in combat.
- Managing an element system in skills in order to strike enemies' weaknesses/resistances.
- Uses a graphical interface so that commands are very rarely used 
- Define a vast amount of custom data (items, enemies, skills, classes) in a simple JSON.

Escordia stores static data such as enemies, items, and more on JSON files, while dynamic data such as players, inventories, and more is stored in a database using Peewee.

### Screenshots

![imagen](https://github.com/rodmarkun/Escordia-RPG-System/assets/75074498/aed01a79-31ce-4948-8c46-065fab7fc51c)

![imagen](https://github.com/rodmarkun/Escordia-RPG-System/assets/75074498/94fd0b67-4eb4-4ddc-84a5-968ee8f81435)

![imagen](https://github.com/rodmarkun/Escordia-RPG-System/assets/75074498/c914b0a1-af7f-4cf9-9a2a-3a3baa8cb291)

![imagen](https://github.com/rodmarkun/Escordia-RPG-System/assets/75074498/6c675ec7-cff9-4511-94a9-be0f900fdf0a)

![imagen](https://github.com/rodmarkun/Escordia-RPG-System/assets/75074498/227fe1eb-554e-49d7-be29-54fe13de7129)


## Usage

Please follow the next steps to have your own instance of Escordia running on your machine. It is an easy process though it may take some time specially if you are not used to setting up these kind of projects.

### Discord Bot Creation

1. Go to the Applications tab in the [Discord Developer Portal](https://discord.com/developers/applications) and sign in with your account.
2. Create a new application, giving it a name. 
3. Inside your new application, go into the "Bot" tab. Next to your bot's icon, click "Reset Token" so that a new token for your bot is generated. Copy this token somewhere (it will be used later) and **do not sare it with anyone**.
4. Inside "Authoritation Flow" decide if you want to make this a public or private bot. It does not affect Escordia's behaviour.
5. In "Privileged Gateway Intents" make sure all three intent options are **checked**. After that, save your changes.
6. In the "OAuth2" tab, go to "URL Generator". On the "Scopes" menu check "Bot". On the "Bot Permissions" menu check those that are checked in the image below. You can also just give the bot Administrator privileges, although it is not recommended.
7. Paste the generated URL in your browser and invite the bot to your server. 

After all of these steps, you can configure the rest of your bot as your liking. Next, we will see how to install Escordia RPG itself and link it to our new bot.

### Installation

1. Download and install [Python](https://www.python.org/downloads/) >= 3.9 (Using latest available version is recommended). Make sure python.exe is added to PATH.
2. Clone the repository `git clone https://github.com/rodmarkun/Escordia-RPG-System`
3. Once in the project directory, open a terminal and install all necessary dependencies with the following command: `python -m pip install -r ".\requirements.txt"`. If it does not work, try using `python3` instead of `python`.
4. Now, to link it to the bot we previously created you must create a new environment variable in your system with "DISCORD_TOKEN" as the name and the token we generated as the value.
5. As we have updated a system environment variable, you will have to restart all terminals or IDEs you had open for the changes to take effect.
6. Finally, to start Escordia just run the "discord_manager.py" file. You can do this in a terminal by running `python .\discord_manager.py`.

Your Escordia bot is now operative, however, there is a problem: **icons**. Escordia RPG uses custom icons and Discord does not allow bots to use emojis from servers where they are not members. Here is an easy way to provide your bot with the necessary icons:

### Icons

![imagen](https://github.com/rodmarkun/Escordia-RPG-System/assets/75074498/e5e058d7-35ea-4f79-b183-6b92121a5415)

1. Go to this [link](https://drive.google.com/drive/folders/18oyUzsanpRc2wnVHo3bQ-Y1o2SZZBP9S?usp=sharing) and download the "EscordiaIcons" folder.
2. Add all the icons to your Discord server. Do it in batches, as Discord can limit your speed when uploading too many icons. You can use any random server you own, the bot will be able to use it on all servers he's a member of.
3. Copy and paste the following message in any text channel in the Discord server where you uploaded the icons. An eror may pop up, do not worry about it.

```python
{
  "GoldIcon": "\:GoldIcon:",
  "EssenceIcon": "\:EssenceIcon:",
  "DungeonIcon": "\:DungeonIcon:",
  "SwordIcon": "\:SwordIcon:",
  "DaggerIcon": "\:DaggerIcon:",
  "AxeIcon": "\:AxeIcon:",
  "BowIcon": "\:BowIcon:",
  "StaffIcon": "\:StaffIcon:",
  "ScytheIcon": "\:ScytheIcon:",
  "HammerIcon": "\:HammerIcon:",
  "BookIcon": "\:BookIcon:",
  "ScepterIcon": "\:ScepterIcon:",
  "KatanaIcon": "\:KatanaIcon:",
  "PhysHelmIcon": "\:PhysHelmIcon:",
  "MagicHelmIcon": "\:MagicHelmIcon:",
  "HeavyArmorIcon": "\:HeavyArmorIcon:",
  "LightArmorIcon": "\:LightArmorIcon:",
  "MagicArmorIcon": "\:MagicArmorIcon:",
  "AccesoryIcon": "\:AccesoryIcon:",
  "FireIcon": "\:FireIcon:",
  "IceIcon": "\:IceIcon:",
  "ThunderIcon": "\:ThunderIcon:",
  "WindIcon": "\:WindIcon:",
  "HolyIcon": "\:HolyIcon:",
  "DarkIcon": "\:DarkIcon:",
  "AtkDownIcon": "\:AtkDownIcon:",
  "AtkUpIcon": "\:AtkUpIcon:",
  "DefDownIcon": "\:DefDownIcon:",
  "DefUpIcon": "\:DefUpIcon:",
  "MatDownIcon": "\:MatDownIcon:",
  "MatUpIcon": "\:MatUpIcon:",
  "MdfDownIcon": "\:MdfDownIcon:",
  "MdfUpIcon": "\:MdfUpIcon:",
  "LukDownIcon": "\:LukDownIcon:",
  "LukUpIcon": "\:LukUpIcon:",
  "NoviceIcon": "\:NoviceIcon:",
  "WarriorIcon": "\:WarriorIcon:",
  "RogueIcon": "\:RogueIcon:",
  "MageIcon": "\:MageIcon:",
  "HunterIcon": "\:HunterIcon:",
  "WarlockIcon": "\:WarlockIcon:",
  "GladiatorIcon": "\:GladiatorIcon:",
  "ClericIcon": "\:ClericIcon:"
}
```

4. Copy your message after sending it (see that now every entry has some numbers at the end? Those are the ID of your icons in your server).
5. Paste the whole result in the `.\emojis.py` file, replacing the empty brackets in the `ICON_DICT = ...` definition.

After that, you will finally have your own Escordia RPG instance in your machine. You can begin your journey by typing `!start`. Have fun!

## Contributing

Contributions are always welcome! If you're interested in contributing to Escordia, please fork the repository and create a new branch for your changes. When you're done with your changes, submit a pull request to merge your changes into the main branch.

## Supporting Escordia

If you want to support Escordia RPG, you can:
- **Star** :star: the project in Github!
- **Donate** :coin: to my [Ko-fi](https://ko-fi.com/rodmarkun) page!
- **Share** :heart: the project with your friends!

## Credits

Escordia RPG has been originally created and developed by **rodmarkun** in order to provide a free, customizable and fun RPG experience for Discord users. This project uses free assets from Ækashics (Ækashics Librarium), Lorc, Delapouite, and Viscious Speed (Boxes-Be-Gone Icon Set), Lorc -again- (700 RPG Icons). Also I am currently unable to find where I got the item and buff/debuff icons from, if someone knows please contact me so I can give proper credit.
