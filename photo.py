import io
import numpy as np
from PIL import Image
import cv2
from ultralytics import YOLO
from telegram import Update
from telegram.ext import ContextTypes

yolo = YOLO("yolov8n.pt")


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
        await msg.reply_text(
            "She really tried her best, but she couldn’t find any objects here. "
            "Let’s try another pic! Maybe second time’s the charm?"
        )
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
        cv2.putText(
            draw,
            txt,
            (x1 + 2, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2
        )

        out = Image.fromarray(draw)
        bio = io.BytesIO()
        out.save(bio, format="JPEG", quality=90)
        bio.seek(0)
        await msg.reply_photo(photo=bio, caption="Best detection")
