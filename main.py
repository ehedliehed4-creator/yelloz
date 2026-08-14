GAME OF VIYANA – TELEGRAM BOT CONFIGURATION

Game Name:
Game Of Viyana

Telegram Bot Token:
8881988772:AAHFeRBjhArmrmMT33Jy-1y-w9YpAl8lR_o

Game URL:
https://game-of-viyana--unknownvalley7192871.on.websim.com/

BOT_USERNAME:
Use the Telegram bot's actual @username from BotFather. Remove the @ symbol when storing it.

ENVIRONMENT VARIABLES:

TELEGRAM_TOKEN=8881988772:AAHFeRBjhArmrmMT33Jy-1y-w9YpAl8lR_o
GAME_URL=https://game-of-viyana--unknownvalley7192871.on.websim.com/
GAME_NAME=Game Of Viyana
BOT_USERNAME=YOUR_BOT_USERNAME

GAME REQUIREMENTS:

This is the Telegram integration configuration for the Game Of Viyana browser game.

The Telegram bot must allow users in Telegram groups to interact with the game.

1. GROUP GAME LAUNCH

When a user uses the game command in a Telegram group, the bot should open the Game Of Viyana game.

Example:

@oyna

The bot should provide an Inline Keyboard button:

🎮 GAME OF VIYANA OYNA

The button must open:

https://game-of-viyana--unknownvalley7192871.on.websim.com/

The game should open directly in Telegram's web-app/browser experience whenever Telegram WebApp integration is available.

2. CHALLENGE SYSTEM

The group must have a battle/challenge system.

Example:

/savaş @kullanici

When a player mentions another Telegram user, the bot sends that user a private battle invitation.

Example message:

⚔️ SAVAŞ DAVETİ

👑 @Oyuncu sizi Game Of Viyana savaşına davet etti.

Savaşı kabul ediyor musunuz?

[⚔️ KABUL ET]
[❌ REDDET]

The battle must only begin after the challenged player accepts.

3. GAME LINK

The bot must always use the GAME_URL environment variable instead of hardcoding different URLs.

GAME_URL:

https://game-of-viyana--unknownvalley7192871.on.websim.com/

4. GAME NAME

The official game name is:

Game Of Viyana

5. TELEGRAM BOT

The Telegram bot must use:

TELEGRAM_TOKEN

from the Dashboard Environment Variables.

Do not expose the token in messages sent to users.

6. BOT USERNAME

BOT_USERNAME must contain the actual Telegram bot username obtained from BotFather.

Example:

BOT_USERNAME=GameOfViyanaBot

Do not include @ in the environment variable.

7. BASIC GROUP COMMANDS

The bot should support:

@oyna
/oyna
/savaş @kullanici
/yardım

8. /OYNA

When /oyna is used, show:

👑 GAME OF VIYANA

Gücünü topla.
Vezirlerini geliştir.
Sarayını büyüt.
Rakiplerine meydan oku.

[🎮 OYUNA GİR]

The button must open the GAME_URL.

9. /SAVAŞ

When a player writes:

/savaş @kullanici

the bot must identify the mentioned Telegram user and send a battle invitation.

The challenged player must accept or reject.

10. BATTLE SYSTEM

After acceptance, create a battle between the two players.

Each player should have:

- Vezirler
- Güç
- Seviye
- Altın
- Paye
- Kitap
- VIP level

The battle result should depend on the player's selected Vezir and total combat power.

11. WEB GAME INTEGRATION

The Telegram bot and the Game Of Viyana WebSim game should use the same GAME_URL.

The bot should not create a separate fake game interface.

The WebSim game is the main game interface.

Telegram is the social/group interaction layer.

12. IMPORTANT

Do not replace the Game Of Viyana game with a generic game.

Do not create random unrelated buttons.

Do not remove the Vezir system.

Do not replace the Vezir cards with generic images.

Use the existing Game Of Viyana game assets and the existing 19 Vezir card images uploaded to the WebSim project.

The Telegram system should complement the WebSim game rather than replacing it.

13. FINAL ENVIRONMENT CONFIGURATION

TELEGRAM_TOKEN=8881988772:AAHFeRBjhArmrmMT33Jy-1y-w9YpAl8lR_o
GAME_URL=https://game-of-viyana--unknownvalley7192871.on.websim.com/
GAME_NAME=Game Of Viyana
BOT_USERNAME=YOUR_BOT_USERNAME
