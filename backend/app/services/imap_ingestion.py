import email
import imaplib
import os
from typing import List

from app.core.config import settings
from app.db.session import SessionLocal


def download_attachments_to_folder() -> List[str]:
    """
    Connects to IMAP and downloads CSV attachments into DATA_FOLDER.
    This is generic; you configure IMAP_* in .env.
    """

    if not settings.IMAP_HOST or not settings.IMAP_USERNAME or not settings.IMAP_PASSWORD:
        raise RuntimeError("IMAP settings are not configured")

    mail = imaplib.IMAP4_SSL(settings.IMAP_HOST, settings.IMAP_PORT)
    mail.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
    mail.select(settings.IMAP_FOLDER)

    # Search all unseen messages with attachments (simple version)
    typ, msg_nums = mail.search(None, "UNSEEN")
    if typ != "OK":
        return []

    saved_files: List[str] = []
    data_folder = settings.DATA_FOLDER
    os.makedirs(data_folder, exist_ok=True)

    for num in msg_nums[0].split():
        typ, msg_data = mail.fetch(num, "(RFC822)")
        if typ != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if not filename:
                    continue
                if not filename.lower().endswith(".csv"):
                    continue

                path = os.path.join(data_folder, filename)
                with open(path, "wb") as f:
                    f.write(part.get_payload(decode=True))
                saved_files.append(path)

    mail.logout()
    return saved_files


def run_imap_ingestion():
    """
    Download CSVs from IMAP and ingest them using the same folder pipeline.
    """
    saved = download_attachments_to_folder()
    if not saved:
        return {"downloaded": 0, "processed": []}

    db = SessionLocal()
    try:
        result = ingest_from_folder(db)
    finally:
        db.close()

    return {
        "downloaded": len(saved),
        "processed": result.get("processed", []),
    }
