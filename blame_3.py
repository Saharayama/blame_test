import re
import subprocess

SRC_FILE = r'./src.txt'
LIST_FILE = r'./list.txt'
OUT_FILE = r'./out.txt'
REPO_DIR = r'D:\Desktop\settings'
BASE_COMMIT = 'd567c3e3cbe976536adadca02affd33cf198ca74'

l_all_list = ''

def write_out():
    with open(OUT_FILE, 'a', encoding='utf-8') as f_out:
        f_out.write(l_src)
        f_out.write('\n')

def get_base_commit_time():
    cmd = 'git -C ' + REPO_DIR + ' log -1 ' + BASE_COMMIT + ' --date=unix | grep Date:'
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return int(str(res.stdout)[10:-3])

base_commit_time = get_base_commit_time()
print(base_commit_time)

with open(LIST_FILE, 'r', encoding='utf-8') as f_list:
    for l_list in f_list:
        l_list = l_list.rstrip()
        if l_list != '':
            l_all_list += l_list
            l_all_list += '|'
        else:
            continue
    l_all_list = l_all_list[:-1]

# print(l_all_list)

with open(SRC_FILE, 'r', encoding='utf-8') as f_src:
    for l_src in f_src:
        l_src = l_src.rstrip()
        if l_src != '':
            if re.findall(l_all_list, l_src):
                write_out()
            else:
                num_src = l_src.split(',')[1]
                file_src = l_src.split(',')[2]
                cmd = 'git -C ' + REPO_DIR + ' blame -pwL ' + num_src + ',' + num_src + ' ' + file_src + ' | grep author-time'
                res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
                commit_time = int(str(res.stdout)[14:-3])
                if commit_time > base_commit_time:
                    write_out()
                    print('blame', l_src)
