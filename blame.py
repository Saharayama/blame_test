import subprocess

src_file = r'./src.txt'
list_file = r'./list.txt'
out_file = r'./out.txt'
repo_dir = r'D:\Desktop\settings'

def write_out():
    with open(out_file, 'a', encoding='utf-8') as f_out:
        f_out.write(l_src)
        f_out.write('\n')


flag_done = 0
with open(src_file, 'r', encoding='utf-8') as f_src:
    for l_src in f_src:
        l_src = l_src.rstrip()
        with open(list_file, 'r', encoding='utf-8') as f_list:
            for l_list in f_list:
                l_list = l_list.rstrip()
                if l_list in l_src:
                    write_out()
                    print(l_list, l_src)
                    flag_done = 1
                    break
        if flag_done == 0:
            num_src = l_src.split(',')[1]
            file_src = l_src.split(',')[2]
            cmd = 'git -C ' + repo_dir + ' blame -wL ' + num_src + ',' + num_src + ' ' + file_src
            res = subprocess.run(cmd, stdout=subprocess.PIPE)
            if str(res.stdout)[2] != '^':
                write_out()
                print('blame', l_src)
        flag_done = 0
