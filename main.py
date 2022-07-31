import parser, glob, zipfile

song_directory = './Praises/'

ODPs = glob.glob(song_directory + "*.odp")

def unzip2(file):
    targetFile = 'content.xmls'
    with zipfile.ZipFile(file, 'r') as zipObj:
        target = zipObj.getinfo(targetFile)
        print(target)
        # print(file + '-' + target.filename)
        # target.filename = file.replace(' ', '_') + '-' + target.filename
        # zipObj.extract(target)


if __name__ == '__main__':
    # print(ODPs)
    unzip2('Agnus Dei.odp')