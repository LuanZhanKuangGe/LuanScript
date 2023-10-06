import argparse
import subprocess
from gooey import Gooey, GooeyParser


@Gooey(program_name="TDL SAMPLE GUI", default_size=(1920, 1080))
def main():
    parser = GooeyParser(description="Enter a string and an integer")
    parser.add_argument("url", help="Enter a telegram url")
    parser.add_argument("count", type=int, help="Enter an integer", default=1)

    args = parser.parse_args()

    url = args.url.split("?")[0]
    count = int(args.count)

    command = r"C:\Softwares\tdl_Windows_64bit\tdl.exe dl -n quickstart -d C:\Users\zhoub\Downloads"

    command += f" -u {url}"

    for i in range(1, count):
        sub_url = ("/").join(url.split("/")[0:-1])
        sub_index = int(url.split("/")[-1])
        command += f" -u {sub_url}/{sub_index+i}"

    subprocess.run(command)

    print(f"{command} done!!!")

if __name__ == "__main__":
    main()
