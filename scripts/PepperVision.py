"""
Provide the image acquired from pepper's camera on a url for using it to do emotion recognition
"""

from flask import Flask, Response, render_template,  url_for
from naoqi import ALProxy
import vision_definitions
import time
import io
from PIL import Image

IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT

REST_PORT = 5000 

app = Flask(__name__)

video_srv = ALProxy("ALVideoDevice", IP_ADD, PORT)

if video_srv.getSubscribers():
    for subscriber in video_srv.getSubscribers():
        if "CameraStream" in subscriber:  # name passed as argument on subscription
            video_srv.unsubscribe(subscriber)

resolution = vision_definitions.kQVGA
colorSpace = vision_definitions.kRGBColorSpace
imgClient = video_srv.subscribe("CameraStream", resolution, colorSpace,30)

@app.route("/pepper_view")
def pepper_view():
    return render_template("camera.html")

@app.route("/pepper_video")
def pepper_video():
    return Response(
        stream_generator(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
     )

def alImage_to_PIL(alImg):
    """
    Converts a ALImage from the naoqi API ALVideoDeviceProxy::getImageRemote.
    :param alImg: The ALimage object as returned from the API.
    :return: A Pillow image.
    """
    im_w = alImg[0]
    im_h = alImg[1]
    im_arr = alImg[6]

    im_str = str(bytearray(im_arr))
    pil_img = Image.frombytes("RGB", (im_w, im_h), im_str)

    return pil_img

def PIL_to_JPEG_BYTEARRAY(pil_img):
    """
    Converts a Pillow image to a JPEG bytearray
    :param pil_img: The pillow image object
    :return: TThe jpeg bytearray
    """
    imgByteArr = io.BytesIO()
    pil_img.save(imgByteArr, format="jpeg")
    jpeg_bytes = imgByteArr.getvalue()

    return jpeg_bytes

def stream_generator():
    while True:
        alImage = video_srv.getImageRemote(imgClient)
        if alImage is not None:
            pil_img = alImage_to_PIL(alImage)
            jpeg_bytes = PIL_to_JPEG_BYTEARRAY(pil_img)
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n\r\n')
        time.sleep(0.01)


app.run(host='127.0.0.1', port = REST_PORT)