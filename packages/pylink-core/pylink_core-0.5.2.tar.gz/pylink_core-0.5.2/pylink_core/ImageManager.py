import base64, re, os
from PIL import Image
from io import BytesIO

def saveToBmp(fileIn,fileOut,width=None):
    if fileIn.startswith("data:image"):
        b64 = re.sub('^data:image/.+;base64,', '', fileIn)
        image_data = base64.b64decode(b64)
        img = Image.open(BytesIO(image_data))
    else:    
        img = Image.open(fileIn)
    img = img.convert("RGB")
    w, h = img.size
    if not width:
        width = w
    
    if h>128:
        hpercent = (128/h)
        w = int(w*hpercent)
        h = int(h*hpercent)

    width = int(width/8)*8 #align to 8pix
    if width > 160:
        width = 160
    wpercent = (width/float(w))
    hsize = int((float(h)*float(wpercent)))

    img = img.resize((width,hsize))
    img.save(fileOut)


if __name__ == "__main__":
    saveToBmp('test.jpg', 'test1.bmp')
    data = open('test.jpg', "rb").read()
    encoded = base64.b64encode(data)
    saveToBmp("data:image/jpeg;base64,"+encoded.decode(), 'test2.bmp')

