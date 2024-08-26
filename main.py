# Imports
import os
import shutil
import sys
import zipfile
from tkinter import filedialog, Tk

import requests
from pyunpack import Archive

# Initial setup where the user inputs their console and other information
print("Homebrew SD manager v0.3")
print("Please type the number to select a console to homebrew:")
print("1 - 3DS")
# DO NOT USE THIS YET print("2 - Switch")
print("3 - DSi")
print("4 - Wii U")

console_selected = False

while not console_selected:
    brew = int(input())
    if brew == 1:
        print("Are you using a new 3DS (type n) or old 3DS (type o)?")
        while True:
            version = input()
            if version == "n":
                print(
                    "What is your console region? (You can find this in System Settings as the last letter in the "
                    "version number.)")
                while True:
                    region = input()
                    if region in ["E", "K", "J"]:
                        print("Setting to", region, "region.")
                        break
                    elif region in ["U"]:
                        print("Are the last 2 digits of your console version '50'? (y/n)")
                        ver = input()
                        if ver == "y":
                            region = "U1"
                            break
                        elif ver == "n":
                            region = "U2"
                            break
                        else:
                            print("Please type 'y' or 'n'.")
                    else:
                        print("That region is invalid, please type E, U, K, or J.")
                console = "n3ds"
                print("Setting to new 3DS mode. Please update the console to the latest firmware.")
                console_selected = True  # Set the flag to true to exit the outer loop
                break  # Exit the inner loop

            elif version == "o":
                print("Please visit https://3ds.hacks.guide/installing-boot9strap-(mset9-cli) to continue with homebrew"
                      " on this path.")
                exit()  # Exit if old 3DS is selected
            else:
                print("Please type 'n' or 'o' to select the model.")

    elif brew == 2:
        print(
            "Please check to see if your serial number is unpatched at "
            "https://gbatemp.net/threads/switch-informations-by-serial-number-read-the-first-post-before-asking-questions"
            ".481215/.")
        print("If your switch is unpatched, press Enter to continue.")
        input()
        print("Setting to Switch mode. Please update the console to the latest firmware.")
        console = "nx"
        console_selected = True  # Set the flag to true to exit the outer loop
        break

    elif brew == 3:
        console = "ds"
        print("Setting to DSi mode. Please update the console to the latest firmware.")
        console_selected = True  # Set the flag to true to exit the outer loop
        break

    elif brew == 4:
        console = "wiiu"
        print("Setting to Wii U mode. Please update the console to the latest firmware.")
        console_selected = True  # Set the flag to true to exit the outer loop
        break

    else:
        print("Please type an integer between 1 and 4.")

# Proceed to the SD card selection and deletion regardless of the console selected
root = Tk()
root.withdraw()
print("Please select the SD card to be used.")
folder = filedialog.askdirectory(title="Select Directory to Extract Files To", initialdir="/Users/12368/pytest")

if folder:
    sd_path = folder

    for filenameCTR in os.listdir(sd_path):
        file_pathCTR = os.path.join(sd_path, filenameCTR)
        try:
            # Check if it's a file and remove it
            if os.path.isfile(file_pathCTR) or os.path.islink(file_pathCTR):
                os.unlink(file_pathCTR)
            # Check if it's a directory and remove it
            elif os.path.isdir(file_pathCTR):
                shutil.rmtree(file_pathCTR)
        except Exception as e:
            print(f"Failed to delete {file_pathCTR}. Reason: {e}")

else:
    print("No directory selected. Exiting...")
    exit()

print("Files may take a while to download, please be patient.")


# Script functions
def n3ds():
    # Downloading required files
    urls = [
        "https://github.com/zoogie/super-skaterhax/releases/download/latest/release_new3ds_v1.1.zip",
        "https://github.com/d0k3/SafeB9SInstaller/releases/download/latest/SafeB9SInstaller-20170605-122940.zip",
        "https://github.com/SciresM/boot9strap/releases/download/latest/boot9strap-1.4.zip",
        "https://github.com/luigoalma/nimdsphax/releases/download/latest/nimdsphax_v1.0.zip",
        "https://github.com/LumaTeam/Luma3DS/releases/download/latest/Luma3DSv13.1.2.zip",
    ]

    for url in urls:
        name = url.split("/")[-1]
        path = os.path.join(sd_path, name)

        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            print("Downloading %s" % name)
            response = requests.get(url, stream=True, allow_redirects=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("File", name, "downloaded to", sd_path)

        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(sd_path)
        print(name, "extracted to", sd_path)

        os.remove(path)
        print(name, "was removed")

    # Initial clean up of files
    rm = [
        "arm9.bin",
        "arm11.bin",
        "Launcher.dat",
        "README.md",
        "SafeB9SInstaller.dat",
        "SafeB9SInstaller.firm",
        "SafeB9SInstaller.nds"
    ]

    for file in rm:
        os.remove(os.path.join(sd_path, file))

    shutil.rmtree(os.path.join(sd_path, "config"))
    print("Cleaned up files")

    os.mkdir(os.path.join(sd_path, "3ds"))
    os.mkdir(os.path.join(sd_path, "boot9strap"))

    # Region-dependent file moving
    region_data = {
        "E": {
            "folder": "EUROPE (11.17.0-50E, 11.16.0-49E, 11.15.0-47E)",
            "files": [
                "arm11code.bin",
                "browserhax_hblauncher_ropbin_payload.bin"
            ]
        },
        "J": {
            "folder": "JAPAN (11.17.0-50J, 11.16.0-49J, 11.15.0-47J)",
            "files": [
                "arm11code.bin",
                "browserhax_hblauncher_ropbin_payload.bin"
            ]
        },
        "U2": {
            "folder": "USA (11.16.0-49U, 11.15.0-47U)",
            "files": [
                "arm11code.bin",
                "browserhax_hblauncher_ropbin_payload.bin"
            ]
        },
        "K": {
            "folder": "KOREA (11.16.0-42K, 11.15.0-40K)",
            "files": [
                "arm11code.bin",
                "browserhax_hblauncher_ropbin_payload.bin"
            ]
        },
        "U1": {
            "folder": "USA (11.17.0-50U)",
            "files": [
                "arm11code.bin",
                "browserhax_hblauncher_ropbin_payload.bin"
            ]
        }
    }

    # Function to handle file operations for a given region
    def process_region(selected_region):
        if selected_region in region_data:
            region_info = region_data[selected_region]

            # Move the relevant files
            for file_name in region_info["files"]:
                shutil.move(os.path.join(sd_path, region_info["folder"], file_name), os.path.join(sd_path, file_name))

            shutil.rmtree(os.path.join(sd_path, region_info["folder"]), ignore_errors=True)

            # Remove other region folders
            for reg in region_data:
                if reg != selected_region:
                    shutil.rmtree(os.path.join(sd_path, region_data[reg]["folder"]), ignore_errors=True)

            print(f"Processed region {selected_region}")
        else:
            print(f"Region {selected_region} is not recognized")

    # Execute function for the selected region
    process_region(region)

    # Moving files and final setup
    shutil.move(os.path.join(sd_path, "boot9strap.firm"), os.path.join(sd_path, "boot9strap", "boot9strap.firm"))
    shutil.move(os.path.join(sd_path, "boot9strap.firm.sha"),
                os.path.join(sd_path, "boot9strap", "boot9strap.firm.sha"))
    shutil.rmtree(os.path.join(sd_path, "SafeB9SInstaller")),

    print("Your SD card has been set up successfully. Please view the guide at "
          "https://3ds.hacks.guide/installing-boot9strap-(super-skaterhax)#section-ii---super-skaterhax to continue "
          "the homebrew method.")


def nx():
    # Selecting the directory to save the payload
    print("Please select a directory to save the payload to.")
    load = filedialog.askdirectory(title="Select Directory to Extract Files To", initialdir="/Users/12368/pytest")
    if load:
        desktop = load

        for filenameNX in os.listdir(desktop):
            file_path_nx = os.path.join(desktop, filenameNX)
            try:
                # Check if it's a file and remove it
                if os.path.isfile(file_path_nx) or os.path.islink(file_path_nx):
                    os.unlink(file_path_nx)
                # Check if it's a directory and remove it
                elif os.path.isdir(file_path_nx):
                    shutil.rmtree(file_path_nx)
            except Exception as expt:
                print(f"Failed to delete {file_path_nx}. Reason: {expt}")
            if not os.path.isdir:
                os.mkdir(os.path.join(desktop, "payload"))

    else:
        print("No directory selected. Exiting...")
        exit()
    # Downloading required files
    urls = [
        "https://github.com/eliboa/TegraRcmGUI/releases/download/latest/TegraRcmGUI_v2.6_Installer.msi",
        "https://github.com/CTCaer/hekate/releases/download/latest/hekate_ctcaer_6.2.1_Nyx_1.6.3.zip",
        "https://github.com/pbatard/libwdi/releases/download/latest/zadig-2.9.exe"
    ]

    for url in urls:
        name = url.split("/")[-1]
        path = os.path.join(desktop, name)

        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            print("Downloading %s" % name)
            response = requests.get(url, stream=True, allow_redirects=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("File", name, "downloaded to", desktop)

        if name.endswith(".zip"):
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(desktop)
            print(name, "extracted to", desktop)

            os.remove(path)
            print(name, "was removed")

    shutil.move(desktop + "/bootloader", sd_path + "/bootloader")
    os.mkdir(os.path.join(sd_path, "switch"))
    # Asking for user input on target device to continue
    print(
        "Please use the guide at https://switch.hacks.guide/user_guide/rcm/entering_rcm/ to enter RCM and to inject a "
        "payload before continuing.")
    input("Press Enter to continue...")
    print(
        "At this point you should be ready to choose between emuMMC and sysMMC. Please reinsert the SD card, "
        "and then type E for emuMMC or S for sysmmc.")
    mmc = input()

    print("Please follow the next page and press enter when you are done.")
    input()
    # More downloading
    urls = [
        "https://switch.hacks.guide/files/emu/hekate_ipl.ini",
        "https://switch.hacks.guide/files/emummc.txt",
        "https://switch.hacks.guide/files/bootlogos.zip",
        "https://github.com/Atmosphere-NX/Atmosphere/releases/download/latest/atmosphere-1.7.1-master-39c201e37"
        "+hbl-2.4.4+hbmenu-3.6.0.zip",
        "https://github.com/mtheall/ftpd/releases/download/latest/ftpd.nro",
        "https://github.com/J-D-K/JKSV/releases/download/latest/JKSV.nro",
        "https://github.com/exelix11/SwitchThemeInjector/releases/download/latest/NXThemesInstaller.nro",
        "https://github.com/joel16/NX-Shell/releases/download/latest/NX-Shell.nro",
        "https://github.com/XorTroll/Goldleaf/releases/download/latest/Goldleaf.nro"
    ]

    for url in urls:
        name = url.split("/")[-1]
        path = os.path.join(sd_path, name)

        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            print("Downloading %s" % name)
            response = requests.get(url, stream=True, allow_redirects=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("File", name, "downloaded to", sd_path)

        if name.endswith(".zip"):
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(sd_path)
            print(name, "extracted to", sd_path)
            os.remove(path)
            print(name, "was removed")
        elif name.endswith(".nro"):
            shutil.move(sd_path + "/" + name, sd_path + "/switch/" + name)

    # File cleanup
    shutil.move(sd_path + "/hekate_ipl.ini", sd_path + "/bootloader/hekate_ipl.ini")
    os.mkdir(sd_path + "/atmosphere/hosts")
    shutil.move(sd_path + "/emummc.txt", sd_path + "/atmosphere/hosts/emummc.txt")
    # Moving Nintendo folder if emuMMC was chosen
    if mmc == "E":
        if os.path.isdir(sd_path + "/Nintendo"):
            shutil.copytree(sd_path + "/Nintendo", sd_path + "/emuMMC/RAW1/Nintendo")
            print("Copied Nintendo folder to the emuMMC.")

    print("Your SD card has been set up! Please continue to follow the guide from "
          "https://switch.hacks.guide/user_guide/all/making_essential_backups/."),


def ds():
    urls = [
        "https://github.com/DS-Homebrew/TWiLightMenu/releases/latest/download/TWiLightMenu-DSi.7z",
        "https://github.com/zoogie/dumpTool/releases/latest/download/dumpTool.nds"
    ]

    for url in urls:
        name = url.split("/")[-1]
        path = os.path.join(sd_path, name)

        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            print("Downloading %s" % name)
            response = requests.get(url, stream=True, allow_redirects=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("File", name, "downloaded to", sd_path)

        if name.endswith(".7z"):
            Archive(path).extractall(sd_path)
            print(name, "extracted to", sd_path)

            os.remove(path)
            print(name, "was removed")
    print("Your SD card has been setup, please continue the guide from "
          "https://dsi.cfw.guide/get-started.html#section-ii-selecting-an-exploit.")


def wiiu():
    urls = [
        "https://aroma.foryour.cafe/api/download?packages=environmentloader,wiiu-nanddumper-payload",
        "https://aroma.foryour.cafe/api/download/base"
    ]

    for url in urls:
        # Force the filename to end with .zip
        name = "downloaded_file.zip"
        path = os.path.join(sd_path, name)

        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            print("Downloading %s" % name)
            response = requests.get(url, stream=True, allow_redirects=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("File", name, "downloaded to", sd_path)

        if name.endswith(".zip"):
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(sd_path)
            print(name, "extracted to", sd_path)
            os.remove(path)
            print(name, "was removed")

    print("Your SD card has been setup, please continue the guide from "
          "https://wiiu.hacks.guide/#/aroma/browser-exploit.")


# Using the functions for each console
# noinspection PyUnboundLocalVariable
if console == "n3ds":
    n3ds()
elif console == "nx":
    # nx()
elif console == "ds":
    ds()
elif console == "wiiu":
    wiiu()
else:
    exit()
