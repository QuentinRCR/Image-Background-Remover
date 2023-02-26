from PIL import Image
import PySimpleGUI as sg
import os.path


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def removeBackground(opacity, colorToRemove, colorToAdd, path, margin):

    windowsPath = path[2:]  # jpg ou png

    if(colorToAdd==""):
        colorToAdd="#ffffff" # in case the second color is not defined

    colorToRemove = hex_to_rgb(colorToRemove)
    colorToAdd = hex_to_rgb(colorToAdd)

    colorToAdd.append(int(opacity * 255))  # to add the opacity component to the rgb form

    img = Image.open(windowsPath)

    rgba = img.convert("RGBA")

    datas = rgba.getdata()
    newData = []

    for image in datas:
        if ((image[0] >= colorToRemove[0] - margin) and (image[0] <= colorToRemove[0] + margin) and (
                image[1] >= colorToRemove[1] - margin) and (image[1] <= colorToRemove[1] + margin) and (
                image[2] >= colorToRemove[2] - margin) and (image[2] <= colorToRemove[2] + margin)):
            newData.append((colorToAdd[0], colorToAdd[1], colorToAdd[2], colorToAdd[3]))
        else:
            newData.append(image)

    rgba.putdata(newData)

    rgba.save(windowsPath[:-4] + "-modified.png", "PNG")

def removeTemporaryFiles():
    try:  # delete temporaries files
        os.remove(folderPath + "/temps.png")
        os.remove(folderPath + "/temps2.png")
    except:
        pass


folderPath = None

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(70, 30), key="-FILE LIST-"
        )
    ],
    [
        sg.Text("Chose opacity of the final replaced pixels"),
        sg.Slider((0, 1), 0, 0.01, 0.5, 'horizontal', False, size=(20, 10), key="-OPACITY-", enable_events=True)
    ],
    [
        sg.Input(key="-REMOVE_COLOR-"),
        sg.ColorChooserButton("Removed color")
    ],
    [
        sg.Input(key="-NEW_COLOR-"),
        sg.ColorChooserButton("New color")
    ],
    [
        sg.Slider((0, 250), 15, 1, 50, 'horizontal', False, key="-MARGIN-")
    ],
    [
        sg.Button("Execute")
    ]
]


# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Image(key="-MODIFIED_IMAGE-")],
    [sg.HSeparator()],
    [sg.Image(key="-IMAGE-")]

]


# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


window = sg.Window("Background remover", layout)


# Run the Event Loop
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        removeTemporaryFiles(); #every time we change folder

        folderPath = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folderPath)
        except:
            file_list = []

        # Remove all not wanted extension with a comprehension for
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folderPath, f))
            and f.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))
        ]
        window["-FILE LIST-"].update(fnames)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            img = Image.open(filename);
            img.thumbnail((500, 500))
            img.save(values["-FOLDER-"]+"/temps.png")
            window["-IMAGE-"].update(filename=values["-FOLDER-"]+"/temps.png")
        except:
            pass

    # call the function when push execute
    elif event == "Execute":
        removeBackground(values["-OPACITY-"],
                         values["-REMOVE_COLOR-"],
                         values["-NEW_COLOR-"],
                         os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0]),
                         values["-MARGIN-"]
                         )
        filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])[:-4] + "-modified.png"
        img1 = Image.open(filename)
        img1.thumbnail((500, 500))
        img1.save(values["-FOLDER-"] + "/temps2.png")
        window["-MODIFIED_IMAGE-"].update(filename=values["-FOLDER-"] + "/temps2.png")


removeTemporaryFiles()
window.close()


