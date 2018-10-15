import json

from watson_developer_cloud import TextToSpeechV1
from django.http.response import HttpResponse
from django.http import JsonResponse
from watson_developer_cloud import WatsonApiException


class TextToSpeech(TextToSpeechV1):

    voice = "es-LA_SofiaVoice"
    format = 'audio/mp3'

    def __init__(self, *args, **kwargs):
        super(TextToSpeech, self).__init__(
            username='8fe4fd30-c3e2-48eb-90cc-d0f903c8155b',
            password='OTdxlPtfExmG',
            url='https://stream.watsonplatform.net/text-to-speech/api'
        )

    def getRawAudio(self, text, format='audio/mp3'):
        return self.synthesize(text, format, self.voice).content
    
    def processRequest(self, text, format='audio/mp3'):
        try:
            audioContent = self.getRawAudio(text)
            response = HttpResponse()
            response.write(audioContent)
            response['Content-Length'] = len(audioContent)
            response['Content-Type'] = format
        except WatsonApiException as ex:
            response = JsonResponse({
                    "message": "Method failed with status code " + str(ex.code) + ": " + ex.message
                })
            response.status_code = 500

        return response

text_to_specch = TextToSpeech()

# https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?accept=audio/wav&text=<prosody pitch="x-low">Lower pitch by 12 semitones from baseline</prosody>&voice=en-US_AllisonVoice

# <speak version="1.0">
#   <prosody pitch="-1500Hz">Transpose pitch to 1500 Hz</prosody>
#   <prosody pitch="-20Hz">Lower pitch by 20 Hz from baseline</prosody>
#   <prosody pitch="20Hz">Increase pitch by 20 Hz from baseline</prosody>
#   <prosody pitch="-12st">Lower pitch by 12 semitones from baseline</prosody>
#   <prosody pitch="x-low">Lower pitch by 12 semitones from baseline</prosody>
# </speak>