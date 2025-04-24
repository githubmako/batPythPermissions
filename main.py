import os
import subprocess 
from tempfile import gettempdir 

def grupy():
    folders = input("Provide folder paths (ex: F:\ak_collection): ").split()

    tmp_acl = os.path.join(gettempdir(), "_acl_lines.txt")
    tmp_grp = os.path.join(gettempdir(), "_grupy_all.txt")

    for tmp_file in [tmp_acl,tmp_grp]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
    

    for folder in folders:
        if os.path.exists(folder):
            print(f"Processing: {folder}")
            with open (tmp_acl,"w") as acl_file:
                subprocess.run(["icacls", folder], stdout = acl_file, text = True)



            with open(tmp_acl, "r") as acl_file, open(tmp_grp, "a") as grp_file:
                for line in acl_file:
                    if "\\" in line:
                        group = line.split("\\")[1].split(":")[0]
                        grp_file.write(group + "\n")
            
        else:
            print("Folder doesnt't exist: {folder}")
    

    groups = set()
    if os.path.exists(tmp_grp):
        with open (tmp_grp,"r") as grp_file:
            groups = sorted(set(line.strip() for line in grp_file if line.strip()))

    print("============SUMMARY============")
    for i, group in enumerate(groups, start = 1):
        print("----------")
        subprocess.run(["net", "group", group, "/domain"], text = True, stderr=subprocess.DEVNULL)
        print("\n")
       
if __name__ == "__main__":
    grupy()




