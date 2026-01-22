from pathlib import Path
import exifread
import datetime
import csv


def _convert_to_degress(value, ref):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    ref_multiplier = 1
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    if ref in ["S", "W"]:
        ref_multiplier = -ref_multiplier

    return ref_multiplier*(d + (m / 60.0) + (s / 3600.0))
            


def get_time(item):
    return item["time"]



def export_to_csv(data_list):
    photos_csv = open('photos2.csv', 'w', newline='', encoding='utf-8')
    fild_names = ['name', 'lat', 'lon', 'time']
    writer = csv.DictWriter(photos_csv, fieldnames=fild_names)
    writer.writeheader() #writes thr first row of titles, which is 'field_names'
    for d in data_list:
        writer.writerow(d)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('dict: ' , d)
    
    

data = []

photo_path = Path("Iphone pics")
if not photo_path.exists():
    print ("Folder not found")
else:
      print("Yay folder is here!!")
for p in photo_path.iterdir():
    print(p)
    if p.is_file() and p.suffix.lower() in [".jpg", ".jpeg", ".png", ".heic"]:
        with open(p, "rb") as photo:
            photo_item = {}
            tags = exifread.process_file(photo)
            #print(tags.get('EXIF DateTimeOriginal'))
            #print(_convert_to_degress(tags.get('GPS GPSLatitude')))
            #print(_convert_to_degress(tags.get('GPS GPSLongitude')))
            photo_item['lat'] = _convert_to_degress(tags.get('GPS GPSLatitude'), str(tags.get('GPSLatitudeRef')))
            photo_item['lon'] = _convert_to_degress(tags.get('GPS GPSLongitude'), str(tags.get('GPSLongitudeRef')))
            photo_item['time'] = str(tags.get('EXIF DateTimeOriginal'))
            photo_item['name'] = p.stem
            
            #print(photo_item)
            data.append(photo_item)
            
print("//////////////////////////////////////////////")
print(data)
            
data.sort(key=get_time)
export_to_csv(data)
#print(f"\n Sorted data: \n\n{data}")

            
            



