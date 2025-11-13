#region To-do
    # Safer file handling (load once, then close)
    # Safer error handling
#endregion

#region Imports
from PIL import Image, ImageTk
from screeninfo import get_monitors
import ctypes
import numpy
import pystray
import random
import threading
import tkinter as tk
#endregion

#region Global variables
p_root = None
p_canvas = None
p_pets = []
p_display_size = None
p_icon = None
#endregion

#region Testing methods
def debug_init():
    """
    Initialize test pet and bind mouse events
    """
    global p_pets
    global p_display_size

    #testShape = pCanvas.create_oval(80, 30, 140, 150, fill="blue")
    test_img = Image.open("cat.png")
    tk_img = ImageTk.PhotoImage(test_img)
    test_shape = p_canvas.create_image(0, 0, image=tk_img, anchor=tk.CENTER) # pivot point in center of image
    test_pet = Pet(name="kitty", position=[p_display_size[0].width/2, p_display_size[0].height/2], move_speed=15, shape=test_shape, tk_img=tk_img)
    test_pet.set_pos(test_pet.position[0], test_pet.position[1])
    p_pets.append(test_pet)

    p_canvas.bind("<ButtonPress-1>", p_pets[0].drag_pet_start)
    p_canvas.bind("<B1-Motion>", p_pets[0].drag_pet_move)
    p_canvas.bind("<ButtonRelease-1>", p_pets[0].drag_pet_release)
#endregion

#region Pet class and methods
class Pet:
    """
    position [x,y]
    current_direction [x,y]
    """
    def __init__(self, name, position, move_speed, current_direction, shape, tk_img):
        self.name = name
        self.position = position.copy()
        self.move_speed = move_speed
        self.current_direction = current_direction
        self.shape = shape
        self.tk_img = tk_img

    def speak(self):
        return f"i am {self.name}"

    def get_pos(self):
        return f"{self.name} @ {self.position}"
    
    def move(self, dx, dy):
        global p_canvas
        p_canvas.move(self.shape, dx, dy)
        self.position[0] += dx
        self.position[1] += dy
    
    def set_pos(self, x, y):
        global p_canvas
        p_canvas.moveto(self.shape, x, y)
        self.position[0] = x
        self.position[1] = y
    
    def drag_pet_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag_pet_move(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.move(dx, dy)
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag_pet_release(self, event):
        print(self.speak())

def spawn_pet():
    global p_pets
    global p_display_size

    posX = random.randint(0, int(p_display_size[0].width))
    posY = random.randint(0, int(p_display_size[0].height))
    dirX = int(random.choice([-3,-2,-1,1,2,3])) # a little silly
    dirY = int(random.choice([-3,-2,-1,1,2,3]))

    placeholder_img = Image.open("cat.png")
    img_recolored = recolor_with_numpy(placeholder_img, (random.randint(50,255), random.randint(50,255), random.randint(50,255)))
    tk_img = ImageTk.PhotoImage(img_recolored)
    test_shape = p_canvas.create_image(0, 0, image=tk_img, anchor=tk.CENTER) # pivot point in center of image
    pet = Pet(name="kitty", position=[posX, posY], move_speed=15, current_direction=[dirX, dirY], shape=test_shape, tk_img=tk_img)
    pet.set_pos(pet.position[0], pet.position[1])
    
    p_canvas.tag_bind(pet.shape, "<ButtonPress-1>", pet.drag_pet_start)
    p_canvas.tag_bind(pet.shape, "<B1-Motion>", pet.drag_pet_move)
    p_canvas.tag_bind(pet.shape, "<ButtonRelease-1>", pet.drag_pet_release)

    p_pets.append(pet)

def update_pets():
    global p_pets
    global p_display_size

    for pet in p_pets:
        pet.move(pet.current_direction[0], pet.current_direction[1])

        # Wrap around screen edges
        if(pet.position[0] > p_display_size[0].width):
            pet.set_pos(0, pet.position[1])
        elif(pet.position[0] < 0):
            pet.set_pos(p_display_size[0].width, pet.position[1])
        
        if(pet.position[1] > p_display_size[0].height):
            pet.set_pos(pet.position[0], 0)
        elif(pet.position[1] < 0):
            pet.set_pos(pet.position[0], p_display_size[0].height)
    
    p_root.after(20, update_pets)

def recolor_with_numpy(image: Image.Image, new_rgb: tuple) -> Image.Image:
    """
    Fast recolor using numpy. Replaces all non-transparent pixels' RGB with new_rgb, preserving alpha.
    """
    img = image.convert("RGBA")
    arr = numpy.array(img) # shape (h, w, 4)
    mask = arr[..., 3] > 0 # alpha > 0
    arr[..., :3][mask] = new_rgb
    return Image.fromarray(arr, mode="RGBA")
#endregion

#region Tray icon methods
def quit_tray(icon, item):
    try:
        icon.stop()
    except Exception:
        pass

    try:
        if p_root is not None:
            p_root.quit()
    except Exception:
        pass

def setup_tray():
    global p_icon
    
    icon_image = Image.open("icon.png")

    menu = pystray.Menu(
        pystray.MenuItem("Quit", quit_tray),
    )

    p_icon = pystray.Icon(
        name="deskpet name",
        icon=icon_image,
        title="deskpet",
        menu=menu,
    )

#endregion

#region Window setup methods
def setup_canvas():
    global p_canvas
    global p_root
    global p_display_size

    p_display_size = get_monitors()
    p_root = tk.Tk()
    
    # Setup transparent window
    p_root.overrideredirect(True)
    p_root.wm_attributes('-transparentcolor', 'white') # make white pixels transparent
    p_root.config(bg='white') # background color
    p_root.wm_attributes('-topmost', True) # always on top of all windows

    # Get window handle
    hwnd = ctypes.windll.user32.GetParent(p_root.winfo_id())

    # Set layered and transparent styles
    extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style | 0x80000 | 0x20)
    
    #region Setup canvas
    p_canvas = tk.Canvas(p_root, bg="white",
        width=p_display_size[0].width, height=p_display_size[0].height, highlightthickness=0)
    
    p_canvas.pack(fill="both")
    p_root.after(0, update_loop)
    #endregion
#endregion

#region Main loop
def main():
    setup_tray()
    setup_canvas()

    # run tray icon on separate thread since run is blocking
    if p_icon is not None:
        threading.Thread(target=p_icon.run, daemon=True).start()

    for i in range(0,128):
        spawn_pet()

    p_root.mainloop()

def update_loop():
    update_pets()
    
if __name__ == "__main__":
    main()
#endregion