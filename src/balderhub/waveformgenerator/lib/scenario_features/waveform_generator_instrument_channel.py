import decimal
from typing import Union

import balder

from balderhub.waveform.lib.utils.waveforms.base_periodic_waveform import BasePeriodicWaveform
from .waveform_generator_feature import WaveformGeneratorFeature
from .waveform_generator_instrument import WaveformGeneratorInstrument


class WaveformGeneratorInstrumentChannel(WaveformGeneratorFeature):
    """
    Implementation of :class:`balderhub.waveformgenerator.lib.scenario_features.WaveformGeneratorFeature` and
    uses a channel of a :class:`balderhub.powersupply.lib.scenario_features.WaveformGeneratorInstrument`.
    """


    class Instrument(balder.VDevice):
        """vdevice representing the signal generator instrument"""
        inst = WaveformGeneratorInstrument()

    @property
    def channel(self) -> WaveformGeneratorInstrument.Channel:
        """
        :return: returns the channel identifier this feature uses
        """
        raise NotImplementedError

    def is_inverted(self) -> bool:
        return self.Instrument.inst.is_inverted(self.channel)

    def is_enabled(self) -> bool:
        return self.Instrument.inst.is_enabled(self.channel)

    def set_waveform(
            self,
            waveform: BasePeriodicWaveform,
    ) -> None:
        if not self.Instrument.inst.is_waveform_on_instrument(waveform):
            self.Instrument.inst.save_waveform(waveform)
        self.Instrument.inst.select_waveform(
            self.channel,
            waveform,
        )

    def update_waveform_parameters(
            self,
            frequency_hz: Union[decimal.Decimal, None] = None,
            amplitude_vpp: Union[decimal.Decimal, None] = None,
            offset_vdc: Union[decimal.Decimal, None] = None,
            phase: Union[decimal.Decimal, None] = None
    ) -> None:
        self.Instrument.inst.update_waveform_parameters(
            of_channel=self.channel,
            frequency_hz=frequency_hz,
            amplitude_vpp=amplitude_vpp,
            offset_vdc=offset_vdc,
            phase=phase
        )

    def get_current_frequency_hz(self) -> decimal.Decimal:
        return self.Instrument.inst.get_current_frequency_hz(of_channel=self.channel)

    def get_current_amplitude_vpp(self) -> decimal.Decimal:
        return self.Instrument.inst.get_current_amplitude_vpp(of_channel=self.channel)

    def get_current_offset_vdc(self) -> decimal.Decimal:
        return self.Instrument.inst.get_current_offset_vdc(of_channel=self.channel)

    def get_current_phase(self) -> decimal.Decimal:
        return self.Instrument.inst.get_current_phase(of_channel=self.channel)

    def enable_signal(self) -> None:
        self.Instrument.inst.enable_signal(self.channel)

    def disable_signal(self) -> None:
        self.Instrument.inst.disable_signal(self.channel)

    def invert_signal(self, state: bool):
        self.Instrument.inst.invert_signal(self.channel, state=state)
