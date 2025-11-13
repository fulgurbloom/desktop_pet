#region To-do
    # Safer file handling (load once, then close)
        # Should be good but re-check everything
    # Safer error handling
        # Should be good but re-check everything
    # Fix 'NoneType' object has no attribute 'stop' on launch
    # Implement enum options for creating customized pets
#endregion

#region Imports
from PIL import Image
from screeninfo import get_monitors
import ctypes
import pystray
import threading
import tkinter as tk

import assets as py_assets
import pet as py_pet
#endregion

#region Global variables
global app_ctx

class AppContext():
    def __init__(self, root, canvas, pets, displays, tray_icon):
        self.root = root
        self.canvas = canvas
        self.pets = pets
        self.displays = displays
        self.tray_icon = tray_icon
#endregion

#region Tray icon methods
def setup_tray():
    global app_ctx
    
    try:
        icon_image = Image.open("assets\\images\\icon.png")
    except Exception as e:
        print(e)

    menu = pystray.Menu(
        pystray.MenuItem("Spawn", py_pet.spawn_pet(image_path="assets\\images\\cat.png", ctx=app_ctx)),
        pystray.MenuItem("Quit", quit_tray(ctx=app_ctx)),
    )

    tray_icon = pystray.Icon(
        name="deskpet name",
        icon=icon_image,
        title="deskpet",
        menu=menu,
    )
    
    app_ctx.tray_icon = tray_icon

def quit_tray(ctx):
    try:
        ctx.tray_icon.stop()
    except Exception as e:
        print(e)

    try:
        if ctx.root is not None:
            ctx.root.quit()
    except Exception as e:
        print(e)
#endregion

#region Window setup methods
def setup_canvas():
    global app_ctx

    app_ctx = AppContext(
        root=tk.Tk(),
        canvas=None,
        pets=[],
        displays=get_monitors(),
        tray_icon=None
    )
    
    # Setup transparent window
    app_ctx.root.overrideredirect(True)
    app_ctx.root.wm_attributes('-transparentcolor', 'white') # make white pixels transparent
    app_ctx.root.config(bg='white') # background color
    app_ctx.root.wm_attributes('-topmost', True) # always on top of all windows

    # Get window handle
    hwnd = ctypes.windll.user32.GetParent(app_ctx.root.winfo_id())

    # Set layered and transparent styles
    extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style | 0x80000 | 0x20)
    
    #region Setup canvas
    app_ctx.canvas = tk.Canvas(app_ctx.root, bg="white",
        width=app_ctx.displays[0].width, height=app_ctx.displays[0].height, highlightthickness=0)
    
    app_ctx.canvas.pack(fill="both")
    app_ctx.root.after(0, update_loop)
    #endregion
#endregion

#region Main loop
def main():
    global app_ctx
    
    setup_canvas()
    setup_tray()

    # run tray icon on separate thread since run is blocking
    if app_ctx.tray_icon is not None:
        threading.Thread(target=app_ctx.tray_icon.run, daemon=True).start()

    for i in range(0,8):
        py_pet.spawn_pet(app_ctx, image_path="assets\\images\\cat.png")

    py_assets.pet_to_json(app_ctx.pets[0])

    app_ctx.root.mainloop()

def update_loop():
    global app_ctx
    
    py_pet.update_pets(app_ctx)
    #p_root.after(20, py_pet.py_update_pets)
    
if __name__ == "__main__":
    main()
#endregion