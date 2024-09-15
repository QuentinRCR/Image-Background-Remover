import os
import numpy as np
from PIL import Image
import FreeSimpleGUI as sg

# Convert hex color code to RGB format
def hex_to_rgb(value):
    value = value.lstrip('#')
    return [int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)]

# Function to remove the background color and replace it with a new color with specified opacity
def remove_background(opacity, color_to_remove, color_to_add, path, margin):
    # Convert hex colors to RGB and add opacity to the new color
    color_to_remove = hex_to_rgb(color_to_remove)
    color_to_add = hex_to_rgb(color_to_add) + [int(opacity * 255)]

    # Open the image and convert to RGBA
    img = Image.open(path[2:]).convert("RGBA")
    img_array = np.array(img)

    # Calculate color difference and create a mask based on margin
    color_diff = np.abs(img_array[..., :3] - color_to_remove)
    mask = np.all(color_diff <= margin, axis=-1)

    # Apply the new color to the masked pixels
    img_array[mask] = color_to_add

    # Save the modified image as a PNG
    Image.fromarray(img_array).save(path[:-4] + "-modified.png", "PNG")

# Function to remove temporary files generated during processing
def remove_temp_files():
    # List of temporary files to remove
    for temp_file in ["temps.png", "temps2.png"]:
        try:
            os.remove(os.path.join(values["-FOLDER-"], temp_file))
        except FileNotFoundError:
            pass

# Function to update the list of image files in the folder
def update_image_list(selected_image=None):
    remove_temp_files()  # Clean up temp files before updating list

    # Get and filter list of image files in the folder
    image_files = [
        f for f in sorted(os.listdir(values["-FOLDER-"]), reverse=os.path.basename(values["-FOLDER-"]) == "Screenshots")
        if os.path.isfile(os.path.join(values["-FOLDER-"], f)) and f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # Update the listbox with the image files
    window["-FILE LIST-"].update(image_files)

    # If an image is selected, keep it highlighted
    if selected_image:
        window["-FILE LIST-"].set_value(selected_image)

# Get the full path of the selected image
def get_selected_image_path():
    return os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])

# Get the default folder path for screenshots
def get_screenshot_folder():
    return os.path.join(os.path.expanduser("~"), r'Pictures\Screenshots')

# Return the layout of the gui
def get_layout(default_folder_path,default_remove_color,default_add_color,default_opacity,default_margin):
    # Left-side column with folder selection and image list
    file_list_column = [
        [sg.Text("Image Folder"), sg.In(size=(25, 1), enable_events=True, key="-FOLDER-", default_text=default_folder_path), sg.FolderBrowse()],
        [sg.Listbox(values=[], enable_events=True, size=(70, 30), key="-FILE LIST-")],
        [sg.Text("Opacity"), sg.Slider((0, 1), default_opacity, 0.01, orientation='horizontal', key="-OPACITY-")],
        [sg.Input(key="-REMOVE_COLOR-", default_text=default_remove_color), sg.ColorChooserButton("Removed color")],
        [sg.Input(key="-NEW_COLOR-", default_text=default_add_color), sg.ColorChooserButton("New color")],
        [sg.Text("Margin"), sg.Slider((0, 250), default_margin, 1, orientation='horizontal', key="-MARGIN-")],
        [sg.Button("Execute")]
    ]

    # Right-side column with image preview
    image_viewer_column = [
        [sg.Image(key="-MODIFIED_IMAGE-")],  # Display the modified image
        [sg.HSeparator()],                   # Horizontal separator
        [sg.Image(key="-IMAGE-")]            # Display the original image
    ]

    # Full window layout
    layout = [
        [sg.Column(file_list_column), sg.VSeperator(), sg.Column(image_viewer_column)]
    ]

    return layout



# Initialize window
layout = get_layout(get_screenshot_folder(),'#f7f7f7','#ffffff',0,15)
window = sg.Window("Background Remover", layout, relative_location=(-200,-50))
event, values = window.read(timeout=0)  # Initial read to handle default behaviors
update_image_list() # Populate the image list at startup

# Event loop to handle GUI interactions
while True:
    event, values = window.read()

    # Close the window if Exit or close button is pressed
    if event in ("Exit", sg.WIN_CLOSED):
        break

    # Update the folder path and image list if a new folder is selected
    if event == "-FOLDER-":
        update_image_list()

    # Display the selected image in the image viewer
    elif event == "-FILE LIST-":
        try:
            img = Image.open(get_selected_image_path())
            img.thumbnail((500, 500))  # Resize image to fit
            img.save(os.path.join(values["-FOLDER-"], "temps.png"))  # Save a temporary resized version
            window["-IMAGE-"].update(filename=os.path.join(values["-FOLDER-"], "temps.png"))
        except:
            pass

    # Execute background removal when the button is clicked
    elif event == "Execute":
        remove_background(
            values["-OPACITY-"], values["-REMOVE_COLOR-"], values["-NEW_COLOR-"],
            get_selected_image_path(), values["-MARGIN-"]
        )

        # Load and display the modified image
        img1 = Image.open(get_selected_image_path()[:-4] + "-modified.png")
        img1.thumbnail((500, 500))  # Resize the modified image
        img1.save(os.path.join(values["-FOLDER-"], "temps2.png"))
        window["-MODIFIED_IMAGE-"].update(filename=os.path.join(values["-FOLDER-"], "temps2.png"))

        # Update the image list and keep the selected image highlighted
        update_image_list(selected_image=values["-FILE LIST-"])

# Clean up temp files and close the window when exiting
window.close()
