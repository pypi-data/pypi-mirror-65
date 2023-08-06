from .OutputSpeech import OutputSpeech
from .Card import Card
from .Image import Image


class Alexa(dict):
    """
    Request:
    {
      "version": "1.0",
      "session": {
        "new": true,
        "sessionId": "amzn1.echo-api.session.[unique-value-here]",
        "application": {
          "applicationId": "amzn1.ask.skill.[unique-value-here]"
        },
        "attributes": {
          "key": "string value"
        },
        "user": {
          "userId": "amzn1.ask.account.[unique-value-here]",
          "accessToken": "Atza|AAAAAAAA...",
          "permissions": {
            "consentToken": "ZZZZZZZ..."
          }
        }
      },
      "context": {
        "System": {
          "device": {
            "deviceId": "string",
            "supportedInterfaces": {
              "AudioPlayer": {}
            }
          },
          "application": {
            "applicationId": "amzn1.ask.skill.[unique-value-here]"
          },
          "user": {
            "userId": "amzn1.ask.account.[unique-value-here]",
            "accessToken": "Atza|AAAAAAAA...",
            "permissions": {
              "consentToken": "ZZZZZZZ..."
            }
          },
          "apiEndpoint": "https://api.amazonalexa.com",
          "apiAccessToken": "AxThk..."
        },
        "AudioPlayer": {
          "playerActivity": "PLAYING",
          "token": "audioplayer-token",
          "offsetInMilliseconds": 0
        }
      },
      "request": {LaunchRequest/IntentRequest/SessionEndedRequest}
    }

    type LaunchRequest:

    {
      "type": "LaunchRequest",
      "requestId": "string",
      "timestamp": "string",
      "locale": "string"
    }

    type IntentRequest:
    {
      "type": "IntentRequest",
      "requestId": "string",
      "timestamp": "string",
      "dialogState": "string",
      "locale": "string",
      "intent": {
        "name": "string",
        "confirmationStatus": "string",
        "slots": {
          "SlotName": {
            "name": "string",
            "value": "string",
            "confirmationStatus": "string",
            "resolutions": {
              "resolutionsPerAuthority": [
                {
                  "authority": "string",
                  "status": {
                    "code": "string"
                  },
                  "values": [
                    {
                      "value": {
                        "name": "string",
                        "id": "string"
                      }
                    }
                  ]
                }
              ]
            }
          }
        }
      }
    }

    type SessionEndedRequest:

    {
      "type": "SessionEndedRequest",
      "requestId": "string",
      "timestamp": "string",
      "reason": "string",
      "locale": "string",
      "error": {# TODO set request_object
        "type": "string",
        "message": "string"
      }
    }

    Response:
    {
      "version": "string",
      "sessionAttributes": {
        "key": "value"
      },
      "response": {
        "outputSpeech": alexaoutputspeechobject,
        "card": AlexaCardObject,
        "reprompt": {
          "outputSpeech": AlexaOutputSpeechObject
        },
        "directives": [
          {
            "type": "InterfaceName.Directive"
            (...properties depend on the directive type)
          }
        ],
        "shouldEndSession": true
      }
    }

    """

    def __init__(self, request_data_json: dict) -> None:
        super().__init__()

        self._session_id = None
        self._result = None
        self._parameters = None
        self._action = None
        self._message = ''
        self._message_dict = None
        self._intent_type = None

        self._parameters = {}

        self.load_request_data(request_data_json)

    def load_request_data(self, request_data_json: dict):

        assert isinstance(request_data_json, dict)

        print('request_data_json: ', request_data_json)

        self._session_id = request_data_json.get('session').get('sessionId')
        print('session_id : ', self._session_id)

        self['sessionAttributes'] = request_data_json.get('session').get('attributes')
        print('session_attributes: ', self['sessionAttributes'])

        self._intent_type = request_data_json.get('request').get('type')
        print('intent_type: ', self._intent_type)

        if self._intent_type == 'LaunchRequest':
            self._action = 'Welcome'
            print('action: ', self._action)

        elif self._intent_type == 'IntentRequest':
            self._action = request_data_json.get('request').get('intent').get('name')
            print('action: ', self._action)

            if self['sessionAttributes'] is not None:
                self._parameters.update(self['sessionAttributes'])

            slots = request_data_json.get('request').get('intent').get('slots')
            print('slots: ', slots)

            if slots is not None:
                for slot in slots.values():
                    print('slot: ', slot)

                    resolution = slot.get('resolutions')
                    if resolution is not None:
                        resolutions_per_authority = resolution.get('resolutions_per_authority')
                        print('resolutions_per_authority: ', resolutions_per_authority)

                        values = resolutions_per_authority[0].get('values')
                        print('values: ', values)

                        if values is not None:
                            parameter_value = values[0].get('value').get('name')
                        else:
                            parameter_value = resolution.get('resolutions_per_authority')[0].get('value')
                        parameter_name = slot.get('name')
                        self._parameters[parameter_name] = parameter_value

            print('parameters: ', self._parameters)

        elif self._intent_type == 'SessionEndedRequest':
            self._action = 'Quit'
            print('action: ', self._action)

        # response objects
        self['version'] = '1.0'
        self['sessionAttributes'] = dict()
        self['card'] = dict()
        self['outputSpeech'] = dict()
        self['directives'] = list()
        self['shouldEndSession'] = False

    @property
    def parameters(self):
        return self._parameters

    @property
    def action(self):
        return self._action

    @property
    def session_id(self):
        return self._session_id

    @property
    def version(self) -> str:
        return self['version']

    @version.setter
    def version(self, value: str):
        assert isinstance(value, str)
        self['version'] = value

    @property
    def session_attributes(self) -> dict:
        return self['sessionAttributes']

    def add_session_attributes(self, **kwargs) -> bool:
        self['sessionAttributes'].update(kwargs)
        return True

    def delete_session_attributes(self, *keys) -> bool:

        if len(keys) == 0:
            self['sessionAttributes'].clear()

        else:
            for key in keys:
                assert isinstance(key, str)
                del self['sessionAttributes'][key]

        return True

    @property
    def output_speech(self) -> OutputSpeech:
        return self['outputSpeech']

    def add_plain_text_response(self, text: str) -> OutputSpeech:
        assert isinstance(text, str)
        self['outputSpeech'] = OutputSpeech(speech_type='PlainText', text=text)
        return self['outputSpeech']

    def add_ssml_response(self, ssml: str) -> OutputSpeech:
        assert isinstance(ssml, str)
        self['outputSpeech'] = OutputSpeech(speech_type='SSML', ssml=ssml)
        return self['outputSpeech']

    @property
    def card(self) -> Card:
        return self['card']

    def add_account_link_card(self) -> Card:
        self['card'] = Card(card_type='LinkAccount')
        return self['card']

    def add_simple_card(self, title: str, content: str) -> Card:
        assert isinstance(title, str)
        assert isinstance(content, str)
        self['card'] = Card(card_type='Simple', title=title, content=content)
        return self['card']

    def add_standard_card(self, title: str, text: str, small_image_url: str, large_image_url: str) -> Card:
        assert isinstance(title, str)
        assert isinstance(text, str)
        assert isinstance(small_image_url, str)
        assert isinstance(large_image_url, str)
        self['card'] = Card(
            card_type='Standard',
            title=title, text=text,
            image=Image(
                small_image_url=small_image_url,
                large_image_url=large_image_url
            )
        )

        return self['card']

    @property
    def reprompt(self) -> OutputSpeech:
        return self['outputSpeech']

    def add_plain_text_reprompt(self, text: str) -> OutputSpeech:
        assert isinstance(text, str)
        self['outputSpeech'] = OutputSpeech(speech_type='PlainText', text=text)
        return self['outputSpeech']

    def add_ssml_reprompt(self, ssml: str) -> OutputSpeech:
        assert isinstance(ssml, str)
        self['outputSpeech'] = OutputSpeech(speech_type='SSML', ssml=ssml)
        return self['outputSpeech']

    @property
    def directives(self) -> list:
        return self['directives']

    def add_directives(self, *args) -> bool:
        self['directives'].extend(args)

        return True

    def delete_directives(self, *args) -> bool:
        for item in args:
            self['directives'].remove(item)

        return True

    @property
    def end_session_flag(self) -> bool:
        return self['shouldEndSession']

    @end_session_flag.setter
    def end_session_flag(self, value: bool):
        assert isinstance(value, bool)
        self['shouldEndSession'] = value

    def end_session(self) -> bool:
        self['shouldEndSession'] = True

        return True

    def continue_session(self) -> bool:
        self['shouldEndSession'] = False

        return True
