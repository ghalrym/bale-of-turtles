from mini_tortoise_tts import TextToSpeech, safe_load_voice

from .mini_turtle_component import use_state, MiniTurtleComponent


class MiniTortoiseTTSComponent(MiniTurtleComponent):

    def __init__(self, voice: str):
        super().__init__()
        self.tts = TextToSpeech(safe_load_voice(voice))

    @use_state("mini-tortoise-tts-say", ["mini_tortoise_tts_say"])
    def say(self, mini_tortoise_tts_say: str):
        audio = self.tts.generate(mini_tortoise_tts_say)
