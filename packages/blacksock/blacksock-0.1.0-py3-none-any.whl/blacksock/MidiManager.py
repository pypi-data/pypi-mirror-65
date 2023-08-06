import rtmidi

MIDI_ON = 127
MIDI_OFF = 0

class MidiManager:

    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_port(0)

    def turn_on(self, midi_nr):
        self.midiout.send_message([0xb0, midi_nr, MIDI_ON])

    def turn_off(self, midi_nr):
        self.midiout.send_message([0xb0, midi_nr, MIDI_OFF])
