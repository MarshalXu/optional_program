import os
import sys
import msvcrt



if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# with open(application_path+"/record.pcm","rb") as f:
#     a = f.read()

file_state = os.stat(application_path+"/record.pcm")
file_len = file_state.st_size
print("total file size：",file_len)



flag =0
start = 0
crc_offset = 2
data_offset = 4096
time_stamp_offset = 4
source = open(application_path+"/record.pcm","rb")
result = open(application_path+"/result.pcm","wb")

def set_start(p):
    global start
    start += p
    source.seek(start)

while(1):

    if source.read(crc_offset) == b'\x04\x00':
        set_start(crc_offset)
        if source.read(crc_offset) == b'\x00\x10':
            set_start(crc_offset)
            time_stamp = int.from_bytes(source.read(time_stamp_offset),byteorder='little',signed='false')/16
            print(time_stamp)
            set_start(time_stamp_offset)
            if start+data_offset <= file_len:
                data = source.read(data_offset)
                set_start(data_offset)
                result.write(data)
            else:
                data = source.read(file_len-start)
                result.write(data)
                flag = 1
            if flag == 1:
                print("完成")
                break
            else:
                continue
        else:
            set_start(crc_offset)
            continue
    else:
        set_start(crc_offset)
        continue
    
source.close()
result.close()

print("Press 'D' to exit...")

while True:
    if ord(msvcrt.getch()) in [68, 100]:
        break