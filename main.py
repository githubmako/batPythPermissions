import os
import subprocess 
import json
from tempfile import gettempdir 
from pathlib import Path


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

def uprawnienia():
 
    folders = input("Provide folder paths separated by spaces (ex: F:\\ak_collection G:\\test): ").split()
    
    
    raw_json_path = Path.home() / "Desktop" / "uprawnienia.json"
    final_json_path = Path.home() / "Desktop" / "uprawnienia_parsed.json"
    tmp_acl_path = Path(gettempdir()) / "_acl_lines.txt"

    
    for file_path in [tmp_acl_path, raw_json_path, final_json_path]:
        if file_path.exists():
            file_path.unlink()

    raw_json_data = []

 
    for folder in folders:
        if os.path.exists(folder):
            print(f"Processing: {folder}")

           
            with open(tmp_acl_path, "w") as acl_file:
                subprocess.run(["icacls", folder], stdout=acl_file, text=True)

          
            with open(tmp_acl_path, "r") as acl_file:
                acl_lines = [line.strip() for line in acl_file if line.strip()]

            
            raw_json_data.append({
                "Path": folder,
                "Acl": acl_lines
            })
        else:
            print(f"Folder doesn't exist: {folder}")

  
    with open(raw_json_path, "w", encoding="utf-8") as raw_json_file:
        json.dump(raw_json_data, raw_json_file, indent=4)

  
    final_json_data = []
    for entry in raw_json_data:

        filtered_acl = [line for line in entry["Acl"] if "Successfully processed" not in line]
        final_json_data.append({
            "Path": entry["Path"],
            "Acl": filtered_acl
        })

    
    with open(final_json_path, "w", encoding="utf-8") as final_json_file:
        json.dump(final_json_data, final_json_file, indent=4)

    print(f"Processing complete. Check the files:\nRaw JSON: {raw_json_path}\nFinal JSON: {final_json_path}")

if __name__ == "__main__":
    uprawnienia()