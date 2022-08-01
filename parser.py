# Parse text from ODP file
# text:p "P1" = song title
# text:p "P5" = verse
# text:p "P3" = lyrics
# text:span "T1" = song title (first page)
# text:span "T4" = song title
# text:span "T3" = verse
# text:span "T2" = lyrics

import zipfile, json, os
from xml.dom import minidom

tmpfile = '/home/calvin/Documents/sdic/backups/sdic-backup_2022-04-30_1735_full/sdi.church/Worship Presentation/ODP/Praises/Agnus Dei.odp'
tmpDirectory = '../song_data/xml/'
targetFile = 'content.xml'

def unzip(file):
    if not os.path.exists(tmpDirectory):
        os.mkdir(tmpDirectory)
    if zipfile.is_zipfile(tmpfile):
        with zipfile.ZipFile(file, 'r') as zipObj:
            fileList = zipObj.namelist()
            if targetFile in fileList:
                target = zipObj.getinfo(targetFile)
                target.filename = file.replace(' ', '_').split('/')[-1] + '-' + target.filename
                if not os.path.exists(tmpDirectory + target.filename):
                    zipObj.extract(target, tmpDirectory)
            else:
                print(targetFile + ' is not in zipfile')
    else:
        print('File is not a zip file')
        print(tmpfile)

def load_ODP(file):
    return minidom.parse(file)

def get_slides(obj):
    return obj.getElementsByTagName('draw:page')

def get_textPs(slide):
    # get all text:p(text box) in a slide
    return slide.getElementsByTagName('text:p')

def get_text(textP):
    text = []
    #nodeList => text:span
    nodeList = textP.childNodes
    line = ''
    for node in nodeList:
        element = node.firstChild
        if element.nodeType == element.TEXT_NODE:
            # if a song line is spread to multiple lines with span, gather them into one line
            line += element.data
        else:
            text.append(line)
            line = ''
    text.append(line)
    return text

def get_verseNo(verse):
    str = ''.join(verse).lower()
    switch = {
        'verse 1'      : 'v1',
        'verse 2'      : 'v2',
        'verse 3'      : 'v3',
        'verse 4'      : 'v4',
        'verse 5'      : 'v5',
        'pre-chorus'   : 'pc',
        'pre chorus'   : 'pc',
        'pre-chorus 2' : 'pc2',
        'pre chorus 2' : 'pc2',
        'pre-chorus2'  : 'pc2',
        'pre chorus2'  : 'pc2',
        'chorus'       : 'c',
        'chorus 1'     : 'c',
        'chorus1'      : 'c',
        'chorus 2'     : 'c2',
        'chorus2'      : 'c2',
        'bridge'       : 'b',
        'ending'       : 'e'
    }
    return switch.get(str, 'Invalid input')

def extract_song(slides):
    data = {
        'title' : '',
        'slides': {}
    }
    for slide in slides:
        songTitle = []
        verse = []
        lyric = []
        textPs = get_textPs(slide)

        if textPs.length == 0:
            # No text <p> element. This is last slide which is usually empty
            continue

        slideNo = int(slide.attributes['draw:name'].value[4:])

        for textP in textPs:
            if slideNo == 1:
                if textP.attributes['text:style-name'].value == 'P1':
                    # this is song title; do this only on 'page1'
                    songTitle = get_text(textP)
                    data['title'] = ''.join(songTitle)
            if textP.attributes['text:style-name'].value == 'P3':
                # this is lyric
                lyric += get_text(textP)
            elif textP.attributes['text:style-name'].value == 'P5':
                # this is verse
                verse = get_text(textP)
        
        verseNo = get_verseNo(verse)
        data['slides'][slideNo] = {
            verseNo: lyric
        }
    return data
    

if __name__ == '__main__':
    unzip(tmpfile)
    # odpObj = load_ODP(tmpDirectory + targetFile)
    # slides = get_slides(odpObj)
    # song = extract_song(slides)

    # print(json.dumps(song, indent=4))


        
    # sample data structure
    song1 = {
        'title': 'Alleluia',
        'slides': {
            'page1': { 'verse1': [ 'Line1', 'Line2', 'Line3', 'Line4' ], },
            'page2': { 'verse1': [ 'Line1', 'Line2', 'Line3' ], },
            'page3': { 'chorus': [ 'Line1', 'Line2', 'Line3' ], },
            'page4': { 'chorus': [ 'Line1', 'Line2', 'Line3' ], },
            'page5': { 'verse2': [ 'Line1', 'Line2', 'Line3' ], },
            'page6': { 'verse2': [ 'Line1', 'Line2', 'Line3' ], }
        }
    }
    song2 = {
        'title': 'Alleluia',
        'slides': {
            1:  { 'v1': [ 'Line1', 'Line2', 'Line3', 'Line4' ], },
            2:  { 'v1': [ 'Line1', 'Line2', 'Line3' ], },
            3:  { 'pc': [ 'Line1', 'Line2', 'Line3' ], },
            4:  { 'pc': [ 'Line1', 'Line2', 'Line3' ], },
            5:  { 'c':  [ 'Line1', 'Line2', 'Line3' ], },
            6:  { 'c':  [ 'Line1', 'Line2', 'Line3' ], },
            7:  { 'v2': [ 'Line1', 'Line2', 'Line3' ], },
            8:  { 'v2': [ 'Line1', 'Line2', 'Line3' ], },
            9:  { 'c2': [ 'Line1', 'Line2', 'Line3' ], },
            10: { 'c2': [ 'Line1', 'Line2', 'Line3' ], },
            11: { 'b':  [ 'Line1', 'Line2', 'Line3' ], },
            12: { 'b':  [ 'Line1', 'Line2', 'Line3' ], }
        }
    }