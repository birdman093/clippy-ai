from os import walk



#mypath = r"C:\Users\mbreau\source\repos\clippy-ai\frontend\Project.extension\lib\assets\clippy_blink"
#mypath = r"C:\Users\mbreau\source\repos\clippy-ai\frontend\Project.extension\lib\assets\clippy_error"
mypath = r"C:\Users\mbreau\source\repos\clippy-ai\frontend\Project.extension\lib\assets\clippy_excited"

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break


timer = 0.0

output_values = []

#frame_49_delay-0 .03s .png

for file in f:
    x = file.split("-")[1]
    duration_string = x[:-5]

    print('<DiscreteObjectKeyFrame KeyTime="0:0:{0}">'.format(timer))
    print('<DiscreteObjectKeyFrame.Value>')
    print('<BitmapImage UriSource="{0}\{1}" />'.format(mypath, file))
    print('</DiscreteObjectKeyFrame.Value>')
    print('</DiscreteObjectKeyFrame>')
    #print("\n\n\n")
    #duration_string = y
    #print("DURATION STRING: {0}".format(duration_string))
    #print("\n\n\n\n\n")

    duration_float = float(duration_string)
    timer += duration_float

    
    
