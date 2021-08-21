import os
import sys
import msvcrt



if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

with open(application_path+"/record.pcm","rb") as f:
    a = f.read()

flag =0
start = 0
crc_offset = 2
data_offset = 4096
time_stamp_offset = 4
file_len = len(a)
print("total file size：",file_len)

result = open(application_path+"/result.pcm","wb")
while(1):
    # print(start,start+crc_offset)
    if a[start:start+crc_offset] == b'\x04\x00':
        # print(1)
        start += 2
        if a[start:start+crc_offset] == b'\x00\x10':
            # print(2)
            start += 2
            time_stamp = int.from_bytes(a[start:start+time_stamp_offset],byteorder='little',signed='false')/16
            print(time_stamp)
            start += time_stamp_offset
            if start+data_offset <= file_len:
                data = a[start:start+data_offset]
                start += data_offset
                result.write(data)
            else:
                data = a[start:file_len]
                result.write(data)
                flag = 1
            if flag == 1:
                result.close()
                print("完成")
                break
            else:
                continue
        else:
            # print(4)
            start +=2
            continue
    else:
        # print(3)
        start += 2
        continue

print("Press 'D' to exit...")

while True:
    if ord(msvcrt.getch()) in [68, 100]:
        break