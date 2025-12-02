import sqlite3
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from restrictions import classify_text, Severity, SEND_WARNINGS

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


async def index_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:
        return

    text = msg.text or ""

    severity = classify_text(text)

    if severity != Severity.OK:
        if SEND_WARNINGS:
            await msg.reply_text(
                "✨ Oopsie! SugarGlitter spotted a not-so-sweet word… "
                "let’s keep things sugar-friendly! 🍬"
            )
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
    await update.message.reply_text(
        "📝 SugarGlitter secretly indexes your sweet messages"
    )


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
