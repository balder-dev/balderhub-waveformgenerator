import time
import balder
from balderhub.waveformgenerator.lib.scenario_features import WaveformGeneratorFeature, TestConfig

from balderhub.waveformmonitor.lib.scenario_features import WaveformMonitorFeature


class ScenarioPlayAndRecord(balder.Scenario):
    """Simple test scenario to play a signal with a waveform generator and read it back with a waveform monitor"""

    class DUT(balder.Device):
        """device under test"""
        testconfig = TestConfig()
        waveform = WaveformGeneratorFeature()

    class Monitor(balder.Device):
        """waveform monitor device"""
        waveform = WaveformMonitorFeature()

    @balder.parametrize_by_feature('waveform', (Monitor, 'testconfig', 'waveforms_to_test'))
    def test_play_and_record(self, waveform):
        """simple test that tries to play a waveform with the generator and reads it back with the monitor"""

        self.DUT.waveform.set_waveform(waveform)

        try:
            self.DUT.waveform.enable_signal()
            try:
                self.Monitor.waveform.start_capturing(1/waveform.frequency_hz, waveform.amplitude_vpp / 4)
                time.sleep(10)
            finally:
                self.Monitor.waveform.stop_capturing()
        finally:
            self.DUT.waveform.disable_signal()

        captured_waveform = self.Monitor.waveform.get_last_captured_waveform()
        captured_waveform.show_plot()

        captured_periodic_waveform = captured_waveform.get_periodic_equivalent_waveform()
        captured_periodic_waveform.show_plot()

        assert waveform.compare(captured_periodic_waveform, ignore_phase=True)
