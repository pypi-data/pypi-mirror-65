from typing import List
from .RichResponse import RichResponse
from .SimpleResponse import SimpleResponse


class InputPrompt(dict):
    """
    Input Prompt

    class for Google
    {
      "richInitialPrompt": {
        object(RichResponse)
      },
      "noInputPrompts": [
        {
          object(SimpleResponse)
        }
      ],
    }
    """

    def __init__(self, rich_initial_prompt: RichResponse = None, no_input_prompts: List[SimpleResponse] = None):
        super().__init__()
        if no_input_prompts is None:
            no_input_prompts = []

        self['noInputPrompts'] = []

        self['noInputPrompts'] = no_input_prompts
        self['richInitialPrompt'] = rich_initial_prompt

    def add_rich_initial_prompt(self) -> RichResponse:
        self['richInitialPrompt'] = RichResponse()
        return self['richInitialPrompt']

    def add_no_input_prompts(self, no_input_prompts: SimpleResponse) -> List[SimpleResponse]:
        for item in no_input_prompts:
            assert isinstance(item, SimpleResponse)
            self['noInputPrompts'].append(item)

        return self['noInputPrompts']

    def add_no_input_prompt(self, text_to_speech: str = '', ssml: str = '',
                            display_text: str = '') -> SimpleResponse:
        no_input_prompt = SimpleResponse(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text)
        self['noInputPrompts'].append(no_input_prompt)

        return no_input_prompt
