import qrcode
import uuid

def generate_qr(user_id: int) -> str:
    qr_id = str(uuid.uuid4())
    img = qrcode.make(qr_id)
    path = f"logs/{qr_id}.png"
    img.save(path)
    return qr_id, path
