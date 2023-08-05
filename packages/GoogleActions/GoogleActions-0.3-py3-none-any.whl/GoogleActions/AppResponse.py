from typing import List
from .FinalResponse import FinalResponse
from .ExpectedInput import ExpectedInput
from .CustomPushMessage import CustomPushMessage
from .RichResponse import RichResponse
from .InputPrompt import InputPrompt
from .ExpectedIntent import ExpectedIntent
from .LinkOutSuggestion import LinkOutSuggestion
from .OrderUpdate import OrderUpdate
from .UserNotification import UserNotification
from .Target import Target


class AppResponse(dict):
    """
    {
      "conversationToken": string,
      "userStorage": string,
      "resetUserStorage": boolean,
      "expectUserResponse": boolean,
      "expectedInputs": [
        {
          object(ExpectedInput)
        }
      ],
      "finalResponse": {
        object(FinalResponse)
      },
      "customPushMessage": {
        object(CustomPushMessage)
      },
      "isInSandbox": boolean,
    }
    """

    def __init__(self, conversation_token=None, user_storage: str = '', reset_user_storage: bool = False,
                 expect_user_response: bool = True, final_response: FinalResponse = None, is_in_sandbox: bool = False,
                 custom_push_message: CustomPushMessage = None, expected_inputs: List[ExpectedInput] = None):

        super(AppResponse, self).__init__()

        if expected_inputs is None:
            expected_inputs = list()

        for item in expected_inputs:
            assert isinstance(item, ExpectedInput)
            self['expectedInputs'] = expected_inputs

        if final_response is not None:
            self['finalResponse'] = final_response

        if user_storage is not None:
            self['userStorage'] = user_storage

        self['resetUserStorage'] = reset_user_storage
        self['isInSandbox'] = is_in_sandbox
        self['expectUserResponse'] = expect_user_response

        if conversation_token is not None:
            self['conversationToken'] = conversation_token

        if custom_push_message is not None:
            self['customPushMessage'] = custom_push_message

    def add_expected_inputs(self, expected_inputs) -> List[ExpectedInput]:
        for item in expected_inputs:
            assert isinstance(item, ExpectedInput)
            self['expectedInputs'].append(item)

        return self['expectedInputs']

    def add_expected_input(self, speech_biasing_hints_list: List[str] = None, input_prompt: InputPrompt = None,
                           possible_intents_list: List[ExpectedIntent] = None) -> ExpectedInput:
        expected_input = ExpectedInput(speech_biasing_hints_list=speech_biasing_hints_list,
                                       input_prompt=input_prompt, possible_intents_list=possible_intents_list)
        self['expectedInputs'].append(expected_input)
        return expected_input

    def add_final_response(self, items_list: list = None, suggestions: list = None,
                           link_out_suggestion: LinkOutSuggestion = None) -> FinalResponse:
        self['finalResponse'] = FinalResponse(rich_response=RichResponse(item_list=items_list,
                                                                         suggestions=suggestions,
                                                                         link_out_suggestion=link_out_suggestion))
        return self['finalResponse']

    def add_custom_push_message(self, order_update: OrderUpdate = None, user_notification: UserNotification = None,
                                target: Target = None) -> CustomPushMessage:
        self['customPushMessage'] = CustomPushMessage(order_update=order_update,
                                                      user_notification=user_notification,
                                                      target=target)
        return self['customPushMessage']
