from PIL import Image 
from PIL.ExifTags import TAGS  
import struct

def read_image_header(image_path):
    with open(image_path, 'rb') as f:
        header = f.read(16)  # Đọc 16 byte đầu tiên
        print("Header (Hex):", header.hex())
    
    try:
        image = Image.open(image_path)
        print("Format:", image.format)
        print("Size:", image.size)
        print("Mode:", image.mode)
        
        # Đọc metadata EXIF nếu có
        exif_data = image._getexif()
        if exif_data:
            print("EXIF Metadata:")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                print(f"{tag_name}: {value}")
        else:
            print("No EXIF metadata found.")
    except Exception as e:
        print("Error reading image:", e)

test_image = "C:\\Users\\DELL\\OneDrive\\Pictures\\Annotation 2024-10-24 123007.png"  
read_image_header(test_image)
