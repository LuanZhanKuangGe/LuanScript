import argparse
import subprocess
from gooey import Gooey, GooeyParser


@Gooey(program_name="TDL SAMPLE GUI", default_size=(1920, 1080))
def main():
    parser = GooeyParser(description="Enter a string and an integer")
    parser.add_argument("url", help="Enter a telegram url")
    parser.add_argument("count", type=int, help="Enter an integer", default=1)

    args = parser.parse_args()

    count = int(args.count)

    command = r"C:\Softwares\tdl_Windows_64bit\tdl.exe dl"

    

    if 'comment=' in args.url:
        url = args.url
        start = int(url.split("comment=")[1])
        stop =  start + count
        for i in range(start, stop):
            sub_url = url.split("comment=")[0]
            subprocess.run(command + f" -u {sub_url}comment={i}")
            print(f"{command} done!!!")
    else:
        url = args.url.split("?")[0]
        command += f" -u {url}"
        for i in range(1, count):
            sub_url = ("/").join(url.split("/")[0:-1])
            sub_index = int(url.split("/")[-1])
            command += f" -u {sub_url}/{sub_index+i}"

        command += r" --continue -d C:\Users\zhoub\Downloads"

        subprocess.run(command)

        print(f"{command} done!!!")

if __name__ == "__main__":
    main()
