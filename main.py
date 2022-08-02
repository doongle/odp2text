from asyncore import read
from curses import KEY_F10
import glob, json, readchar, os, parser, subprocess

songDirectory = '../song_data/ODP/Praises/'
tmpDirectory = '../song_data/xml/'
targetFile = 'content.xml'

def clear():
    _ = subprocess.call('clear' if os.name == 'posix' else 'cls')

def get_direction():
    chr = readchar.readkey()
    switch = {
        readchar.key.LEFT      : 'go_previous',
        readchar.key.UP        : 'go_previous',
        readchar.key.PAGE_UP   : 'go_previous',
        readchar.key.RIGHT     : 'go_next',
        readchar.key.DOWN      : 'go_next',
        readchar.key.PAGE_DOWN : 'go_next',
    }
    return switch.get(chr, chr)

def extract_xml_from_odp_ALL(ODPs):
    i = 0
    range = len(ODPs) - 1
    while True:
    # for i in range(len(ODPs)):
        clear()
        print("Index #: ", i, " of ", range)
        xmlFile = parser.unzip(ODPs[i])
        odpObj = parser.load_ODP(tmpDirectory + xmlFile)
        slides = parser.get_slides(odpObj)
        slides.pop()    # remove last slide which is usually empty
        song = parser.extract_song(slides)
        print(json.dumps(song, indent=4))
        print('Press arrow key to next/previous song or any other key to stop', end=": ", flush=True)
        direction = get_direction()
        if direction == 'go_previous':
            i -= 1
            if i == -1:
                i = range
        elif direction == 'go_next':
            i += 1
            if i > range:
                i = 0
        else:
            print()
            break

def insert_into_song_db(XMLs):
    ...
    # Check the song in DB before insert
    # If song found in DB, skip insert



if __name__ == '__main__':
    ODPs = glob.glob(songDirectory + "*.odp")
    ODPs.sort()
    extract_xml_from_odp_ALL(ODPs)

    XMLs = glob.glob(tmpDirectory + "*.xml")
    # insert_into_song_db(XMLs.sort())
