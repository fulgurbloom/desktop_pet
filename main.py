# region To-do
# Safer file handling (load once, then close)
# Should be good but re-check everything
# Safer error handling
# Should be good but re-check everything
# DONE Fix 'NoneType' object has no attribute 'stop' on launch
# DONE Implement enum options for creating customized pets
# Add setup.py
# DONE Fix tray Quit not working
# Physics ("grounded" pets)
# endregion

# region Imports
from PIL import Image
from screeninfo import get_monitors
import ctypes
import pystray
import threading
import tkinter as tk

import assets as py_assets
import pet as py_pet

# endregion

# region Global variables
global app_ctx


class AppContext:
    def __init__(self, root, canvas, pets: py_pet.Pet, displays, tray_icon):
        self.root = root
        self.canvas = canvas
        self.pets = pets
        self.displays = displays
        self.tray_icon = tray_icon


# endregion


# region Tray icon methods
def setup_tray():
    global app_ctx

    try:
        icon_image = Image.open("assets\\images\\icon.png")
    except Exception as e:
        print(e)

    default_pet_config = py_pet.PetConfig(
        name="default",
        spawn_amount=1,
        move_speed=25,
        initial_position=[0, 0],
        initial_position_type=py_pet.InitialPositionType.RANDOMIZED,
        border_reaction_type=py_pet.BorderReactionType.BOUNCE,
        direction_type=py_pet.DirectionType.RANDOMIZED_ONCE,
        image_path="assets\\images\\cat.png",
        dialogue=[],
    )

    menu = pystray.Menu(
        pystray.MenuItem(
            "Spawn", py_pet.spawn_pet(app_ctx, pet_config=default_pet_config)
        ),
        pystray.MenuItem("Quit", quit_tray),
    )

    tray_icon = pystray.Icon(
        name="deskpet name",
        icon=icon_image,
        title="deskpet",
        menu=menu,
    )

    app_ctx.tray_icon = tray_icon


def quit_tray():
    global app_ctx

    try:
        app_ctx.root.quit()
    except Exception as e:
        print(e)


# endregion


# region Window setup methods
def setup_canvas():
    global app_ctx

    app_ctx = AppContext(
        root=tk.Tk(), canvas=None, pets=[], displays=get_monitors(), tray_icon=None
    )

    # Setup transparent window
    app_ctx.root.overrideredirect(True)
    app_ctx.root.wm_attributes(
        "-transparentcolor", "white"
    )  # make white pixels transparent
    app_ctx.root.config(bg="white")  # background color
    app_ctx.root.wm_attributes("-topmost", True)  # always on top of all windows

    # Get window handle
    hwnd = ctypes.windll.user32.GetParent(app_ctx.root.winfo_id())

    # Set layered and transparent styles
    extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style | 0x80000 | 0x20)

    # region Setup canvas
    app_ctx.canvas = tk.Canvas(
        app_ctx.root,
        bg="white",
        width=app_ctx.displays[0].width,
        height=app_ctx.displays[0].height,
        highlightthickness=0,
    )

    app_ctx.canvas.pack(fill="both")
    app_ctx.root.after(0, update_loop)
    # endregion


# endregion


# region Main loop
def spawn_test_pets():
    config_options = py_pet.PetConfig(
        name="test pet",
        spawn_amount=32,
        initial_position=[128, 128],
        move_speed=0,
        initial_position_type=py_pet.InitialPositionType.RANDOMIZED,
        border_reaction_type=py_pet.BorderReactionType.BOUNCE,
        direction_type=py_pet.DirectionType.RANDOMIZED_ONCE,
        image_path="assets\\images\\cat.png",
        dialogue=None,
    )

    for i in range(0, config_options.spawn_amount):
        py_pet.spawn_pet(app_ctx, pet_config=config_options)


def main():
    global app_ctx

    setup_canvas()
    setup_tray()

    # run tray icon on separate thread since run is blocking
    if app_ctx.tray_icon is not None:
        threading.Thread(target=app_ctx.tray_icon.run, daemon=True).start()

    spawn_test_pets()

    py_assets.pet_to_json(app_ctx.pets[0])

    app_ctx.root.mainloop()


def update_loop():
    global app_ctx

    py_pet.update_pets(app_ctx)


if __name__ == "__main__":
    main()
# endregion
