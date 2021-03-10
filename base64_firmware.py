import sys
import base64

if len(sys.argv)<6:
    print("Argv Error! EXIT!")
    exit()

in_file_name=sys.argv[1]
out_file_name=sys.argv[2]
model=sys.argv[3]
version=sys.argv[4]
build_time=sys.argv[5]
# print("in_file_name %s out_file_name %s model %s version %s build_time %s" %
#       (in_file_name, out_file_name, model, version, build_time))

with open(in_file_name, "rb") as in_file:
    in_data=in_file.read()

PACK_LEN_MAX=512
with open(out_file_name, 'wt') as out:
    print('{"model":"%s", "version":"%s", "build":"%s"}' % (model, version, build_time), file=out)
    for i in range(0, len(in_data), PACK_LEN_MAX):
        pack_len = PACK_LEN_MAX
        if i+pack_len > len(in_data):
            pack_len = len(in_data)-i
        base64_pack=str(base64.b64encode(in_data[i:(i+pack_len)]), "ascii")
        print("firmware no:%d,data:%s" % (i/PACK_LEN_MAX, base64_pack), file=out)
    print("firmware no:FFFF,sum:%d,len:%d" % (sum(in_data), len(in_data)), file=out)



