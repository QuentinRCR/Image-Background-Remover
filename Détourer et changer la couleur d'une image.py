from PIL import Image
#import PySimpleGUI as sg


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


#sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

colorToRemove = "ffffff"  # possible to specify using rgb in a list or in hexadecimal with "#00784d"
colorToAdd = "ffffff"  # possible to specify using rgb in a list or in hexadecimal with "#00784d"
opacity = 0
margin = 250


windowsPath = "C:/Users/quent/Desktop/dégradé de médaille automne 2021.png"[2:]  # jpg ou png
# changer les / par des / avec ctrl+r


if type(colorToRemove) is str:
    colorToRemove = hex_to_rgb(colorToRemove)

if type(colorToAdd) is str:
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
