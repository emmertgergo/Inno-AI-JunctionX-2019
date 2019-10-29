from statistics_app.models import Result
from JunctionX.settings import BASE_DIR, STATIC_DIR
import time
from xml.etree import ElementTree
import requests
import json
import asyncio, io, glob, os, sys, time, uuid, requests
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
import azure.cognitiveservices.speech as speechsdk


def emotion_detction(result_id):
    KEY = "subscription_key"
    ENDPOINT = "https://facetestfirsttry.cognitiveservices.azure.com/face/v1.0/detect"
    result = Result.objects.get(pk=result_id)
    image_path = str(result.image.url)

    #image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': KEY}
    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'emotion',
    }
    response = requests.post(
        ENDPOINT, headers=headers, params=params, json={"url": image_path})
    response.raise_for_status()
    data = response.json()
    print(response)
    print(data)
    if data != []:
        emotion = data[0]['faceAttributes']['emotion']
        result.emotion_0 = emotion['anger']
        result.emotion_1 = emotion['contempt']
        result.emotion_2 = emotion['disgust']
        result.emotion_3 = emotion['fear']
        result.emotion_4 = emotion['happiness']
        result.emotion_5 = emotion['neutral']
        result.emotion_6 = emotion['sadness']
        result.emotion_7 = emotion['surprise']
        result.save()


class TextToSpeech(object):
    def __init__(self, subscription_key, text):
        self.subscription_key = subscription_key
        self.tts = text
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):

        fetch_token_url = "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        # https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken
        base_url = 'https://westeurope.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(STATIC_DIR + '/azure_app/voices/sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                      "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")


def text_to_speech(text):
    subscription_key = "subscription_key"
    app = TextToSpeech(subscription_key, text)
    app.get_token()
    app.save_audio()

