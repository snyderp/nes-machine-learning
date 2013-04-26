import os
import store
from utils import trim_song, sized_observation_from_index, parse_song


data_dir = os.path.join("data", "training_songs")
max_channel_to_capture = 3
prev_frames_to_record = 16


for root, dirs, files in os.walk(data_dir):
    for name in [a_file for a_file in files if a_file[-4:] == ".mid"]:
        relative_file_path = os.path.join(root, name)

        if store.has_file_been_recorded(relative_file_path):
            print "Not recalculating counts for %s" % (relative_file_path,)
            continue
        else:
            print "Beginning to calculate counts for %s" % (relative_file_path,)
            store.record_file(relative_file_path)

        song = parse_song(relative_file_path)
        song = trim_song(song, length=2500)
        song_len = len(song[0])

        if song_len < 100:
            print "Song is too short for consideration.  May be a sound effect or something trivial.  Ignoring."
            continue

        # for channel_name in song:
        #     print channel_name
        #     print song[channel_name]
        # continue

        # for x in range(0, len(song[0])):
        #     print "|".join([str(chanel[x]) for chanel in song.values()])
        #     #print "%d: %s" % (k, ["%03d" % (i,) for i in song[k]])
        # break
        store.record_obs('S|S|S')
        for x in range(0, song_len):
            for y in range(1, prev_frames_to_record + 1):
                frame = sized_observation_from_index(song, start=x, length=y)
                store.record_obs(frame)
        store.commit()
        print "finished calculating counts from %s" % (relative_file_path,)