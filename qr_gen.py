import secrets
import qrcode

data = secrets.token_hex(100)
print(data)
img = qrcode.make(data)
img.save("user1.png")