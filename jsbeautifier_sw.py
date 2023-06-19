import jsbeautifier
import os


filename1 = "service_worker_scripts"
filename2 = "sw_beautified"

for filename in os.listdir(filename1):
    if filename.endswith('.js'):

        #print(filename[:-3])
        file_path = os.path.join(filename1,filename)
        with open(file_path, "r") as f:
            contents = f.read()
            content1 = jsbeautifier.beautify(contents)
            sw_beauty = f"sw_beautified/{filename[:-3]}.js"
            with open(sw_beauty, "w") as g:                
                g.write(content1)


