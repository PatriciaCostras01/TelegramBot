from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import sqlite3
from restrictions import setup_restrictions
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
        await msg.reply_text("Send a photo and she’ll try her best to recognize what’s inside!")
        return

    tg_file = await context.bot.get_file(file_id)
    img_bytes = await tg_file.download_as_bytearray()
    pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = np.array(pil)

    results = yolo.predict(img, conf=0.25, verbose=False)
    r = results[0]
    names = r.names

    if r.boxes is None or len(r.boxes) == 0:
        await msg.reply_text("She really tried her best, but she couldn’t find any objects here. Let’s try another pic! Maybe second time’s the charm?")
        return

    dets = []
    for b, c, s in zip(
        r.boxes.xyxy.cpu().numpy(),
        r.boxes.cls.cpu().numpy(),
        r.boxes.conf.cpu().numpy()
    ):
        dets.append((names[int(c)], float(s), b.astype(int)))

    dets.sort(key=lambda x: x[1], reverse=True)
    best_label, best_score, best_box = dets[0]

    percent = best_score * 100
    await msg.reply_text(
        f"I think this is a **{best_label}** "
        f"(confidence: {best_score:.2f} ≈ {percent:.0f}%).",
        parse_mode="Markdown"
    )

    if annotate:
        x1, y1, x2, y2 = best_box
        draw = img.copy()
        cv2.rectangle(draw, (x1, y1), (x2, y2), (0, 255, 0), 2)
        txt = f"{best_label} {best_score:.2f}"
        (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(draw, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 255, 0), -1)
        cv2.putText(draw, txt, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        out = Image.fromarray(draw)
        bio = io.BytesIO()
        out.save(bio, format="JPEG", quality=90)
        bio.seek(0)
        await msg.reply_photo(photo=bio, caption="Best detection")

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

    await msg.reply_text("📝 SugarGlitter secretly indexed this message for search~ ✨")


async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(
            "✨ SugarGlitter needs a search term, sweet friend!\n"
            "Try `/search <word>` or use `/searchwords` for a magical guided search~ 💖",
            parse_mode="Markdown"
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
            f"🌸 Aww… SugarGlitter couldn’t find anything containing *'{query}'*.\n"
            "Maybe try another sparkly keyword? ✨",
            parse_mode="Markdown"
        )
        return

    result = "\n\n".join(
        f"• @{(r['username'] or 'user')} (# {r['message_id']}):\n{r['text'][:400]}"
        for r in rows
    )
    await update.message.reply_text(
        f"💖✨ SugarGlitter found some glittery matches for *'{query}'*:\n\n{result}",
        parse_mode="Markdown"
    )


async def search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌈✨ What magical thing would you like SugarGlitter to search for? 💖"
    )
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
        await update.message.reply_text(
            f"💗 SugarGlitter found no sparkles for *'{query}'*.\n"
            "Try another magical word? ✨",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    result = "\n\n".join(
        f"• @{(r['username'] or 'user')} (# {r['message_id']}):\n{r['text'][:400]}"
        for r in rows
    )

    await update.message.reply_text(
        f"🎀✨ Here are SugarGlitter’s glittery results for *'{query}'*:\n\n{result}",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def search_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 Oh, the search was cancelled~ SugarGlitter will sparkle again whenever you need her! 💖"
    )
    return ConversationHandler.END



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 Hiii! SugarGlitter just sprinkled into the chat! ✨💖\n"
        "Use /help to see all the magical things I can do! 🎀"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💖✨ *SugarGlitter Command Menu* ✨💖\n\n"
        "🍬 /start – Wake up this girls SugarGlitter and begin the magic\n"
        "🌸 /help – Show this sweet little guide\n"
        "🎀 /youtube – A sparkly doorway to YouTube\n"
        "💗 /linkedin – Your professional glitter profile\n"
        "💌 /gmail – Your shiny Gmail link\n"
        "📚 /geeks – A nerdy sprinkle of GeeksforGeeks\n\n"
        
        "🔎✨ *Search Spells:* ✨🔍\n"
        "💎 /search <term> – Instantly search messages (e.g. `/search grey car`)\n"
        "🌈 /searchwords – SugarGlitter asks you what to search for\n"
        "🍭 /cancel – Cancel the current search enchantment\n\n"

        "🖼️💫 *Image Magic:* 💫🖼️\n"
        "Send SugarGlitter a photo and she’ll try her best to recognize what’s inside!\n"
        "✨ (people, cars, pets, objects… and everything sparkly) ✨",
        parse_mode="Markdown"
    )


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
        f"🍬 *'{update.message.text}'* isn’t in SugarGlitter’s candy jar of commands! Try /help for something yummy! 💗",
        parse_mode="Markdown"
    )


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🧁 Aww… *'{update.message.text}'* doesn’t make much sense to SugarGlitter. "
        f"Try something a bit clearer? 💗",
        parse_mode="Markdown"
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

    setup_restrictions(app)

    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))

    app.run_polling()




if __name__ == "__main__":
    main()
