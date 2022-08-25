# This program extracts selected metadata from photos in a directory and formats the
# metadata as a CSV (comma-separated values) text file. The resulting CSV file can be
# opened and edited in a spreadsheet application; it also can be used to upload metadata
# to a digital library system.

# Import modules.
import os
import mimetypes
import exifread
import csv

# Identify the photo directory. Path used for final project:
# /Users/heather_m_campbell/Documents/GitHub/452-final-project/Photos
photo_directory = input('Enter the file path to your photo directory: ')

# Generate the file names in the photo directory tree. For each directory in the tree,
# the function yields a 3-tuple (directory path [0], directory names [1], file names [2]).
allfiles = os.walk(photo_directory)
# print(allfiles)           # Uncomment this statement to view the allfiles object.

# Use loops to collect file information in a list of lists for each file.
file_num = 0
file_names = []
file_data = []
all_file_list = []

for dir in allfiles:
    path = dir[0]
    folder = path[(len(photo_directory)+1):]  # Slice path after photo directory to get folder
    file_names = dir[2]
    for file in file_names:
        if 'ipynb' not in file and 'DS_Store' not in file:
            file_num = file_num + 1
            file_data = [file_num, path, folder, file]
            all_file_list.append(file_data)

# Use length of this list to verify number of files in your photo directory.
print(len(all_file_list), 'files to process.')
# print(all_file_list)      # Uncomment this statement to view the contents of the list.

# Extract metadata from files. Put metadata in a list of lists for each file.
file_metadata = []
all_file_metadata = []

for file in all_file_list:
    file_ID = file[0]
    event = file[2]
    file_name = file[3]
    file_path = file[1] + '/' + file_name
    file_format = mimetypes.guess_type(file_path, strict=False)
    file_size = os.stat(file_path).st_size
    file_size_MB = round((file_size*0.000001),2)  # round to 2 decimal places
    image_metadata = open(file_path, 'rb')
    tags = exifread.process_file(image_metadata, details=False)
    datetime_original = tags.get('EXIF DateTimeOriginal')
    datetime_modified = tags.get('EXIF DateTime')
    image_software = tags.get('Image Software')
    image_width = tags.get('Image XResolution')
    image_height = tags.get('Image YResolution')
    image_units = tags.get('Image ResolutionUnit')
    latitude_ref = tags.get('GPS GPSLatitudeRef') # generates a list of coordinates
    latitude = tags.get('GPS GPSLatitude')
    longitude_ref = tags.get('GPS GPSLongitudeRef')
    longitude = tags.get('GPS GPSLongitude')
    camera = tags.get('Image Model')
    exposure = tags.get('EXIF ExposureTime')
    flash = tags.get('EXIF Flash')
    lens = tags.get('EXIF LensModel')
    file_metadata = [file_ID, event, file_name, file_format[0], file_size, file_size_MB,
                     datetime_original, datetime_modified,
                     image_software, latitude_ref, latitude, longitude_ref, longitude,
                     camera, exposure, flash, lens]
    all_file_metadata.append(file_metadata)

# print(all_file_metadata)  # Uncomment this statement to view the contents of the list.

# Output file metadata in CSV format.
outfile = open('photo_data.csv', 'w')
csv_out = csv.writer(outfile)
csv_out.writerow(['ID', 'Event', 'File Name', 'File Format', 'File Size (Bytes)',
                  'File Size (MB)', 'Date Taken', 'Date Modified',
                  'Software', 'Latitude', 'DMS', 'Longitude', 'DMS',
                  'Camera', 'Exposure Time', 'Flash Used?', 'Lens Model'] )
csv_out.writerows(all_file_metadata)
outfile.close()

print('Your CSV file is ready.')
# Go open your CSV file!
