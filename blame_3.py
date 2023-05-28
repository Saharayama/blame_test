import re
import subprocess

SRC_FILE = r"./src.txt"
LIST_FILE = r"./list.txt"
OUT_FILE = r"./out.txt"
REPO_DIR = r"D:\Desktop\settings"
BASE_COMMIT = "@~"


def write_out(l: str) -> None:
    with open(OUT_FILE, "a", encoding="utf-8") as f_out:
        f_out.write(l)
        f_out.write("\n")


def get_base_commit_time() -> int:
    cmd = "git -C " + REPO_DIR + " log -1 " + BASE_COMMIT + " --date=unix | grep Date:"
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return int(str(res.stdout)[10:-3])


def get_commit_time(num: str, file: str) -> int:
    cmd = (
        "git -C "
        + REPO_DIR
        + " blame -pwL "
        + num
        + ","
        + num
        + " "
        + file
        + " | grep author-time"
    )
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return int(str(res.stdout)[14:-3])


base_commit_time: int = get_base_commit_time()

with open(LIST_FILE, "r", encoding="utf-8") as f_list:
    l_all_list: str = ""
    for l_list in f_list:
        l_list = l_list.rstrip()
        if l_list != "":
            l_all_list += l_list
            l_all_list += "|"
        else:
            continue
    l_all_list = l_all_list[:-1]

with open(SRC_FILE, "r", encoding="utf-8") as f_src:
    for l_src in f_src:
        l_src = l_src.rstrip()
        if l_src != "":
            if re.findall(l_all_list, l_src):
                write_out(l_src)
            else:
                num_src = l_src.split(",")[1]
                file_src = l_src.split(",")[2]
                commit_time = get_commit_time(num_src, file_src)
                if commit_time > base_commit_time:
                    write_out(l_src)
                    print("blame", l_src)
