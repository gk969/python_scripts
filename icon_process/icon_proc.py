import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

class Img:
    def __init__(self, name, height, width, pixels):
        self.name=name
        self.height = height
        self.width = width
        self.pixels = pixels
        print("pixels %d" % len(pixels))


def read_img_file(file):
    print(file)
    img = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB)
    print(img.shape)

    pixels=[]
    for line in img:
        for pix in line:
            pixels.append((pix[0] >> 3 << 11) | (pix[1] >> 2 << 5) | (pix[2] >> 3))

    return Img(file.replace("/", "_").replace("-", "_"), img.shape[0], img.shape[1], pixels)


def read_img_in_dir(dir):
    img_list=[]
    for file in os.listdir(dir):
        full_path = dir+"/"+file
        if os.path.isdir(full_path):
            img_list+=read_img_in_dir(full_path)
        elif os.path.splitext(full_path)[1] == ".png":
            img_list.append(read_img_file(full_path))
    
    return img_list


def write_cmd_style_file(img_list, out_file):
    with open(out_file, "wt") as out:
        name_str = ""
        addr_str = ""
        total_pixels=[]
        total_len=0
        chksum=0
        for img in img_list:
            name_str += "%s," % (img.name)
            offset=total_len
            img_len = len(img.pixels)
            chksum += offset+img_len
            addr_str += "%06X_%06X-" % (offset, img_len)
            total_len += img_len
            total_pixels+=img.pixels
        chksum+=total_len
        
        print("img_name [%s]" % name_str[0:-1], file=out)
        print("img_addr_list chksum:%08X,total:%08X,list:%s" % (chksum, total_len, addr_str), file=out)
        print("img_addr_list img %d pixels %d" % (len(img_list), total_len))

        PACK_SIZE_MAX=128
        offset=0
        for pack_offset in range(0, len(total_pixels), PACK_SIZE_MAX):
            pack_size=len(total_pixels)-pack_offset
            if pack_size>PACK_SIZE_MAX:
                pack_size=PACK_SIZE_MAX
            
            pixel_str=""
            chksum=0
            for i in range(pack_offset, pack_offset+pack_size):
                pixel_str+="%04X-" % total_pixels[i]
                chksum+=total_pixels[i]
            chksum += offset+pack_size
            print("img_pixel chksum:%08X,offset:%08X,len:%04X,data:%s" % (chksum, offset, pack_size, pixel_str), file=out)
            offset += pack_size
            
if(__name__ == '__main__'):
    img_list = read_img_in_dir("icon")
    write_cmd_style_file(img_list, "icon.cwi")

