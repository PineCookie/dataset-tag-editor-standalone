from typing import NamedTuple, get_type_hints
import gradio as gr
from .ui_common import *


class Params(NamedTuple):
    num_beams: int = 1
    num_beam_groups: int = 1
    do_sample: bool = False
    penalty_alpha: float = 0
    top_k: int = 50
    top_p: float = 1.0


presets: dict[str, tuple[Params, set[str]]] = {
    'custom': (Params(), set(Params()._asdict().keys())),
    'beam-search': (Params(num_beams=1, do_sample=False, num_beam_groups=1), {'num_beams', 'num_beam_groups'}),
    'contrastive': (Params(penalty_alpha=0.6, top_k=50), {'penalty_alpha', 'top_k', 'top_p'}),
    'multinomial': (Params(num_beams=1, do_sample=True), {'num_beams'})
}


class Config(NamedTuple):
    enable: bool = True
    preset: str = 'custom'
    params: Params = Params()


class BLIPSettingUI:
    def create_param_ui(self):
        self.ui_blocks: dict[str, gr.Blocks] = dict()
        th = get_type_hints(Config)

    def create_ui(
        self,
        default: Config
    ):
        self.cb_enable = gr.Checkbox(label='Use custom params', value=default.enable, interactive=True)
        # Validate preset value is in choices, default to 'custom' if not
        valid_preset = default.preset if default.preset in presets else 'custom'
        self.dd_preset = gr.Dropdown(
            list(presets.keys()), value=valid_preset)
        with gr.Column(variant='panel'):
            self.create_param_ui()
