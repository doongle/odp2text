import parser, glob, zipfile, json

song_directory = '../song_data/ODP/Praises/'
tmpDirectory = '../song_data/xml/'
targetFile = 'content.xml'

ODPs = glob.glob(song_directory + "*.odp")

if __name__ == '__main__':
    for odp in ODPs:
        xmlFile = parser.unzip(odp)
        odpObj = parser.load_ODP(tmpDirectory + xmlFile)
        slides = parser.get_slides(odpObj)
        song = parser.extract_song(slides)
        print(json.dumps(song, indent=4))
        stop = input('Press <ENTER> to continue or any other key to stop: ')
        if stop:
            break