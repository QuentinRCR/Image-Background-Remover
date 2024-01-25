from PIL import Image
import PySimpleGUI as sg
import os.path
import numpy as np
import matplotlib.pyplot as plt


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def removeBackground(opacity, colorToRemove, colorToAdd, path, margin):

    windowsPath = path[2:]  # jpg ou png

    if(colorToAdd==""):
        colorToAdd="#ffffff" # in case the second color is not defined
    if(colorToRemove==""):
        colorToRemove="#f7f7f7" # in case the second color is not defined
    colorToRemove = hex_to_rgb(colorToRemove)
    colorToAdd = hex_to_rgb(colorToAdd)
    colorToAdd.append(int(opacity * 255))  #to add the opacity component to the rgb form

    imgToConvert = Image.open(windowsPath)
    rgba = imgToConvert.convert("RGBA") # convert any format to rbga

    img_array = np.array(rgba)

    # Calculate the absolute difference between the image array and the target color
    color_difference = np.abs(img_array[..., :3] - colorToRemove)

    # Create a mask for the target color within the tolerance range
    mask = np.all(color_difference <= margin, axis=-1)

    #update the color
    img_array[mask] = colorToAdd

    rgba = Image.fromarray(img_array)

    # save the new version
    rgba.save(windowsPath[:-4] + "-modified.png", "PNG")

def removeTemporaryFiles():
    try:  # delete temporaries files
        os.remove(folderPath + "/temps.png")
        os.remove(folderPath + "/temps2.png")
    except:
        pass

def update_image_list():
    removeTemporaryFiles() #To avoid leaving temporarily files if we change folder without quiting the app

    # Get list of files in folder
    file_list = os.listdir(folderPath)

    # Remove all not wanted extension with a comprehension for
    imageFiles = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folderPath, f))
        and f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    window["-FILE LIST-"].update(imageFiles)

# define the path to the image displayed
folderPath = None

# defines the elements that goes on the left of the window
file_list_column = [
    [ #select the folder
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [ #displays the image elements inside the folder
        sg.Listbox(
            values=[], enable_events=True, size=(70, 30), key="-FILE LIST-"
        )
    ],
    [
        sg.Text("Chose opacity of the final replaced pixels"),
        sg.Slider((0, 1), 0, 0.01, 0.5, 'horizontal', False, size=(20, 10), key="-OPACITY-", enable_events=True)
    ],
    [ #choose the color that need to be removed
        sg.Input(key="-REMOVE_COLOR-"),
        sg.ColorChooserButton("Removed color")
    ],
    [ #chose the color to replace the missing pixels
        sg.Input(key="-NEW_COLOR-"),
        sg.ColorChooserButton("New color")
    ],
    [ #defines the margin to get all the pixels
        sg.Text("Margin"),
        sg.Slider((0, 250), 15, 1, 50, 'horizontal', False, key="-MARGIN-")
    ],
    [
        sg.Button("Execute")
    ]
]


# Defines images on the right
image_viewer_column = [
    [sg.Image(key="-MODIFIED_IMAGE-")], #displays the modified image
    [sg.HSeparator()],
    [sg.Image(key="-IMAGE-")]

]


# Defines the full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


# Opens the window
window = sg.Window("Background remover", layout)


# Run the Event Loop
while True:
    # reads if there is any new event
    event, values = window.read()

    #if the window is closed, break the loop
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was chosen, make a list of files in the folder
    if event == "-FOLDER-":
        folderPath = values["-FOLDER-"]
        update_image_list()

    # A file was chosen from the listbox
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )

            # Resize the image to have a constant window and change the file
            # from jpg to png so that the image is displayed
            img = Image.open(filename)
            img.thumbnail((500, 500))
            img.save(values["-FOLDER-"]+"/temps.png")

            #update the value of the image
            window["-IMAGE-"].update(filename=values["-FOLDER-"]+"/temps.png")
        except:
            pass

    # call the function when button execute is pressed
    elif event == "Execute":
        removeBackground(values["-OPACITY-"],
                         values["-REMOVE_COLOR-"],
                         values["-NEW_COLOR-"],
                         os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0]),
                         values["-MARGIN-"]
                         )


        filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])[:-4] + "-modified.png"

        # Resize the image to have a constant window and change the file
        # from jpg to png so that the image is displayed
        img1 = Image.open(filename)
        img1.thumbnail((500, 500))
        img1.save(values["-FOLDER-"] + "/temps2.png")

        #update the result image to know what the image looks like
        window["-MODIFIED_IMAGE-"].update(filename=values["-FOLDER-"] + "/temps2.png")

        update_image_list()


removeTemporaryFiles() #to remove temp files before closing the window
window.close()


