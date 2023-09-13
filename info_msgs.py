import emojis

HELP_MSG = f"{emojis.SPARKLER_EMOJI} **--- GENERAL ---** {emojis.SPARKLER_EMOJI}\n" \
            "`!start` - Creates a new character\n" \
            "`!tutorial` - Shows the tutorial\n" \
            "`!help` - Shows all commands\n" \
            f"{emojis.CHARACTER_EMOJI} **--- PLAYER ---** {emojis.CHARACTER_EMOJI}\n" \
            "`!profile` - Shows player info\n" \
            "`!rest` - Recover all your HP/MP\n" \
            "`!skills` - See details about your current skills\n" \
            "`!equipment` - Shows player equipment\n" \
            "`!shop` - See the shop of your current area\n" \
            f"{emojis.ESC_SWORD_ICON} **--- COMBAT ---** {emojis.ESC_SWORD_ICON}\n" \
            "`!fight` - Search the area for an enemy\n" \
            "`!dungeon` - See all dungeons in your current area\n" \
            "`!job` - See details about your current job or change it\n" \
            "`!boss` - Fight against the boss of this area\n" \

TUTORIAL_MSG = f"Hello traveller! Welcome to __Escordia RPG__!\n\nHere, you can **fight** diverse enemies in your current **area**, earning gold and XP. You can acquire new **equipment** in the **shop** or in challenging **dungeons**. If you are pretty wounded, take care of yourself **resting**. While fighting, remember to check for enemy **weaknesses** and exploit them!\n\n" \
                "As you gain XP, you will advance in your current **job**, adquiring new **skills**. You can unlock new jobs by completing their requirements! Check them out! Once you really feel strong, head for the **boss** of the area in order to go to the next one!\n\n" \
                "--> __You can play the whole game just by entering the command__ `!menu` :) <--"

ESSENCE_MSG = f"You can destroy items for essence {emojis.ESC_ESSENCE_ICON}. You can spend your essence on permanent blessings. When destroying an item, you destroy all copies of that item in your inventory. The amount of essence you get depends on the item's rarity and quantity destroyed."
PVP_MSG = f"Welcome to the Escordia Arena! Here you can fight other players in a 1v1 battle. There are no prizes other than honor and glory. To duel someone, use `!duel [their character name]`."
CREDITS = "**CREDITS**\nThis project uses free assets from **Ækashics** (Ækashics Librarium), **Lorc**, **Delapouite**, and **Viscious Speed**"\
           " (Boxes-Be-Gone Icon Set), **Lorc** -again- (700 RPG Icons). Also I am currently unable to find where I got the item and buff/debuff icons from, if someone knows please contact me so I can give proper credit."
SUPPORT = f"**SUPPORT**\nIf you want to support the development of Escordia RPG, you can:\n- **Star** {emojis.SPARKLER_EMOJI} in Github! (https://github.com/rodmarkun/Escordia-RPG-System).\n- **Donate** {emojis.ESC_GOLD_ICON} to my Ko-fi page! (https://ko-fi.com/rodmarkun)\n- **Share** {emojis.HEART_EMOJI} the project with your friends!\n\nThank you!"
ABOUT_MSG = f"\n**ABOUT ESCORDIA RPG**\nEscordia RPG is a Discord RPG Bot System originally created by **rodmarkun** in order to provide a free, customizable and fun RPG experience for Discord users. The bot is currently under development and I do not have much free time, so please be patient for updates.\n\n" \
            f"{CREDITS}\n\n{SUPPORT}"
