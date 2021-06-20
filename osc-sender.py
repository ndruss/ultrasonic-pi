from pythonosc import udp_client
from threading import *
import time
from distance import sense_distance

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

min_cutoff = 40

amp = 0
pitch = 0
cutoff = min_cutoff

note_range = [54, 66]
notes = [*range(note_range[0], note_range[1] + 1, 1)]
note_count = len(notes)

def percent_to_midi(percent):
    index = int(percent * (note_count - 1))
    return notes[index]

def trigger_note(e):
    level = int(e) / 4
    sender.send_message('/trigger/prophet', [70, 100, level])

def change_pitch(e):
    # print('changing pitch')
    global pitch
    percent = 1 - int(e) / 255
    pitch = percent_to_midi(percent)

def change_volume(e):
    # print('changing volume')
    global amp
    amp = abs(128 - int(e)) / 128

def change_cutoff(e):
    global cutoff
    percent = abs(128 - int(e)) / 128
    cutoff = (percent * 60) + min_cutoff
    print(cutoff)

def print_distance(dist):
	# print ('%.2f cm' % dist)
	print(round(dist / 100, 2))

def listen_to_sensors():
    # controller.handleInput(None, change_cutoff, change_pitch)
    sense_distance(print_distance)

def play():
    global amp
    global pitch
    pitch = percent_to_midi(0.5)

    while True:
        if cutoff > min_cutoff:
            sender.send_message('/trigger/prophet', [pitch, cutoff, 1])
            # print('amp', amp)
            # print('pitch', pitch)
            time.sleep(0.1)


# creating threads
t1 = Thread(target=listen_to_sensors)
t2 = Thread(target=play)

# starting threads
t1.start()
# t2.start()
