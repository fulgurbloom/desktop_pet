# region Imports
from enum import Enum
import random
import tkinter as tk

import assets as py_assets

# endregion


# region Configuration
class InitialPositionType(Enum):
    RANDOMIZED = "RANDOMIZED"
    SET = "SET"


class BorderReactionType(Enum):
    BOUNCE = "BOUNCE"
    WRAP = "WRAP"


class DirectionType(Enum):
    RANDOMIZED_ONCE = "RANDOMIZED_ONCE"


class PetConfig:
    def __init__(
        self,
        name,
        spawn_amount,
        initial_position,
        move_speed,
        initial_position_type: InitialPositionType,
        border_reaction_type: BorderReactionType,
        direction_type: DirectionType,
        image_path,
        dialogue,
    ):
        self.name = name
        self.spawn_amount = spawn_amount
        self.initial_position = initial_position
        self.move_speed = move_speed
        self.initial_position_type = (initial_position_type,)
        self.border_reaction_type = (border_reaction_type,)
        self.direction_type = (direction_type,)
        self.image_path = image_path
        self.dialogue = dialogue


# endregion


# region Pet class and methods
class Pet:
    """
    position [x,y]
    velocity [x,y]
    """

    def __init__(self, pet_config: PetConfig, position, velocity, shape, tk_img):
        self.pet_config = pet_config
        self.position = position.copy()
        self.velocity = velocity
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


def spawn_pet(
    ctx,
    initial_position=[0, 0],
    pet_config: PetConfig = None,
):
    pos = [0, 0]
    dir = [0, 0]

    if pet_config is None:
        raise ValueError("pet_config cannot be None")
    if not isinstance(pet_config, PetConfig):
        raise TypeError("pet_config must be an instance of PetConfig")

    match pet_config.initial_position_type[0].value:
        case InitialPositionType.SET.value:
            pos = [initial_position[0], initial_position[1]]

        case InitialPositionType.RANDOMIZED.value:
            pos[0] = random.randint(0, int(ctx.displays[0].width))
            pos[1] = random.randint(0, int(ctx.displays[0].height))

    match pet_config.direction_type[0].value:
        case DirectionType.RANDOMIZED_ONCE.value:
            dir[0] = int(random.choice([-3, -2, -1, 1, 2, 3]))  # a little silly
            dir[1] = int(random.choice([-3, -2, -1, 1, 2, 3]))

    tk_img = py_assets.load_image(pet_config.image_path, True)
    shape = ctx.canvas.create_image(
        0, 0, image=tk_img, anchor=tk.CENTER
    )  # pivot point in center of image
    pet = Pet(
        pet_config=pet_config,
        position=pos,
        velocity=dir,
        shape=shape,
        tk_img=tk_img,
    )
    pet.set_pos(ctx, pet.position[0], pet.position[1])

    ctx.canvas.tag_bind(pet.shape, "<ButtonPress-1>", pet.drag_pet_start)
    ctx.canvas.tag_bind(pet.shape, "<B1-Motion>", lambda e: pet.drag_pet_move(e, ctx))
    ctx.canvas.tag_bind(pet.shape, "<ButtonRelease-1>", pet.drag_pet_release)

    ctx.pets.append(pet)


def update_pets(ctx):
    for pet in ctx.pets:
        try:
            pet.move(ctx, pet.velocity[0], pet.velocity[1])

            # 16 is "border" pixel amount to prevent pets from going off screen and killing python

            match pet.pet_config.border_reaction_type[0].value:
                case (
                    BorderReactionType.BOUNCE.value
                ):  # Switch directions on contact with border
                    if (
                        pet.position[0] > (ctx.displays[0].width - 16)
                        or pet.position[0] < 16
                    ):
                        pet.velocity = [
                            -pet.velocity[0],
                            pet.velocity[1],
                        ]

                    if (
                        pet.position[1] > (ctx.displays[0].height - 16)
                        or pet.position[1] < 16
                    ):
                        pet.velocity = [
                            pet.velocity[0],
                            -pet.velocity[1],
                        ]

                case (
                    BorderReactionType.WRAP.value
                ):  # Wrap around border to opposite end
                    if pet.position[0] > ctx.displays[0].width:
                        pet.set_pos(ctx, 0, pet.position[1])
                    elif pet.position[0] < 0:
                        pet.set_pos(ctx, ctx.displays[0].width, pet.position[1])

                    if pet.position[1] > ctx.displays[0].height:
                        pet.set_pos(ctx, pet.position[0], 0)
                    elif pet.position[1] < 0:
                        pet.set_pos(ctx, pet.position[0], ctx.displays[0].height)
                    pass

        except AttributeError as e:
            print(f"Error updating pet {pet.name}: {e}")
        except Exception as e:
            print(f"Unexpected error with pet {pet.name}: {e}")

    ctx.root.after(20, lambda: update_pets(ctx))


# endregion
