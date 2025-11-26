from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import sqlite3
from pathlib import Path
from telegram.ext import ConversationHandler
import os
from dotenv import load_dotenv
import io
import numpy as np
from PIL import Image
import cv2
from ultralytics import YOLO

yolo = YOLO("yolov8n.pt")

load_dotenv()

DB_PATH = Path("index.db")
ASK_QUERY = 1

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                chat_id INTEGER,
                message_id INTEGER,
                from_id INTEGER,
                username TEXT,
                text TEXT,
                created_at INTEGER,
                PRIMARY KEY (chat_id, message_id)
            )
        """)
        con.execute("CREATE INDEX IF NOT EXISTS idx_text ON messages(text)")
init_db()

async def analyze_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, annotate: bool = False):
    msg = update.effective_message

    file_id = None
    if msg.photo:
        file_id = msg.photo[-1].file_id 
    elif msg.document and msg.document.mime_type.startswith("image/"):
        file_id = msg.document.file_id
    else:
        await msg.reply_text("Send a photo and the bot will recognize objects in it.")
        return

    tg_file = await context.bot.get_file(file_id)
    img_bytes = await tg_file.download_as_bytearray()
    pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = np.array(pil)

    results = yolo.predict(img, conf=0.25, verbose=False)
    r = results[0]
    names = r.names

    if r.boxes is None or len(r.boxes) == 0:
        await msg.reply_text("I found nothing.")
        return

    dets = []
    for b, c, s in zip(r.boxes.xyxy.cpu().numpy(), r.boxes.cls.cpu().numpy(), r.boxes.conf.cpu().numpy()):
        dets.append((names[int(c)], float(s), b.astype(int)))
    dets.sort(key=lambda x: x[1], reverse=True)

    lines = [f"• {label} ({score:.2f})" for label, score, _ in dets[:10]]
    await msg.reply_text("I found:\n" + "\n".join(lines))

    if annotate:
        draw = img.copy()
        for label, score, (x1, y1, x2, y2) in dets:
            cv2.rectangle(draw, (x1, y1), (x2, y2), (0, 255, 0), 2)
            txt = f"{label} {score:.2f}"
            (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(draw, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 255, 0), -1)
            cv2.putText(draw, txt, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        out = Image.fromarray(draw)
        bio = io.BytesIO()
        out.save(bio, format="JPEG", quality=90)
        bio.seek(0)
        await msg.reply_photo(photo=bio, caption="Detecții anotate")


async def index_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:
        return
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT OR IGNORE INTO messages "
            "(chat_id, message_id, from_id, username, text, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                update.effective_chat.id,
                msg.message_id,
                (update.effective_user.id if update.effective_user else None),
                (update.effective_user.username if update.effective_user else None),
                msg.text,
                int(msg.date.timestamp()) if msg.date else None,
            ),
        )

async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(
            "Use /search <term> for direct search or /searchwords to start interactive mode."
        )
        return
    chat_id = update.effective_chat.id
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.execute(
            "SELECT message_id, username, text FROM messages "
            "WHERE chat_id=? AND lower(text) LIKE ? "
            "ORDER BY message_id DESC LIMIT 10",
            (chat_id, f"%{query.lower()}%"),
        )
        rows = cur.fetchall()
    if not rows:
        await update.message.reply_text(
            f"No messages found containing '{query}'.\n"
            "Remember: the bot can only search messages it has already seen."
        )
        return

    result = "\n\n".join(
        f"• @{(r['username'] or 'user')} (# {r['message_id']}):\n{r['text'][:400]}"
        for r in rows
    )
    await update.message.reply_text(f"Results for '{query}' (top 10):\n\n{result}")

async def search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What would you like to search for?")
    return ASK_QUERY

async def search_receive_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    chat_id = update.effective_chat.id
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.execute(
            "SELECT message_id, username, text FROM messages "
            "WHERE chat_id=? AND lower(text) LIKE ? "
            "ORDER BY message_id DESC LIMIT 10",
            (chat_id, f"%{query.lower()}%"),
        )
        rows = cur.fetchall()
    if not rows:
        await update.message.reply_text(f"No results found for '{query}'.")
        return ConversationHandler.END
    result = "\n\n".join(
        f"• @{(r['username'] or 'user')} (# {r['message_id']}):\n{r['text'][:400]}"
        for r in rows
    )
    await update.message.reply_text(f"Results for '{query}' (top 10):\n\n{result}")
    return ConversationHandler.END

async def search_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Search cancelled.")
    return ConversationHandler.END



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! /help to see available commands."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Available Commands:*\n\n"
        "/start  - Start the bot\n"
        "/help   - Show this help message\n"
        "/youtube - Get the YouTube link\n"
        "/linkedin - Get your LinkedIn profile URL\n"
        "/gmail  - Get the Gmail link\n"
        "/geeks  - Get the GeeksforGeeks URL\n"
        "🔎 *Search Features:*\n"
        "/search <term> - Search messages directly (e.g. `/search grey car`)\n"
        "/searchwords - Start interactive search mode (the bot asks what to search)\n"
        "/cancel - Cancel the current interactive flow\n\n"
        "🖼️ *Image Recognition:*\n"
        "Send a photo directly to the bot and it will recognize objects in it "
        "(e.g. person, car, dog, etc.)."
    , parse_mode="Markdown")


async def gmail_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your gmail link here (not sharing mine)")

async def youtube_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Youtube Link => https://www.youtube.com/")

async def linkedIn_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "LinkedIn URL => https://www.linkedin.com/in/username/"
    )

async def geeks_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "GeeksforGeeks URL => https://www.geeksforgeeks.org/"
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Sorry, '{update.message.text}' is not a valid command"
    )

async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Sorry, I can't recognize you. You said '{update.message.text}'"
    )

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ BOT_TOKEN not found in environment! Check your .env file.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("gmail", gmail_url))
    app.add_handler(CommandHandler("youtube", youtube_url))
    app.add_handler(CommandHandler("linkedin", linkedIn_url))
    app.add_handler(CommandHandler("geeks", geeks_url))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, analyze_photo))
    app.add_handler(CommandHandler("search", search_cmd))

    conv = ConversationHandler(
        entry_points=[CommandHandler("searchwords", search_start)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_receive_query)]
        },
        fallbacks=[CommandHandler("cancel", search_cancel)],
    )
    app.add_handler(conv)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, index_message))

    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))

    app.run_polling()



if __name__ == "__main__":
    main()
