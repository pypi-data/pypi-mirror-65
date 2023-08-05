from PIL import Image
from PIL.ExifTags import TAGS
import pprint


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

fn = '/media/max/AsusC/Photographs/000 Test Photos/From Macintosh/DSC00021.jpg'

pprint.pprint(get_exif(fn))

Picasa = '/media/max/AsusC/Photographs/000 Test Photos/Ireland 2018-09-09 to 16/2018-09-09/DSC00021.JPG'

print('\n\n Picasa file ')
pprint.pprint(get_exif(Picasa))