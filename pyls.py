def base_sort(item):
    return item["name"]
    
def prepare_all_details():
    list_of_files = []
    src = {}
    flag = True if "-r" in sys.argv else False 
    for rec in all_records:
        if "-A" not in sys.argv:
            if rec["name"].startswith("."):
                continue
        rec['label'] = ''
        list_of_files.append(rec)
        if rec.get("contents", False):
            for sub_rec in rec["contents"]:
                src = sub_rec.copy()
                src['label'] = rec['name']
                list_of_files.append(src)

    #print(list_of_files)
    return sorted(list_of_files, key=base_sort, reverse=flag)

def name_of_files():
    for rec in op_table:
        #if "-A" not in sys.argv:
        #    continue
        if len(rec['label']) > 0:
            continue
        print(rec["name"], end=' ')
    print()

def print_all_details():
    import datetime

    for rec in op_table:
        date_time = datetime.datetime.fromtimestamp(rec["time_modified"]).strftime("%b %d %H:%M:%S")
        if "--filter=dir" in sys.argv and rec["permissions"].startswith("-"):
                continue
        if "--filter=file" in sys.argv and rec["permissions"].startswith("d"):
                continue
        if "-h" in sys.argv:
            size = human_readble(rec["size"])
        else:
            size = str(rec["size"])
        if len(rec['label']) > 0:
            continue
        print(rec["permissions"] + " " + size + " " + str(date_time) + " " + rec["name"])

def sort_details_by_time():
    file_per_time = {}
    flag = True if "-r" in sys.argv else False
    for rec in op_table:
        file_per_time[rec["name"]] = rec["time_modified"]
    sorted(file_per_time, key=lambda x:x[1], reverse=flag)

    for key in file_per_time.keys():
        print(key, end=" ")
    print()

def human_readble(total_bytes):
    import math
    div_mb = total_bytes/(1024*1024)
    if int(div_mb/1024) > 0:
        div_gb = div_mb/1024
        size = math.ceil(div_gb)
        size = str(size) + "G"
    elif int(div_mb) > 0:
        div_mb = total_bytes/(1024*1024)
        size = math.ceil(div_mb)
        size = str(size) + "M"
    elif int(total_bytes/1024) > 0:
        div_kb = total_bytes/1024
        size = math.ceil(div_kb)
        size = str(size) + "K"
    else :
        size = str(total_bytes)
    return size

def read_from_json(path):
    import json

    with open(path) as json_file:
        data = json.load(json_file)
        all_contents = data['contents']
    return all_contents

if __name__ == '__main__':
    import sys

    all_records = read_from_json('structure.json')
    allowed_options = ['-A','-l','-r','-t','-h','--flag', '--filter=dir', '--filter=file']
    
    for opt in sys.argv[1:]:
        if opt not in allowed_options or '-help' in sys.argv:
            print("USAGE : pyls -[options] | -l , -A, -r, -t, -help, --flag")
            print("Extended options : pyls -l -A -r -t --flag=dir|file")
            sys.exit(-1)
    op_table = prepare_all_details()
    
    if len(sys.argv) == 1:
        name_of_files()
    else :
        if "-A" in sys.argv and "-l" in sys.argv and "-t" in sys.argv and "-r" in sys.argv:
            print_all_details()
        elif "-l" in sys.argv and "-t" in sys.argv and "-r" in sys.argv:
            print_all_details()
        elif "-l" in sys.argv and "-t" in sys.argv:
            print_all_details()
        elif "-r" in sys.argv and "-t" in sys.argv:
            sort_details_by_time()
        elif "-A" in sys.argv and "-l" in sys.argv:
            print_all_details()
        elif "-A" in sys.argv:
            name_of_files()
        elif "-l" in sys.argv:
            print_all_details()
