import re
import numpy as np
import sounddevice as sd
from typing import Optional

fourth = {
    "A": 440,
    "Bb": 466.1638,
    "B": 493.8833,
    "C": 523.2511,
    "Db": 554.3653,
    "D": 587.3295,
    "Eb": 622.2540,
    "E": 659.2551,
    "F": 698.4565,
    "Gb": 739.9888,
    "G": 783.9909,
    "Ab": 830.6094,
}

fourth_ind = {
    0: "A",
    1: "Bb",
    2: "B",
    3: "C",
    4: "Db",
    5: "D",
    6: "Eb",
    7: "E",
    8: "F",
    9: "Gb",
    10: "G",
    11: "Ab"
}

fifth_cycle = [
    "A",
    "E",
    "B",
    "Gb",
    "Db",
    "Ab",
    "Eb",
    "Bb",
    "F",
    "C",
    "G",
    "D",
]
reverse_indices = {v: k for k, v in fourth_ind.items()}

sampling_rate = 48000  # Sampling rate in Hz

class Tone:
    def __init__(self, name: str):
        self.letter, self.height = self.separate_letters_numbers(name)
        self.frequency = fourth[self.letter]*(2**(self.height-4))

    def get_wave(self, duration: float, amplitude:float=1.0):
        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        return amplitude * 0.5 * np.sin(2 * np.pi * self.frequency * t)

    def play(self, duration: float):
        wave = self.get_wave(duration)
        sd.play(wave, sampling_rate)
        sd.wait()

    def separate_letters_numbers(self, s):
        match = re.match(r"([a-zA-Z]+)(\d+)", s)
        if match:
            letters, numbers = match.groups()
            return letters, int(numbers)
        return s, 3

class Chord:
    def __init__(self, tones: list[Tone]):
        self.tones = tones

    @classmethod
    def from_name(cls, name: str):
        name_tones = list(fourth.keys())
        if len(name)>1 and name[:2] in name_tones:
            base = Tone(name[:2])
            type_chord = name[2:]
        else:
            base = Tone(name[:1])
            type_chord = name[1:]

        base_index = reverse_indices[base.letter]
        if type_chord in ["", "M", "maj"]:
            return cls([
                base,
                Tone(fourth_ind[(base_index+4)%12]),
                Tone(fourth_ind[(base_index+7)%12])
            ])
        elif type_chord in ["m", "min"]:
            return cls([
                base,
                Tone(fourth_ind[(base_index+3)%12]),
                Tone(fourth_ind[(base_index+7)%12])
            ])

    def play(self, duration: float, amplitude:float=1.0):
        wave = np.zeros(int(sampling_rate * duration))
        for tone in self.tones:
            wave += tone.get_wave(duration, amplitude=amplitude/len(self.tones))
        sd.play(wave, sampling_rate)
        sd.wait()

zombie_1 = Chord.from_name("Am")
zombie_2 = Chord.from_name("F")
zombie_3 = Chord.from_name("Cmaj")
zombie_4 = Chord.from_name("GM")

# Ca ressemble à Zombie des Cranberries
for i in range(4):
    for chord in [zombie_1, zombie_2, zombie_3, zombie_4]:
        for j in range(2):
            chord.play(0.8)
            chord.play(0.4)
            chord.play(0.2)
            chord.play(0.2)




# La COOOOOOP
n1 = Tone("A3")
n2 = Tone("C3")
n3 = Tone("D3")
n4 = Tone("E3")

n1.play(0.2)
n2.play(0.4)
n3.play(0.4)
n4.play(0.3)
n3.play(0.15)
n2.play(0.25)
n1.play(0.2)

exit()

# Parameters for the sine wave
frequency = 440  # Frequency in Hz
duration = 1  # Duration in seconds
sampling_rate = 48000  # Sampling rate in Hz

create_a_440()
