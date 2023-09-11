from utilities.input_handler import InputHandler
from typing import List


class ScenarioDataContainer:
    input_handler: InputHandler
    outputs_to_verify: List

    def __init__(self):
        self.outputs_to_verify = []
        self.input_handler = InputHandler()
