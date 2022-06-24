from exif import Image
with open('priroda_kartinki_foto_03.jpg','rb') as imageFile:
    exifImage2 = Image(imageFile)
bubaList = {'Bop','Pop','Cat','Mep','Ill','Oil','Pill'}
exifImage2.make = "%s" % (bubaList)

with open('ModImage.jpg','wb') as newImageFile:
    newImageFile.write(exifImage2.get_file())
list = exifImage2.make
newImageFile.close()
imageFile.close()
print(list)
