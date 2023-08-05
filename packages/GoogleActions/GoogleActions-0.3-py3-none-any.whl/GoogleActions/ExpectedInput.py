from typing import List
from .InputPrompt import InputPrompt
from .ExpectedIntent import ExpectedIntent
from .RichResponse import RichResponse


class ExpectedInput(dict):
    """
    {
      "inputPrompt": {
        object(InputPrompt)
      },
      "possibleIntents": [
        {
          object(ExpectedIntent)
        }
      ],
      "speechBiasingHints": [
        string
      ],
    }
    """

    def __init__(self, speech_biasing_hints_list: List[str] = None, input_prompt: InputPrompt = None,
                 possible_intents_list: List[ExpectedIntent] = None):
        super().__init__()

        if speech_biasing_hints_list is not None:
            self['speechBiasingHints'] = speech_biasing_hints_list

        if input_prompt is not None:
            self['inputPrompt'] = input_prompt

        if possible_intents_list is not None:
            self['possibleIntents'] = possible_intents_list

    def add_speech_biasing_hint(self, speech_biasing_hints: str) -> List[str]:
        for item in speech_biasing_hints:
            assert isinstance(item, str)
            self['speechBiasingHints'].append(item)

        return self['speechBiasingHints']

    def add_possible_intent(self, possible_intents: ExpectedIntent) -> List[ExpectedIntent]:
        for item in possible_intents:
            assert isinstance(item, ExpectedIntent)
            self['possibleIntents'].append(item)

        return self['possibleIntents']

    def add_input_prompt(self, rich_initial_prompt: RichResponse = None, no_input_prompts: InputPrompt = None) -> \
            InputPrompt:
        if no_input_prompts is None:
            no_input_prompts = []
        self['inputPrompt'] = InputPrompt(rich_initial_prompt=rich_initial_prompt, no_input_prompts=no_input_prompts)
        return self['inputPrompt']
