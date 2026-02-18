from ..scenario_features.waveform_generator_instrument import WaveformGeneratorInstrument
from ..scenario_features.waveform_generator_instrument_channel import WaveformGeneratorInstrumentChannel


class WaveformGeneratorInstrumentChannel2(WaveformGeneratorInstrumentChannel):
    """
    Universal waveform generator Setup Feature representing the Channel 2 of a signal generator instrument
    """
    @property
    def channel(self) -> WaveformGeneratorInstrument.Channel:
        return WaveformGeneratorInstrument.Channel(2)
