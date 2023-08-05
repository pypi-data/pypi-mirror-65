import requests
import json
import logging
import uuid
import base64
from urllib.parse import urljoin

#from robot.api import logger
#from robot.libraries.BuiltIn import BuiltIn
#from robot.utils.asserts import assert_equal
#from robot.api.deco import keyword

class ATPKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self, atpUrl, imageProcessor='local', relayAtpUrl='http://localhost:9090/'):

        self._atpUrl = atpUrl
        self._imageProcessor = imageProcessor
        self._relayAtpUrl = relayAtpUrl

        if self._imageProcessor == 'relay':
            pingResponse = self._call(self._getRelayAtpUrl('v3'), 'performPing')
            if pingResponse['Successful'] == False:
                raise Exception('Relay ATP instance not available!')

    def _getAtpUrl(self, version='v3'):
        return urljoin(self._atpUrl, 'ATP/' + version)

    def _getRelayAtpUrl(self, version='v3'):
        return urljoin(self._relayAtpUrl, 'ATP/' + version)

    def _validateResponse(self, response, result=True, errors=True):

        try:
            logging.debug('ATP:validateResponse')
            logging.debug(json.dumps(response, indent=4))

            if result == True:
                if response['result']:
                    assert response['result'], 'Invalid ATP Response'
                    assert response['result']['Successful'] == True, 'ATP Response was not successful'
                    assert response['result']['Result'], 'ATP Response has no result'
                    if errors == True:
                        assert len(response['result']['Errors']) == 0, 'ATP Response contains errors'
                else:
                    assert response != None, 'Invalid ATP Response'
            if response['result']:        
                return response['result']
            else:
                return response
        except Exception as error:
            logging.error(error)
            assert error, error

    def _call(self, url, method, params=[{}], validateResult=True, validateErrors=True):
        try:
            logging.debug('ATP:call ' + method + ' @ ' + url)

            payload = {
                "method": method,
                "params": params,
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4())
            }

            response = requests.post(url, json=payload)

            logging.debug(response.text)
            
            return self._validateResponse(response.json(), validateResult, validateErrors)
        except Exception as error:
            logging.error(error)

    def atp_ping(self):
        """ ATP Ping: Pings ATP server """
        return self._call(self._getAtpUrl('v3'), 'performPing',[{}], True)

    def atp_kill(self):
        """ ATP Kill: Kills ATP server """
        return self._call(self._getAtpUrl('v2'), 'kill', [], False)

    def atp_delay(self, duration):
        """ ATP Delay: Delays X milliseconds """
        return self._call(self._getAtpUrl('v2'), 'delay', [duration], False)

    def atp_take_screen_capture(self):
        """ ATP Take Screen Capture: Takes Screen capture on ATP server """
        return self._call(self._getAtpUrl('v2'), 'takeScreenCapture',[], True)

    def atp_save_screen_capture(self, filename):
        """ ATP Save Screen Capture: Takes and Saves screen capture from ATP server to file """
        response = self.atp_take_screen_capture()
        data = base64.b64decode(response['Result'])
        with open(filename, 'wb') as f:
            f.write(data)

    def _read_image(self, filename):
        with open(filename, "rb") as imgFile:
            imgBytes = imgFile.read()

        base64Bytes = base64.b64encode(imgBytes).decode('utf-8')
        return str(base64Bytes)

    def atp_find_image_in(self, findImage, targetImage):
        """ ATP Find Image In: Finds image inside another image """

        findInPayload = {
            "tolerance": 0.95,
            "findText": None,
            "findImage": findImage,
            "targetImage": targetImage
        }

        if self._imageProcessor == 'relay':
            return self._call(self._getRelayAtpUrl('v3'), 'performFindImageIn',[findInPayload], True)
        else:
            return self._call(self._getAtpUrl('v3'), 'performFindImageIn', [findInPayload], True)

    def atp_click(self, filename):
        """ ATP Click: Mouse moves and clicks where an image is found """
        targetResponse = self.atp_take_screen_capture()
        logging.debug('Target: ' + targetResponse['Result'])

        imageData = self._read_image(filename)
        logging.debug('Find: ' + imageData)

        findImage = {
            "imageData": imageData,
            "imagePath": filename
        }

        targetImage = {
            "imageData": targetResponse['Result']
        }

        findImageInResponse = self.atp_find_image_in(findImage, targetImage)
        match = findImageInResponse['Result']['Matches'][0]

        clickPayload = {
            "clickOffset": str(match['x'] + int(match['width'] / 2)) + ',' + str(match['y'] + int(match['height'] / 2)),
            "clickType": "LEFTSINGLE"
        }

        clickResponse = self._call(self._getAtpUrl('v3'), 'performClick', [clickPayload], True)
        return clickResponse
