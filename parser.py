# Parse text from ODP file

import zipfile
from xml.dom import minidom

tmpfile = '/home/calvin/Documents/sdic/backups/sdic-backup_2022-01-16_1114_full/sdi.church/Worship Presentation/ODP/Praises/Joy.odp'
targetFile = 'content.xml'

def unzip(file):
    if zipfile.is_zipfile(tmpfile):
        with zipfile.ZipFile(file, 'r') as zipObj:
            fileList = zipObj.namelist()
            if targetFile in fileList:
                zipObj.extract(targetFile, '.')
            else:
                print(targetFile + ' is not in zipfile')
    else:
        print('File is not a zip file')
        print(tmpfile)

def parseText(file):
    parser = minidom.parse(file)
    slides = parser.getElementsByTagName('draw:page')
    
    # for each page/slide
    for slide in slides:
        slideNo = slide.attributes['draw:name'].value
        print(slideNo)

        # get all texts in a slide
        spanTags = slide.getElementsByTagName('text:span')
        
        texts = []
        # for each textline in a slide
        for span in spanTags:
            if span.hasAttribute('text:style-name'):
                if span.attributes['text:style-name'].value == 'T1':
                    songTitle = span.firstChild.data
                elif span.attributes['text:style-name'].value == 'T2':
                    texts.append(span.firstChild.data)
                elif span.attributes['text:style-name'].value == 'T3':
                    verse = span.firstChild.data
        if 'songTitle' in locals():
            lyrics = "\n".join(texts)
            print(songTitle)
            print(verse)
            print(lyrics)
            print('----')
                

if __name__ == '__main__':
    #unzip(tmpfile)
    parseText(targetFile)