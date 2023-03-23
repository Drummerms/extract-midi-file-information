import mido
from mido import MidiFile

midi_file = MidiFile('./Tool - 46 N 2.mid')

ticks_per_beat = midi_file.ticks_per_beat
time_signatures = []
tempos = []

for track in midi_file.tracks:
    for msg in track:
        if msg.type == 'time_signature':
            time_signature = f"{msg.numerator}/{msg.denominator}"
            time_signatures.append((msg, time_signature))
        elif msg.type == 'set_tempo':
            tempo = mido.tempo2bpm(msg.tempo)
            tempos.append((msg, tempo))

def calculate_bar_position(event_time, time_signatures, ticks_per_beat):
    accumulated_ticks = 0
    current_bar = 1
    for ts_event, _ in time_signatures:
        if event_time > ts_event.time:
            ticks_per_bar = ts_event.numerator * ticks_per_beat
            elapsed_bars, remainder = divmod(event_time - accumulated_ticks, ticks_per_bar)
            current_bar += elapsed_bars
            accumulated_ticks += elapsed_bars * ticks_per_bar
        else:
            break
    return current_bar

if time_signatures:
    print("Time Signatures:")
    for ts_event, ts in time_signatures:
        bar_position = calculate_bar_position(ts_event.time, time_signatures, ticks_per_beat)
        print(f"  - {ts} at tick {ts_event.time}, bar {bar_position}")
else:
    print("Time signatures not found in the MIDI file.")

if tempos:
    print("Tempos:")
    for tempo_event, tempo in tempos:
        bar_position = calculate_bar_position(tempo_event.time, time_signatures, ticks_per_beat)
        print(f"  - {tempo:.2f} BPM at tick {tempo_event.time}, bar {bar_position}")
else:
    print("Tempos not found in the MIDI file.")
