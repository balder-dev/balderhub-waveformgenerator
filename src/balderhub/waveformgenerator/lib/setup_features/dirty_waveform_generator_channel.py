import decimal
from typing import Union

from balderhub.waveform.lib.utils.waveforms.base_periodic_waveform import BasePeriodicWaveform

from ..scenario_features import WaveformGeneratorFeature
from ..scenario_features.waveform_generator_instrument import WaveformGeneratorInstrument


class DirtyWaveformGeneratorChannel(WaveformGeneratorFeature):
    """
    Dirty helper feature that can be assigned directly to the device
    """
    inst = WaveformGeneratorInstrument()

    @property
    def channel(self) -> WaveformGeneratorInstrument.Channel:
        """
        :return: returns the channel that should be used for the feature (defaults to 1)
        """
        return self.inst.__class__.Channel(1)

    def is_inverted(self) -> bool:
        return self.inst.is_inverted(self.channel)

    def is_enabled(self) -> bool:
        return self.inst.is_enabled(self.channel)

    def set_waveform(
            self,
            waveform: BasePeriodicWaveform,
    ) -> None:
        if not self.inst.is_waveform_on_instrument(waveform):
            self.inst.save_waveform(waveform)
        self.inst.select_waveform(
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
        self.inst.update_waveform_parameters(self.channel, frequency_hz, amplitude_vpp, offset_vdc, phase)

    def get_current_frequency_hz(self) -> decimal.Decimal:
        return self.inst.get_current_frequency_hz(of_channel=self.channel)

    def get_current_amplitude_vpp(self) -> decimal.Decimal:
        return self.inst.get_current_amplitude_vpp(of_channel=self.channel)

    def get_current_offset_vdc(self) -> decimal.Decimal:
        return self.inst.get_current_offset_vdc(of_channel=self.channel)

    def get_current_phase(self) -> decimal.Decimal:
        return self.inst.get_current_phase(of_channel=self.channel)

    def enable_signal(self) -> None:
        self.inst.enable_signal(self.channel)

    def disable_signal(self) -> None:
        self.inst.disable_signal(self.channel)

    def invert_signal(self, state: bool):
        self.inst.invert_signal(self.channel, state=state)
