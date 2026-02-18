from ..scenario_features.waveform_generator_instrument import WaveformGeneratorInstrument
from ..scenario_features.waveform_generator_instrument_channel import WaveformGeneratorInstrumentChannel


class WaveformGeneratorInstrumentChannel1(WaveformGeneratorInstrumentChannel):
    """
    Universal waveform generator Setup Feature representing the Channel 1 of a signal generator instrument
    """
    @property
    def channel(self) -> WaveformGeneratorInstrument.Channel:
        return WaveformGeneratorInstrument.Channel(1)
