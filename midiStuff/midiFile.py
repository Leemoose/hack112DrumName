import mido

from mido import Message, MidiFile, MidiTrack


mid = mido.MidiFile('AULDLANG.mid')

notes = {'timeTick':0, 'notes':[]}


tempo = 50000

for i, track in enumerate(mid.tracks):
    # print('Track {}: {}'.format(i, track.name))
    for msgO in track:
        msg = str(msgO)
    
        if msg.startswith('<meta message set_tempo tempo='):
            tempo=msg[len('<meta message set_tempo tempo='):len('<meta message set_tempo tempo=')+5]
            
        if msg.startswith('note'):
            # print(msg)
            timeI = msg.find('time=') + 5

            timeNow = int(msg[timeI:])

            notes['timeTick'] += timeNow

            for elem in msg.split(" "):
                if elem.startswith('note='):
                    noteNum = elem[5:]
                    # print(noteNum)

            if msg.startswith("note_on"):
                notes['notes'].append((noteNum, notes['timeTick'],
                    mido.tick2second(int(notes['timeTick']), int(mid.ticks_per_beat),int(tempo))*10))
