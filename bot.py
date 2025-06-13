from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import asyncio 
from telegram.ext import ConversationHandler, MessageHandler, filters
import os 



ASKING_NAME = 1
GUESSING = 2
scoreboard = {}




# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data.get('name', 'Nathan')
    await update.message.reply_text(f"👋 Hello {name}! I'm alive and listening.")


# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here are some commands you can try:\n/start\n/help\n/about\n/joke")

# /about command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 I’m a bot coded by Nathan. Soon to be famous, don’t forget me.")

# /joke command
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Why don’t coders use dark mode?\nBecause light attracts bugs. 🐛")
    
async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_mood = context.args[0].lower()
        username = update.message.from_user.first_name

        context.user_data['name'] = username
        context.user_data['mood'] = user_mood

        if user_mood == "happy":
            reply = f"😊 I'm glad you're happy, {username}!"
        elif user_mood == "sad":
            reply = f"😢 It's okay, {username}. Tomorrow will be better."
        else:
            reply = f"🤔 I don't understand that mood, but I'm here for you, {username}!"
    else:
        reply = "Please tell me your mood. Example: /mood happy"

    await update.message.reply_text(reply)

  
qa_pairs = {
    "who created you": "Nathan built me from scratch, with code and love 💻❤️.",
    "what's your name": "I’m Nino, your personal AI bot!",
    "how are you": "Always active and ready to serve! 🤖",
    "what can you do": "I can chat, joke, motivate, remind, and more. Just ask me!",
}

async def echo_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower().strip(" ?.!")

    if "say hi" in user_message:
        await update.message.reply_text("Hello Nathan! 👋")
    elif "tell joke" in user_message:
        await update.message.reply_text("Why did the Python programmer go hungry?\nBecause his food was in a tuple and he couldn’t change it. 😂")
    elif "help" in user_message:
        await help_command(update, context)
    elif "about" in user_message:
        await about(update, context)
    else:
        answer = qa_pairs.get(user_message)
        if answer:
            await update.message.reply_text(answer)
        else:
            await update.message.reply_text(f"You said: {update.message.text}")



async def keyboard_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("👋 Say Hi"), KeyboardButton("🃏 Tell Joke")],
        [KeyboardButton("📖 Help"), KeyboardButton("ℹ️ About")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Here's your keyboard menu:", reply_markup=reply_markup)


quotes = [
    "Believe in yourself, even when no one else does.",
    "Pain is temporary, victory is forever.",
    "A lesson in every loss.",
    "You don’t grow when you’re comfortable.",
    "Power comes to those who train like monsters.",
    "Discipline beats motivation.",
    "You're already strong — become unstoppable."
]

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_quote = random.choice(quotes)
    await update.message.reply_text(f"🧠 Quote:\n\n{random_quote}")


qa_pairs = {
    "who created you": "Nathan built me from scratch, with code and love 💻❤️.",
    "what's your name": "I’m Nino, your personal AI bot!",
    "how are you": "Always active and ready to serve! 🤖",
    "what can you do": "I can chat, joke, motivate, remind, and more. Just ask me!",
}

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Say Hi", callback_data='say_hi'),
            InlineKeyboardButton("Tell Joke", callback_data='tell_joke'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    if query.data == 'say_hi':
        await query.edit_message_text(text="Hello again, Nathan! 👋")
    elif query.data == 'tell_joke':
        await query.edit_message_text(text="Why don’t coders use dark mode?\nBecause light attracts bugs. 🐛")
    else:
        await query.edit_message_text(text="Oops, I don't know that one.")


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        delay = int(context.args[0])
        message = ' '.join(context.args[1:])
        if not message:
            await update.message.reply_text("Please give a message after the time.")
            return
        await update.message.reply_text(f"⏳ Okay! I’ll remind you in {delay} seconds.")
        await asyncio.sleep(delay)
        await update.message.reply_text(f"⏰ Reminder: {message}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /remind <seconds> <message>")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data.get("name", "Unknown user")
    mood = context.user_data.get("mood", "not shared")
    await update.message.reply_text(f"🧠 Your saved data:\nName: {name}\nMood: {mood}")

async def setname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        name = ' '.join(context.args)
        context.user_data["name"] = name
        await update.message.reply_text(f"✅ Got it! I’ll call you {name} from now on.")
    else:
        await update.message.reply_text("Please give me a name. Example: /setname Nathan")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data.get("name", "Nathan")
    keyboard = [
        [
            InlineKeyboardButton("👋 Say Hi", callback_data='say_hi'),
            InlineKeyboardButton("🃏 Tell Joke", callback_data='tell_joke'),
        ],
        [
            InlineKeyboardButton("📖 Help", callback_data='help'),
            InlineKeyboardButton("ℹ️ About", callback_data='about'),
        ],
        [
            InlineKeyboardButton("🎯 Motivation", callback_data='quote'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Hi {name}, pick an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    name = context.user_data.get("name", "Nathan")

    if query.data == 'say_hi':
        await query.edit_message_text(text=f"Hey {name}! 👋")
    elif query.data == 'tell_joke':
        await query.edit_message_text(text="Why did the JavaScript developer leave?\nBecause he didn’t ‘null’ his feelings. 😅")
    elif query.data == 'help':
        await query.edit_message_text(text="/start\n/help\n/about\n/joke\n/menu")
    elif query.data == 'about':
        await query.edit_message_text(text="I'm your loyal bot, built by Nathan 💻.")
    elif query.data == 'quote':
        await query.edit_message_text(text=random.choice(quotes))
    else:
        await query.edit_message_text(text="❓ Unknown command.")

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! What should I call you? Please type your name.")
    return ASKING_NAME

async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data['name'] = name
    await update.message.reply_text(f"Got it! I’ll call you {name} from now on.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Okay, no worries! If you want to set your name later, just tell me.")
    return ConversationHandler.END


praises = [
    "{} you're unstoppable today! 🔥",
    "{} your brain is on another level. 🧠",
    "{} you code like a wizard! 🧙‍♂️",
    "{} you're the reason bots have self-esteem. 😎"
]

async def praise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = ' '.join(context.args) if context.args else context.user_data.get("name", "Nathan")
    compliment = random.choice(praises).format(name)
    await update.message.reply_text(compliment)

insults = [
    "{} your code runs… away from responsibility. 😂",
    "{} even semicolons are ashamed to be near your syntax. 🤡",
    "{} you debug like you’re in a horror movie—screaming and lost. 😭",
    "{} stop flexing that ‘Hello World’ program. It's been 3 days. 🥲"
]

async def insult(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = ' '.join(context.args) if context.args else context.user_data.get("name", "Nathan")
    roast = random.choice(insults).format(name)
    await update.message.reply_text(roast)

async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secret_number = random.randint(1, 10)
    context.user_data['secret_number'] = secret_number
    context.user_data['attempts'] = 0

    await update.message.reply_text("🎯 I'm thinking of a number between 1 and 10. You have 3 tries. Send your guess!")
    return GUESSING

async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number.")
        return GUESSING

    secret_number = context.user_data.get('secret_number')
    context.user_data['attempts'] += 1
    attempts = context.user_data['attempts']
    user_id = update.effective_user.id

    if user_guess == secret_number:
        context.user_data['games_played'] = context.user_data.get('games_played', 0) + 1
        context.user_data['games_won'] = context.user_data.get('games_won', 0) + 1
        scoreboard[user_id] = scoreboard.get(user_id, 0) + 1

        await update.message.reply_text(f"🎉 Correct! You win! The number was {secret_number}.")
        return ConversationHandler.END
    elif attempts >= 3:
        context.user_data['games_played'] = context.user_data.get('games_played', 0) + 1
        await update.message.reply_text(f"❌ Out of tries! The number was {secret_number}. Better luck next time!")
        return ConversationHandler.END
    else:
       hint = "📉 Too low!" if user_guess < secret_number else "📈 Too high!"
       await update.message.reply_text(f"{hint} You have {3 - attempts} tries left.")
       return GUESSING


async def show_scoreboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = scoreboard.get(user_id, 0)
    await update.message.reply_text(f"🏆 Your score: {score} correct guesses!")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        message = ' '.join(context.args)
        await update.message.reply_text("💬 Thanks for your feedback!")
        # You can also log or store it somewhere if needed
    else:
        await update.message.reply_text("Please provide your feedback after the command. Example: /feedback I love this bot!")


from aiohttp import web

async def handle(request):
    return web.Response(text="I’m alive, baby!")

app_web = web.Application()
app_web.add_routes([web.get('/', handle)])

def run_keep_alive():
    runner = web.AppRunner(app_web)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    loop.run_until_complete(site.start())

# Call this before app.run_polling()
run_keep_alive()

# Start the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token("7298826183:AAGyAFWoWFAxmVBJwPaipwskekTFHXftWwY").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("mood", mood))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("keyboard", keyboard_menu))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("setname", setname))
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('myname', ask_name)],
    states={
        ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("praise", praise))
    app.add_handler(CommandHandler("insult", insult))

    conv_game = ConversationHandler(
    entry_points=[CommandHandler("guess", guess_number)],
    states={GUESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess)]},
    fallbacks=[]
    )

    app.add_handler(conv_game)
    app.add_handler(CommandHandler("scoreboard", show_scoreboard))
    app.add_handler(CommandHandler("feedback", feedback))






    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_all))
    
    # Call this before app.run_polling()
    run_keep_alive() 
    print("Bot is running...")
    


    app.run_polling()

