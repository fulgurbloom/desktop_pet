#region Imports
from enum import Enum
import assets as py_assets
import random
import tkinter as tk
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
    
    def move(self, ctx, dx, dy):
        ctx.canvas.move(self.shape, dx, dy)
        self.position[0] += dx
        self.position[1] += dy
    
    def set_pos(self, ctx, x, y):
        ctx.canvas.moveto(self.shape, x, y)
        self.position[0] = x
        self.position[1] = y
    
    def drag_pet_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag_pet_move(self, event, ctx):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.move(ctx, dx, dy)
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag_pet_release(self, event):
        print(self.speak())

class InitialPositionType(Enum):
    SET = "SET"
    RANDOMIZED = "RANDOMIZED"

class MovementType(Enum):
    WRAP = "WRAP"
    BOUNCE = "BOUNCE"

class PetConfigOptions(Enum):
    INITIAL_POSITION_TYPE = InitialPositionType
    MOVEMENT_TYPE = MovementType

class PetConfig:
    def __init__(self, name, move_speed, image_path, dialogue):
        self.name = name
        self.move_speed = move_speed
        self.image_path = image_path
        self.dialogue = dialogue

def spawn_pet(ctx, image_path, name="empty", position=[0,0], move_speed=10):
    posX = random.randint(0, int(ctx.displays[0].width))
    posY = random.randint(0, int(ctx.displays[0].height))
    dirX = int(random.choice([-3,-2,-1,1,2,3])) # a little silly
    dirY = int(random.choice([-3,-2,-1,1,2,3]))

    tk_img = py_assets.load_image(image_path, True)
    shape = ctx.canvas.create_image(0, 0, image=tk_img, anchor=tk.CENTER) # pivot point in center of image
    pet = Pet(name=name, position=[posX, posY], move_speed=move_speed, current_direction=[dirX, dirY], shape=shape, tk_img=tk_img)
    pet.set_pos(ctx, pet.position[0], pet.position[1])
    
    ctx.canvas.tag_bind(pet.shape, "<ButtonPress-1>", pet.drag_pet_start)
    ctx.canvas.tag_bind(pet.shape, "<B1-Motion>", lambda e: pet.drag_pet_move(e, ctx))
    ctx.canvas.tag_bind(pet.shape, "<ButtonRelease-1>", pet.drag_pet_release)

    ctx.pets.append(pet)

def update_pets(ctx):
    for pet in ctx.pets:
        pet.move(ctx, pet.current_direction[0], pet.current_direction[1])

        # Wrap around screen edges
        if(pet.position[0] > ctx.displays[0].width):
            pet.set_pos(ctx, 0, pet.position[1])
        elif(pet.position[0] < 0):
            pet.set_pos(ctx, ctx.displays[0].width, pet.position[1])
        
        if(pet.position[1] > ctx.displays[0].height):
            pet.set_pos(ctx, pet.position[0], 0)
        elif(pet.position[1] < 0):
            pet.set_pos(ctx, pet.position[0], ctx.displays[0].height)
    
    ctx.root.after(20, lambda: update_pets(ctx))
#endregion
