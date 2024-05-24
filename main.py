import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw
import requests

def add_rounded_corners(image, radius):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
    rounded_image = Image.new("RGB", image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

def get_bitcoin_value(value):
    url = f"https://blockchain.info/tobtc?currency=USD&value={value}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Failed to fetch data. Status code: {response.status_code}"

def main():
    value = input("Enter Bitcoin value in USD: ")
    bitcoin_value = get_bitcoin_value(value)
    bitcoin_address = input("Enter Your Bitcoin Address: ")
    
    qr = qrcode.QRCode(version=3, box_size=20, border=0, error_correction=qrcode.constants.ERROR_CORRECT_H)
    data = f"bitcoin:{bitcoin_address}?amount={bitcoin_value}&label=<label>&message=<message>"
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
    
    border_size = 10
    radius = 30
    new_size = (img_qr.size[0] + 2 * border_size, img_qr.size[1] + 2 * border_size)
    img_with_border = Image.new("RGB", new_size, "white")
    img_with_border.paste(img_qr, (border_size, border_size))
    img_with_rounded_corners = add_rounded_corners(img_with_border, radius)
    img_with_rounded_corners.save("QR_CODE.png")
    
    print(f"Bitcoin value for ${value} USD: {bitcoin_value}")

if __name__ == "__main__":
    main()
