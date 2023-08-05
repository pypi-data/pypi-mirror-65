#! python3
'''
Utilities to extract, process and write image file metadata.
It synchronizes captions between the various formats.
The intent is to make the many captions created with Google's defunct Picasa
to be copied into other formats in the photo, so they appear when the
photo is viewed through more modern photo handlers.
There is also a routine to synchronize captions between a .JPG and a .TIFF.
The scanspeeder scanning software will create a JPG, and in a folder underneath it,
a TIFF with the same basename.  When you caption the JPG, you can run Synch_to_TIF
to get the caption copied to the TIF."""
"""
Because of the multiple standards, this is complicated.
In the end, I've decided to use py3exiv2, since it can read IPTC, Exif, and XMP and return
them all in one dictionary.

It is hard to find captions.  They can be stored in IPTC data, or EXIF data, or XMP data.
They can be stored in Iptc.Application2.Caption, or Xmp.dc.description, or
exif.image.Image Description or Xmp.dc.title or even custom fields.
It was very surprising to find that Picassa seemed to use IPTC.Application2.Caption
instead of IPTC.caption/abstract

See http://www.photometadata.org/meta-resources-field-guide-to-metadata

Use http://exif.regex.info/exif.cgi to get the info on a single file

To find them you really have to get some sample photos, then load the photos and dump all the
keys and values in the metadata.  You look for the known value, and see what key it is stored under.

In the end, I wrote find_all_keys, which scans a folder tree and lists all distinct keys -- of which
there are many in Exif and Xmp you don't care about, as they are for specific camera settings.

Finally, I found that half a dozen IPTC fields were supposedly stored in utf-16 encoding, not utf-8.
It is hard to retrieve the normal text using the iptcinfo3 library, as it needs decoding from utf-8 or utf-16.
The Pyexiv2 library has a function to do this, which I used to write back data, but not to read it.

The Exif standard, as documented here: https://sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
says that the following are int8u (utf-8 byte strings, I think).
    XPTitle
    XPComment
    XPAuthor
    XPKeywords
    XPSubject
It says that ImageDescription is a string, which I found to be true in
    /media/max/AsusC/Photographs/Family/2009/With Mom Aug-Dec/SDC10098.JPG
However, I found a dozen and a half photos where it was a byte string.  See Problem Image Descriptions.txt
These appear to be mostly in the Legacy folder, created by the scanner, and captioned by it
    Here is what I found in test photos:
    SDC10098.JPG
        Iptc.Application2.Caption  = 'Gayle, Maurine, Max'
        BUT Exif.Image.ImageDescription contains crap: "<KENOX S860  / Samsung S860>"
        LESSON: when found, Caption takes priority
    DSC00021.jpg From Sony FDR-AX33 camcorder, captioned in Picasa
        Exif.Image.ImageDescription contains: "Getting ready to explore on our first day in Dublin. "
        Iptc.Application2.ObjectName contains "The Clayton Hotel, Ballsbridge"
        Iptc.Application2.Caption contains "Getting ready to explore on our first day in Dublin. "
        Xmp.dc.title contains "The Clayton Hotel, Ballsbridge"
        Xmp.dc.description contains 'Getting ready to explore on our first day in Dublin. '
    DSC00015.jpg from Sony FDR-AX33 camcorder, captioned in Picasa
        Exif.Image.ImageDescription contains: "Our first night's stay. In a wealthy suburb of Dublin."
        Iptc.Application2.ObjectName contains "The Clayton Hotel, Ballsbridge"
        Iptc.Application2.Caption contains "Our first night's stay. In a wealthy suburb of Dublin."
So I wrote a function, imageKeyValueType, to guess the type based on the value.
Eventually I checked all these photos and saw that I wanted to simply let the caption field overwrite the bad data.

Shotwell 'captions' photos using the Title field, which is XMP.Description.  When you modify the Title field in
Shotwell it modifies XMP.Caption, XMP.Headline but not XMP.Description or Exif.Image.Description or EXIF.XP.Title.
It modifies Iptc.Caption-Abstract and Iptc.Headline to hold the modified Title.
Shotwell provides for elaborate comments using the XMP Notes field, and EXIF User Comment field, same text in both

I set up logging at the module level.  Thus filehandler and consolehandler are global variables, and can
be changed inside functions.

'''
# Installing pyexiv2 is troublesome.
# First install boost.python via sudo apt-get install libboost-all-dev
# Next install libexiv2 developers edition:  sudo apt-get install libexiv2-dev
# Next sudo -H pip3 install py3exiv2
# Next install py3exiv2 in the PyCharm interpreter
# Docs are at https://pypi.org/project/py3exiv2/ and https://python3-exiv2.readthedocs.io/en/latest/index.html


import logging
import os, os.path, sys
from pathlib import Path
from pprint import *
import pyexiv2  # yes this really is py3exiv2, for compatibility reasons.
sys.path.append('/home/max/PycharmProjects/Utilities/')
from myUtilities import *  # Max's utilities
import PySimpleGUI as sg

import codecs
# Use codecs line below to cause pyexiv2 automatic encoding and decoding to ignore errors
# Images tend to have lots of bad or non-standard string data.  Best to ignore that.
codecs.register_error("strict", codecs.ignore_errors)

# This is used to list only the tags of interest
img_text_tags = {
    'Exif.Image.DocumentName': 'string',
    'Exif.Image.ImageDescription': 'string',
    'Exif.Image.XPTitle': 'utf-8',
    'Exif.Image.XPComment': 'utf-8',
    'Exif.Image.XPAuthor': 'utf-8',
    'Exif.Image.XPKeywords': 'utf-8',
    'Exif.Image.XPSubject': 'utf-8',
    'Xmp.dc.description': 'utf-8',
    'Xmp.dc.title': 'utf-8',
    'Iptc.Application2.Caption': 'string'
    }

# This is used to ignore bad data that occurs in some of the fields.
bogusDescriptions = {
    'None',
    'OLYMPUS DIGITAL CAMERA',
    '<KENOX S860  / Samsung S860>',
    'Autosave-File vom d-lab2/3 der AgfaPhoto GmbH ',
    'Autosave-File vom d-lab2/3 der AgfaPhoto GmbH',
    'DCIM\\100SPORT',
    'DCIM\\100GOPRO\\GOPR0352.JPG',
    'DCIM\\103GOPRO\\G0033741.JPG',
    'DCIM\\103GOPRO\\G0063888.JPG',
    'DCIM\\103GOPRO\\G0063912.JPG',
    'DCIM\\103GOPRO\\G0063913.JPG',
    'DCIM\\103GOPRO\\G0073962.JPG',
    'DCIM\\103GOPRO\\G0073965.JPG',
    'DCIM\\103GOPRO\\GOPR3982.JPG',
    'DCIM\\103GOPRO\\GOPR3983.JPG',
    'DCIM\\103GOPRO\\G0084047.JPG',
    'DCIM\\103GOPRO\\G0084155.JPG',
    'DCIM\\103GOPRO\\G0084156.JPG',
    'DCIM\\103GOPRO\\G0084160.JPG',
    'DCIM\\103GOPRO\\G0084161.JPG',
    'DCIM\\103GOPRO\\G0084186.JPG',
    'DCIM\\103GOPRO\\G0084188.JPG',
    'DCIM\\103GOPRO\\G0084189.JPG',
    'DCIM\\103GOPRO\\G0084190.JPG',
    'DCIM\\103GOPRO\\G0073966.JPG',
    'DCIM\\103GOPRO\\G0084187.JPG',
    'DCIM\\104GOPRO\\G0084699.JPG',
    'DCIM\\104GOPRO\\G0084909.JPG',
    'DCIM\\104GOPRO\\G0084910.JPG',
    'DCIM\\104GOPRO\\G0084915.JPG',
    'DCIM\\104GOPRO\\G0084943.JPG',
    'DCIM\\104GOPRO\\G0085274.JPG',
    'DCIM\\105GOPRO\\GOPR5704.JPG'}


def getEXIF(file: str) -> dict:
    '''Return Exif tags
    :param file: an image file
    :type file: str
    :return: dictionary of exif data
    :rtype: dict

    NOTE WELL.  Scanned photos will have HARDLY ANY EXIF data, so use tags.get(key) to avoid lots of try: except:
    '''
    import exifread
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    f.close()
    # print('Type: ', type(tags))
    # pprint(list(tags.keys()))
    # pprint(list(tags.values()))
    # print(tags['Image DateTime'])

    # Convert byte array to unicode
    for k in ['Image XPTitle', 'Image XPComment', 'Image XPAuthor',
              'Image XPKeywords', 'Image XPSubject']:
        if k in tags:
            tagValue = tags[k].values  # get the value, which here is a sequence of unicode byte numbers
            # Below like can fail on Image ImageDescription, which can be empty or have unencoded data
            byteString = bytes(tagValue)  # Converts the list to bytes, which are utf-16.  Ugh
            string = byteString.decode('utf-16')  # Convert the bytes to normal string
            tags[k].values = string  # Store the converted string

    if 'Image XPTitle' in tags:
        print("Title: ", tags['Image XPTitle'].values)

    if 'Image ImageDescription' in tags:
        print("Description: ", tags['Image ImageDescription'].values)

    return tags


def getIPTC(file: str):
    '''
    HUGE LIMITATION.
    If no IPTC data in a file, it terminates with message "No IPTC data found in Picassa.jpg"
    but with NO TRAPPABLE ERROR CODE.
    If you force it with info = IPTCInfo(file, force=True) it terminates with message
    "Marker scan hit start of image data" but again with NO TRAPPABLE ERROR CODE
    Get IPTC info from an image file.
    :param file: path to an image file
    :type file: str
    :return: IPTC info
    :rtype: charset
    '''
    from iptcinfo3 import IPTCInfo
    # Create new info object
    info = IPTCInfo(file)  # info is of type charset

    # Print list of keywords, supplemental categories, contacts
    # print(info['keywords'])
    # print(info['supplementalCategories'])
    # print(info['contacts'])
    print(type(info))
    print(info)
    # Get specific attributes...
    caption = info['caption/abstract']
    print(caption)
    return info

    # Create object for file that may not have IPTC data
    # info = IPTCInfo(file, force=True)

    # Add/change an attribute
    info['caption/abstract'] = 'Witty caption here'
    info['supplemental category'] = ['portrait']

    # Save new info to file
    ##### See disclaimer in 'SAVING FILES' section #####
    # info.save()  # Fails if the file doesn't have any IPTC data
    info.save_as('very_meta.jpg')
    return info


def find_all_keys(root='/media/max/AsusC/Photographs'):
    # Use this at the start of a project to find out all the keys used by the photos you are processing.
    iptcKeys = {}
    xmpKeys = {}
    exifKeys = {}
    for folderName, subfolders, filenames in os.walk(root):
        # Remember, for each loop, the foldername changes to the current position in the directory tree
        print('Processing ' + folderName)
        for filename in filenames:
            # Get the full, absolute file paths, and use that
            absWorkingDir = os.path.abspath(folderName)
            fullname = os.path.join(absWorkingDir, filename)
            # testMetadataExtractors(fullname)
            if fileExt(filename) not in ['jpg', 'jpeg', 'tif', 'tiff', 'png']:
                continue

            metadata = pyexiv2.ImageMetadata(fullname)
            try:
                metadata.read()
                for k in metadata.exif_keys:
                    exifKeys[k] = k
                for k in metadata.xmp_keys:
                    xmpKeys[k] = k
                for k in metadata.iptc_keys:
                    iptcKeys[k] = k
            except FileNotFoundError as err:
                logger.error('File not found error.  '
                             'Have you mounted the filesystem target? For Windows you need to do that first.')
                logger.error(err)
    logger.info(pformat(exifKeys))
    logger.info((pformat(xmpKeys)))
    logger.info(pformat(iptcKeys))
    print('done')


def get_value(metadata, k, v) -> str:
    '''For a key, value pair, determine how to retrieve the value as a string and return it.'''
    if k in metadata.keys():
        # Determine the Family of the tag, as the rules are slightly different for Exif, Iptc, and XMP
        family = k.split('.')[0]
        if family == 'Exif':  # Argg.  How you read and write it depends on the type
            if metadata[k].type=='Byte':
                val = pyexiv2.undefined_to_string(v.value)
            elif metadata[k].type=='Ascii':
                val = v.value
            else:
                val = str(v.value)
        elif family=='Iptc':
            val = metadata[k].value[0]
        elif family=='Xmp':
            # XMP tags return a dictionary, we have to code like below
            val = v.value['x-default']
        else:
            val = v
            logger.debug("For key " + k + ' the family was not recognized.')
        # logger.debug(k + ' type is ' + metadata[k].type)
        # logger.debug(k + ' value ' + str(val))
        val = val.strip()               # lots of these are full of blanks
        if val in bogusDescriptions: val = ''
        if val is None: val = ''
    else:
        val = ''
    return val


def write_value(metadata, k, v):
    '''For a key, value pair, determine how to write it, and do so.'''
    try:
        if k in metadata.keys():
            if v is not None:
                family = k.split('.')[0]
                if family=='Exif':  # Argg.  How you read and write it depends on the type
                    if metadata[k].type=='Byte':
                        val = v.value           # v.value should be a string of bytes separated by spaces
                    elif metadata[k].type=='Ascii':
                        val = v.value
                    else:
                        val = str(v.value)
                elif family=='Iptc':
                    val = [v.value]
                elif family=='Xmp':
                    # XMP tags return a dictionary, we have to code like below
                    val = v.value['x-default']
                else:
                    val = v.value
                    logger.debug("For key " + k + ' the family was not recognized.')
                # logger.debug(k + ' type is ' + metadata[k].type)
                # logger.debug(k + ' value ' + str(val))
                if val in bogusDescriptions:
                    val = ''
                val = val.strip()  # lots of these are full of blanks
            else:
                val = ''
            # now do the write
            metadata[k] = val                           # Change the key's value
            metadata.write(preserve_timestamps=True)    # Write to the file
            return val
    except TypeError as err:
        logger.debug('Type error for k, v of ' + k + ' ' + str(v.value))
        logger.debug(err)



def testMetadataExtractors(file, test=True):
    # Here we test exifread, iptcinfo3, and py3exiv2.

    # Run this from main or from walkFolder.
    # Python has the very general Pillow (PIL) library, which is named Python Imaging Library
    # from PIL import ImageColor

    # Get EXIF metadata
    # Python has the Exif extraction tool called ExifRead
    # import exifread
    # efile = '/media/max/AsusC/Photographs/000 Test Photos/EpsonSlide.jpg'
    # sfile = '/media/max/AsusC/Photographs/000 Test Photos/ScanSpeederSlide.jpg'
    # pfile = '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_095058.jpg'
    # epson_exif = getEXIF(efile)  # Huge if the photo contains a thumbnail
    # print(epson_exif.get('EXIF UserComment'))
    # ss_exif = getEXIF(sfile)  # Huge if the photo contains a thumbnail
    # print(ss_exif.get('EXIF UserComment'))
    # ss_exif = getEXIF(pfile)  # Huge if the photo contains a thumbnail
    # print(ss_exif.get(pfile))

    # # GET IPTC metadata
    # from iptcinfo3 import IPTCInfo
    # epson_IPTC = getIPTC(efile)  # Huge if the photo contains a thumbnail
    # print(epson_IPTC['caption/abstract'])
    # ss_IPTC = getIPTC(sfile)  # Huge if the photo contains a thumbnail
    # print(ss_IPTC['caption/abstract'])

    # Now try exiv2
    import pyexiv2
    '''
    One of the big annoyances is that several fields are, according to the standards, stored as byte streams, 
    technically utf-8 or utf-16, as a string consisting of integers, not normal text.  
    I found the comment online, "Due to the "Byte" nature of this tag, pyexiv2 doesn’t know for sure how
    to interpret those values, so it just prints them out as is.
    To convert ascii text to a byte sequence value, use the
        pyexiv2.utils.string_to_u ndefined(…) function  
    This is a really bad name, but the name follows the standard since the encoding for the string is undefined
    >'''
    # file = '/media/max/AsusC/Photographs/Family/2018/From Macintosh/DSC00021.jpg'
    # file = '/media/max/AsusC/Photographs/000 Test Photos/Jean Slides-069.jpg'
    # file = '/media/max/AsusC/Photographs/000 Test Photos/ScanSpeederSlide.jpg'
    # file = '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_095058.jpg'
    # file = '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_095147.jpg'
    # file = '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/Shotwell Title.jpg'
    #file = "/media/max/AsusC/Photographs/Fishing Trips/2013 June 10-14 Mackie Lake/Arnie's Photos"



    if fileExt(file) not in ['jpg', 'jpeg', 'tif', 'tiff', 'png']:
        return False

    metadata = pyexiv2.ImageMetadata(file)
    try:
        metadata.read()
    except FileNotFoundError as err:
        logger.error('File not found error.  '
                     'Have you mounted the filesystem target? For Windows you need to do that first.')
        logger.error(err)

    key = ''
    try:
        logger.info('\n' + '- ' * 20 + os.path.basename(file) + " -" * 30)
        for k, v in metadata.items():
            if k in img_text_tags.keys():       # Just the ones we care about
                # Some interesting values are in byte strings, and may be encoded in utf-8 or utf-16
                # Finally found how to read the type from the library, and apply conversion function
                # v = get_value
                # Determine the Family of the tag, as the rules are slightly different for Exif, Iptc, and XMP
                family = k.split('.')[0]
                if family == 'Exif':                # Argg.  How you read and write it depends on the type
                    if k.type == 'Byte':
                        val = pyexiv2.undefined_to_string(v.value)
                    elif k.type == 'Ascii':
                        val = v.value
                    else:
                        val = str(v.value)
                    val = metadata[k].value
                elif family == 'Iptc':
                    val = metadata[k].value[0]
                elif family == 'Xmp':
                    val = metadata[k].value
                else:
                    val = v
                    logger.debug("For key " + k + ' the family was not recognized.')
                logger.debug(k + ' type is ' + metadata[k].type)
                logger.debug(k + ' value ' + str(val))

                metadata['Exif.Image.XPTitle'] = pyexiv2.utils.string_to_undefined("Max changed the value.")

                metadata.write()

        # The tutorial for py3exiv2 is misleading.  It suggests you do it like this:
        # tag = tags['Exif.Image.ImageDescription']     # This fails when key doesn't exist
        # tag = tags.get('Exif.Image.ImageDescription') # Do it like this.  If key doesn't exist it returns None
        # tag.value = description                       # Fails if key doesn't exist
        # tags['Exif.Image.ImageDescription'] = 'some value'    # Adds the key if it doesn't already exist

        # Many photos lack the data.  The underlying c library was written to automatically add
        # a missing key when you try to write to it, so as to avoid tedious error checking and key creation.
        # You do that by directly addressing the key, not the value, like metadata[key] = 'string'
        # Furthermore, for some keys you must convert to bytes via badly named function in the library
        # key = 'Exif.Image.XPTitle'
        # val = pyexiv2.string_to_undefined('test XPTitle text')
        # metadata[key] = val  # writes to existing key, or adds key and value if missing
        #
        # key = 'Exif.Image.XPSubject'
        # val = pyexiv2.string_to_undefined('test XP Subject text')
        # # Following line adds the key if it doesn't exist.  Always do it this way.
        # metadata[key] = val  # writes to existing key, or adds key and value if missing
        #
        # # You can pass reference to the metadata object and update that way.
        # key = 'Exif.Image.ImageDescription'
        # val = pyexiv2.string_to_undefined('test image description')
        # tags = metadata
        # tags[key] = "test to exif.image.imagedescription"

        # Finally, write to the file
        if test is not True:
            metadata.write(preserve_timestamps=True)
    except KeyError as err:
        logger.exception('Key error in accessing or updating key' + key)
    except ValueError as err:
        logger.exception('Value error in updating key ' + key + "'s value.")


def getAllMetadata(file: str, list_items: bool = True):
    '''
    Use exif2 to get metatdata for EXIF, IPTC, and XMP tags from image files
    :param file: the absolute path image filname
    :type file: string
    :return: metadata
    :rtype: dictionary like object
    See the tutorial: https://python3-exiv2.readthedocs.io/en/latest/tutorial.html
    '''
    if fileExt(file) not in ['jpg', 'jpeg', 'tif', 'tiff', 'png']:
        return False
    metadata = pyexiv2.ImageMetadata(file)
    try:
        metadata.read()
    except FileNotFoundError as err:
        logger.exception('Check to see you have read-write access to the file if it is indeed there.')
    # Makernote fields often get corrupted:     https://www.exiv2.org/makernote.html
    # But you can't delete them in the data structure returned from pyexiv2.
    # I would have to copy that into a dictionary, then delete undesired keys from the dictionary.  Ick.  Ignoring.
    if list_items is True:
        # Using this to find out which tags in my photo collection actually contain useful data, and in what format
        logger.debug('*' * 10 + file + '*' * 10)
        try:
            filehandler.setFormatter(bare)
            for k, v in metadata.items():
                if k in img_text_tags:
                    # Finally found how to read the type from the library, and apply conversion function
                    # Some interesting values are in byte strings, and may be encoded in utf-8 or utf-16
                    if "Byte" == metadata[k].type:
                        v = decode_string(v)
                    # How to handle IPTC tags, which return a list of values?
                    if k[0:4] == 'Iptc':
                        v = v.value[0]
                    # # XMP tags return a dictionary, code like below
                    # if k in ['Xmp.dc.description', 'Xmp.dc.title']:  # damn Xmp.dc. fields
                    #     v = v.value['x-default']

                    logger.debug(k + ' value ' + str(v))
        except KeyError as err:
            logger.exception("Key {} doesn't exist".format(k))
        except UnicodeDecodeError as err:
            logger.exception('UnicodeDecodeError in file {0} for key {1}'.format(os.path.basename(file), k))
    return metadata
    '''
    # Below is examples of use
    # The tutorial is misleading.  It suggests you do it like this:
    # tag = tags['Exif.Image.ImageDescription']     # This fails when key doesn't exist
    # tag.value = description                       # Fails if key doesn't exist
    # tags['Exif.Image.ImageDescription'] = description     # Always do it like this

    # Manipulating Exif metadata ************************
    tag = metadata['Exif.Image.DateTime']
    >>> tag.raw_value                           # Always a byte string
    '2004-07-13T21:23:44Z'

    >>> tag.value
    datetime.datetime(2004, 7, 13, 21, 23, 44)  # Converted to a normal string
    
    To change and write back
    import datetime
    >>> tag.value = datetime.datetime.today()
    
    >>> metadata.write(preserve_timestamps=True)    # default is False
    
    # Manipulating IPTC tags *********************************
    tag = metadata['Iptc.Application2.DateCreated']     # this always returns a LIST of values, unlike Exif
    This supports the .raw and .value the same as Exif.
    To write: 
    tag.value = [datetime.date.today()]
    metadata.write(preserve_timestamps=True)    # or
    metadata[key] = values
    >>> key = 'Iptc.Application2.Contact'
    >>> values = ['John', 'Paul', 'Ringo', 'George']
    >>> metadata[key] = pyexiv2.IptcTag(key, values)
    
    # Manipulating XMP tags *********************************
    Same as Exif plus additional support for namespaces
    '''


def fileExt(filename: str) -> str:
    '''
    Return just the file extension, without the separator, in lower case
    :param filename:
    :type filename: str
    :return: ext
    :rtype: str
    '''
    return os.path.splitext(filename)[-1][1:].lower()


def utf8(key: str) -> str:
    keys = ['Exif.Image.XPTitle',
            'Exif.Image.XPComment',
            'Exif.Image.XPAuthor',
            'Exif.Image.XPKeywords',
            'Exif.Image.XPSubject']
    if key in keys:
        return 'utf-8'  # assumes the field really does match the standard


def decode_string(byteString) -> str:
    '''
    Some Exif are in utf-16, as a string consisting of integers.  Ick.  Convert to normal string

    :param byteString: the value as a byte string object
    :type byteString: a value object from a tag, should be a string of bytes as integers
    :return: a decoded string
    :rtype: str
    '''

    try:
        # utf16 = '50 0 110 0 100 0 32 0 97 0 110 0 100 0 32 0 49 0 115 0 116 0 32 0 71 0 114 0 97 0 100 0 101'
        # Determine the type of the string
        # Tags of type Byte can be either utf-8 or utf-16.  decode_string determines it
        encoding = imageKeyValueType(byteString.value)
        if encoding is None:
            return byteString.value
        else:
            # Use split to create a list and get rid of the spaces
            str_val = byteString.value.split()
            int_val = [int(i) for i in str_val]
            bytes_val = bytes(int_val)
            text = bytes_val.decode(encoding)
            return text
    except Exception as err:
        logger.exception('The argument must be a string of integers, which specify utf-8 or utf-16 bytes')


def imageKeyValueType(val: str):
    # Use a regular expression.
    '''
    Determines whether an image key is returning a utf-16 byte stream or just text

    :param val: the value in the key, a string or a string of numbers
    :type val:
    :return: a type, utf-16, utf-8 or None
    :rtype: str
    '''

    # utf16 = '50 0 110 0 100 0 32 0 97 0 110 0 100 0 32 0 49 0 115 0 116 0 32 0 71 0 114 0 97 0 100 0 101 0'
    # utf8 = '116 101 115 116 32 88 80 84 105 116 108 101 32 116 101 120 116'

    import re
    pattern = re.compile(r'[a-zA-Z]')
    mo = re.match(pattern, val)
    if mo is not None:
        return None
    utf16 = re.compile(r'''
                        ^(?=            # pin to start, make a group, forward lookahead
                       [0-9]{1,3}           # one to three characters in range 0-9 inclusive
                       \s0\s                # a space, a 0, another space.  utf-8 doesn't seem to have this
                       [0-9]{1,3})
                       ''', re.VERBOSE)  # another group of 1-3 digits
    mo16 = re.match(utf16, val)
    if mo16 is not None:
        return 'utf-16'
    utf8 = re.compile(r'''
                        ^(?=            # pin to start, make a group, forward lookahead
                       [0-9]{1,3}       # one to three characters in range 0-9 inclusive
                       \s               # a single space
                       [1-9]{1,3})      # a group of 1 to 9, disallowing a zero separator, which utf-8 lacks
                       ''', re.VERBOSE)
    mo8 = re.match(utf8, val)
    if mo8 is not None:
        return 'utf-8'
    else:
        return None


def walkFolder(root='.', test_run: bool = True, detect_mismatches: bool = False):
    # Loop over files in a directory.  Defaults to the current working directory.
    # Walking a directory tree with os.walk()
    # Note that quickdoc (Ctrl-Q) on os.walk is VERY HELPFUL
    logger.info('Walking folder starting at ' + root)
    logger.info('Detecting and skipping mismatches? ' + detect_mismatches)

    for folderName, subfolders, filenames in os.walk(root):
        # Remember, for each loop, the foldername changes to the current position in the directory tree
        print('Processing: ' + folderName)      # give some indication where it is running
        for filename in filenames:
            # Get the full, absolute file paths, and use that
            absWorkingDir = os.path.abspath(folderName)
            fullname = os.path.join(absWorkingDir, filename)
            # testMetadataExtractors(fullname)
            synchCaptions(fullname, test_run, detect_mismatches)
            # if fileExt(fullname).upper() == 'JPG':
            #     synch_to_TIF(folderName, fullname)


def synchCaptions(filespec: str, test_run: bool = True, detect_mismatches: bool = False) -> bool:
    '''
    Sets the various metadata keys where captions are stored to all the same values
    :param filespec: full path and file name, else, file must be in current working directory
    :type filespec: basestring
    :test True suppresses changes, and only logs changes that would be made
    :return: True if successful
    :rtype: bool
    '''
    if fileExt(filespec) in ['jpg', 'jpeg', 'tif', 'tiff', 'png']:   # the function returns lower case
        logger.debug("Synching captions in {}".format(filespec))
        tags = getAllMetadata(filespec, list_items=False)
        try:
            # Get the tags
            # Note, I really should use get_value() because it has logic to deal with bogus descriptions, etc.
            caption = tags.get('Iptc.Application2.Caption')
            title = tags.get('Exif.Image.XPTitle')
            description = tags.get('Exif.Image.ImageDescription')
            xmpDescription = tags.get('Xmp.dc.description')
            xmpTitle = tags.get('Xmp.dc.title')         # this field has info from Gayle's Macintosh.  Not using it.
            comment = tags.get('Exif.Image.XPComment')
            author = tags.get('Exif.Image.XPAuthor')
            subject = tags.get('Exif.Image.XPSubject')

            # Read the values from the tags
            tabset = 35
            if caption is not None:
                caption = caption.value[0].strip()      # Damn IPTC tag returns a single valued list
                caption = caption.replace(chr(0), '')   # Strip out ending nulls
                if caption in bogusDescriptions:
                    caption = None
                else:
                    logger.debug('Caption: '.rjust(tabset) + caption)
            if title is not None:
                title = decode_string(title)              # typically in utf-8
                title = title.strip().strip().replace(chr(0), '')     # this last to strip out ending nulls
                if title in bogusDescriptions: title = ''
                logger.debug('Title: '.rjust(tabset) + title)
            if description is not None:
                description = description.value  # typically in utf-16
                description = description.strip()           # Many of my photos have a lot of spaces for description
                if description == '' or description in bogusDescriptions or "GOPR" in description:
                    description = None
                else:
                    logger.debug('Description:'.rjust(tabset) + description)
            if xmpDescription is not None:
                xmpDescription = xmpDescription.value.get('x-default')     # when empty, it returns an empty dictionary
                if xmpDescription is None or len(xmpDescription) == 0 or xmpDescription in bogusDescriptions:
                    xmpDescription = None
                else:
                    xmpDescription = xmpDescription.strip()
                    logger.debug(('Xmp.dc.description: '.rjust(tabset) + xmpDescription))
            if subject is not None:
                subject = decode_string(subject)

            # Find possible inconsistencies in captioning
            # Order of preference is caption, title, description, IptcDescription, Xmp.dc.description
            mismatch = False
            if detect_mismatches:
                if caption is not None and title is not None:
                    if caption != title:
                        logger.error('Caption and title mismatch in ' + filespec)
                        logger.error('Caption: '.rjust(tabset) + caption)
                        logger.error('Title: '.rjust(tabset) + title)
                        mismatch = True
                if caption is not None and description is not None:
                    if caption != description:
                        logger.error('Caption and description mismatch in ' + filespec)
                        logger.error('Caption: '.rjust(tabset) + caption)
                        logger.error('ImageDescription: '.rjust(tabset) + str(description))
                        mismatch = True
                if caption is not None and xmpDescription is not None:
                    if caption != xmpDescription:
                        logger.error('Caption and xmp.dc.description mismatch in ' + filespec)
                        logger.error('Caption: '.rjust(tabset) + caption)
                        logger.error('Xmp.dc.description: '.rjust(tabset) + xmpDescription)
                        mismatch = True

            # Now synchronize the variables by order of preference
            # For some fields you must convert the string to bytes via the badly named function string_to_undefined
            if caption is not None and caption != "":
                tags['Exif.Image.ImageDescription'] = caption
                tags['Exif.Image.XPTitle'] = pyexiv2.utils.string_to_undefined(caption)
                tags['Xmp.dc.description'] = caption
                logger.debug('Set the tags to caption on ' + filespec)
            elif title is not None and title != "":
                tags['Iptc.Application2.Caption'] = [title]     # must pass a list
                tags['Exif.Image.ImageDescription'] = title
                tags['Xmp.dc.description'] = title
                logger.info('Set the tags to title on ' + filespec)
            elif description is not None and description != "":
                tags['Iptc.Application2.Caption'] = [description]
                tags['Exif.Image.XPTitle'] = pyexiv2.utils.string_to_undefined(description) # annoying
                tags['Xmp.dc.description'] = description
                logger.info('Set the tags to description on ' + filespec)
            elif xmpDescription is not None and xmpDescription != "":
                tags['Iptc.Application2.Caption'] = [xmpDescription]
                tags['Exif.Image.XPTitle'] = pyexiv2.utils.string_to_undefined(xmpDescription)
                tags['Xmp.dc.description'] = xmpDescription
                logger.info('Set the tags to xmpDescription on ' + filespec)
            else:
                logger.debug('All four proposed caption fields are None for ' + filespec)
                return False      # No changes to write back

            if mismatch is True:
                logger.error('Mismatch detected in ' + filespec + '.  No changes made to it.')
            if test_run is False and mismatch is False:
                tags.write(preserve_timestamps=True)

        except KeyError as err:
            logger.exception("Key doesn't exist.  Error in: " + filespec)
            return False
    return True


def synch_to_TIF(root: str, from_file: str) -> bool:
    '''
    Find the matching TIF for a JPG and synchronize metadata between them.

    My scan program produces both a JPG and a TIF and assigns the same XPDescription or Title to them.
    However, I often edit metadata on the JPG, but not the TIF.
    Also, I have sometimes scanned photos to TIF, then converted to JPG and only tagged the JPG.
    The TIF are always exactly one folder level below the JPG, though the folder name can vary.
    If there are multiple matching TIFs (very rare) then synch them all.
    Determine matches by comparing the basenames.
    :param root: a foldername
    :param from_file: a target_file for a JPG image file
    :type from_file: str
    :return: None or True
    :rtype: bool
    '''
    from_file_root = bareFilename(from_file)
    try:
        # This way only walks one level down from the from_file file.
        for folderName, subfolders, filenames in walklevel(root, level=1):  # os.walk walks all levels
            if folderName != root:
                for target_file in filenames:
                    if target_file.upper().endswith('TIF'):
                        target_file_root = bareFilename(target_file)
                        target_file = os.path.join(folderName,target_file)
                        if target_file_root == from_file_root:
                            logger.debug(from_file + ' matches ' + target_file)
                            meta_from = getAllMetadata(from_file)
                            meta_to = getAllMetadata(target_file, list_items=False)
                            meta_from.copy(meta_to, exif=True, iptc=True, xmp=True, comment=False)  # Image comment not supported for TIF
                            # Does not copy XMP Description or subject (tags) to TIF, it seems.
                            meta_to = getAllMetadata(target_file, list_items=True)      # See difference in the log.
                            logger.debug('Copied metadata from ' + from_file + ' to ' + target_file)

    except Exception as err:
        logger.exception('Error in synch_to_TIF')
        return False

def compare_values(meta_Mac, Mac_file, meta_Win, Win_file, tag):
    logger.debug('\nfilename: ' + os.path.basename(Mac_file))
    for tag in img_text_tags:
        # comparisons = {}
        Mac_val = get_value(meta_Mac, tag, meta_Mac.get(tag))[:45]      # Just get first 75 chars
        Win_val = get_value(meta_Win, tag, meta_Win.get(tag))[:45]      # Just get first 75 chars
        if Mac_val is not None and Mac_val != "" and Win_val is not None and Win_val != '':
            logger.debug((tag + ": " + str(Mac_val)).ljust(80) + str(Win_val))
        # comparisons[tag] = [Mac_val, Win_val]


def synch_Ireland_metadata():
    '''
    Find the matching JPGs between two folders and copy some metadata between them.

    Gayle has edited metadata and cropped photos in our Ireland Photos.
    Max has done the same on another set of copies in Picasa.
    This function finds the matching files by filename, and synchs the metadata, logging conflicts
    :param Picasa_root: a foldername
    :param Mac_file: a Win_file for a JPG image file
    :type Mac_file: str
    :return: None or True
    :rtype: bool
    '''
    filehandler.setFormatter(bare)
    Mac_root = '/media/max/AsusC/Photographs/Family/2018/From Macintosh'
    Win_root = '/media/max/AsusC/Photographs/Family/2018/Ireland 2018-09-09 to 16'
    test_file = 'DSC00021.jpg'
    logger.debug('Mac tag'.ljust(120) + 'Windows tag')
    try:
        for Mac_folderName, Mac_subfolders, Mac_filenames in os.walk(Mac_root):
            for Mac_file in Mac_filenames:
                if not Mac_file.upper().endswith('JPG'): continue
                Mac_file = os.path.join(Mac_folderName, Mac_file)
                for Win_folderName, Win_subfolders, Win_filenames in os.walk(Win_root):
                    if Win_folderName not in [Win_root, 'From Macintosh']:
                        for Win_file in Win_filenames:
                            if not Win_file.upper().endswith('JPG'): continue
                            if os.path.basename(Win_file).upper() == os.path.basename(Mac_file).upper():
                                Win_file = os.path.join(Win_folderName, Win_file)
                                # logger.debug('\n' + Mac_file + ' matches ' + Win_file)
                                meta_Mac = getAllMetadata(Mac_file, list_items=False)
                                meta_Win = getAllMetadata(Win_file, list_items=False)
                                for tag in img_text_tags:
                                    Mac_val = get_value(meta_Mac, tag, meta_Mac.get(tag))
                                    Win_val = get_value(meta_Win, tag, meta_Win.get(tag))
                                    if tag!='Iptc.Application2.Caption':    # Never copy over this tag
                                        if Mac_val == '':
                                            continue
                                        elif (Win_val=='' or Mac_val != Win_val):
                                            # compare_values(meta_Mac, Mac_file, meta_Win, Win_file, tag)
                                            write_value(meta_Win, tag, meta_Mac.get(tag))   # Write Mac to Win
                                    else:
                                        if Win_val == '' or Win_val in bogusDescriptions:
                                            if Mac_val is not None and Mac_val != '' and Mac_val not in bogusDescriptions:
                                                write_value(meta_Win, tag, meta_Mac.get(tag))  # Write Mac to Win


    except Exception as err:
        logger.exception('Error in ' + __name__)
        return False


# By defining logging at the module level, we can do setLevel in one function and have it be effective everywhere
logger = logging.getLogger(__name__)  # a new logger
# Creates a logger and sets logging level to DEBUG.  Creates a console handler set to level ERROR.
logger.setLevel(logging.DEBUG)
logdir = os.path.join(os.path.expanduser('~'), 'Documents/Logs')
if not os.path.exists(logdir):
    os.makedirs(logdir)
logfile = os.path.join(logdir, os.path.basename(__file__) + '.log')
# create a filehandler and set it to log DEBUG and above
filehandler = logging.FileHandler(logfile, 'w')  # open new log file
filehandler.setLevel(logging.DEBUG)
# create a console handler with a higher log level
consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.INFO)
# create a formatter and add it to the handlers. Use {} style.  Put message at front
formatter = logging.Formatter('{message:10s} {asctime} {name} {levelname}', style='{')
bare = logging.Formatter('{message}', style='{')
filehandler.setFormatter(formatter)
consolehandler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(filehandler)
logger.addHandler(consolehandler)

# test the logging setup
# logger.info('An information message.')
# filehandler.setFormatter(bare)
# logger.info('A bare message.')
# filehandler.setFormatter(formatter)
# logger.info('A fully formatted message.')

# logger.error('This is sent to console for error level configured in consolehandler')
# Enable below to echo logging to stdout, i.e. the screen, for error level for filehandler in setup_logging
# logger.addHandler(logging.StreamHandler(sys.stdout))


def main():
    logger.setLevel(logging.INFO)
    logger.info('Starting.')
    filehandler.setFormatter(bare)
    # synch_Ireland_metadata()
    # testfile = '/media/max/AsusC/Photographs/000 Test Photos/Ireland 2018-09-09 to 16/2018-09-09/DSC00021.JPG'
    # testfile = '/media/max/AsusC/Photographs/000 Test Photos/From Macintosh/DSC00021.jpg'
    # # testfile = '/media/max/AsusC/Photographs/000 Test Photos/Ireland 2018-09-09 to 16/2018-09-10/C0030T01.JPG'
    # testMetadataExtractors(testfile, test=True)
    #

    p = Path('/Photographs/Family/2019')
    root = select_a_folder(p.expanduser())
    # root = select_a_folder(".")
    mismatches = sg.PopupYesNo('Detect and skip mismatches between caption, title, and description?')
    if sg.PopupYesNo('Save changes to files.  Are you sure?') == 'Yes':
        walkFolder(root=root, test_run=False, detect_mismatches=mismatches)
    else:
        walkFolder(root=root, test_run=True, detect_mismatches=mismatches)


    files = ['/media/max/AsusC/Photographs/Family/2009/With Mom Aug-Dec/SDC10098.JPG',
             '/media/max/AsusC/Photographs/Family/2018/From Macintosh/DSC00021.jpg',
             '/media/max/AsusC/Photographs/Family/2018/From Macintosh/DSC00015.jpg',
             '/media/max/AsusC/Photographs/Family/2018/From Macintosh/DSC00098.jpg',
             '/media/max/AsusC/Photographs/000 Test Photos/Pict0010.TIF',
             '/media/max/AsusC/Photographs/000 Test Photos/ScanSpeederSlide.jpg',
             '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_095058.jpg',
             '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_095147.jpg',
             '/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/Shotwell Title.jpg'
             ]

    # logger.info(pformat(files,width=120))
    #
    # for f in files:
    #     testMetadataExtractors(f)
    #     getIPTC(f)
    #     synchCaptions(f)

    # filename = '/media/max/QuietPC/Photo Archive/Maurine_Teaching/FullSize/Teaching 1952-53_0001.tif'
    # filename = '/media/max/AsusC/Photographs/Family/2018/From Macintosh/DSC00037.jpg'
    # synchCaptions(filename)

    # ARGGG
    # https://stackoverflow.com/questions/30297355/accessing-shared-smb-ubuntu-in-python-scripts.  We need:
    # sudo mount -t cifs -o username=Max\ Fritzler,uid=1000,gid=1000 //192.168.0.56/QuietPC\ Data\ Drive /media/max/QuietPC
    # walkFolder('/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions')

    # walkFolder(root="/media/max/AsusC/Photographs", test_run=True)

    # walkFolder(root='/media/max/AsusC/Photo Archive')
    # walkFolder('/media/max/AsusC/Photographs/000 Test Photos', test_run=False)

    # getIPTC('/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_192945.jpg')
    # getIPTC('/media/max/AsusC/Photographs/000 Test Photos/Picasa Only Captions/20190411_095058.jpg')

    # find_all_keys()
    # walkFolder(root='/media/max/AsusC/Photographs/Family/2018/From Macintosh')

    filehandler.setFormatter(formatter)
    logger.info('Finished.')


# Since this will wind up being a module, we don't want it to run any code when imported.
# So we use this.  Or we could just have nothing but function and class definitions in it.
# if __name__=='__main__':
#     pass

if __name__ == "__main__":          # use this when you want to run code from inside this module
    main()
