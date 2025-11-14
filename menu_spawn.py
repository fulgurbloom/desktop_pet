# region Imports
from PIL import Image
from screeninfo import get_monitors
import ctypes
import pystray
import threading
import tkinter as tk
from tkinter import messagebox

import assets as py_assets
import pet as py_pet

# endregion


# region Window methods
def create_label(parent, text, row, column, pady):
    label = tk.Label(parent, text=text)
    label.grid(row=row, column=column, pady=pady)
    return label


def create_entry_box(parent, row, column, width, pady):
    entry_box = tk.Entry(parent, width=width)
    entry_box.grid(row=row, column=column, pady=pady)
    return entry_box


def create_button(parent, text, row, column, width, height, pady, command=None):
    button = tk.Button(parent, text=text, width=width, height=height, command=command)
    button.grid(row=row, column=column, pady=pady)


def create_spawn_window(ctx):

    spawn_window = tk.Toplevel(ctx.root)
    spawn_window.title("Spawn")
    spawn_window.geometry("256x256")

    name_label = create_label(spawn_window, text="Pet name", row=0, column=0, pady=2)
    name_text_box = create_entry_box(spawn_window, row=0, column=1, width=16, pady=2)

    spawn_amount_label = create_label(
        spawn_window, text="Spawn amount", row=1, column=0, pady=2
    )
    spawn_amount_box = create_entry_box(spawn_window, row=1, column=1, width=16, pady=2)

    move_speed_label = create_label(
        spawn_window, text="Move speed", row=2, column=0, pady=2
    )
    move_speed_box = create_entry_box(spawn_window, row=2, column=1, width=16, pady=2)

    initial_position_label = create_label(
        spawn_window, text="Initial position", row=3, column=0, pady=2
    )
    initial_position_box = create_entry_box(
        spawn_window, row=3, column=1, width=16, pady=2
    )

    initial_position_type_label = create_label(
        spawn_window, text="Initial position type", row=4, column=0, pady=2
    )
    initial_position_type_box = create_entry_box(
        spawn_window, row=4, column=1, width=16, pady=2
    )

    border_reaction_type_label = create_label(
        spawn_window, text="Border reaction type", row=5, column=0, pady=2
    )
    border_reaction_type_box = create_entry_box(
        spawn_window, row=5, column=1, width=16, pady=2
    )

    direction_type_label = create_label(
        spawn_window, text="Border reaction type", row=6, column=0, pady=2
    )
    direction_type_box = create_entry_box(
        spawn_window, row=6, column=1, width=16, pady=2
    )

    image_path_label = create_label(
        spawn_window, text="Image path", row=7, column=0, pady=2
    )
    image_path_box = create_entry_box(spawn_window, row=7, column=1, width=16, pady=2)

    dialogue_label = create_label(
        spawn_window, text="Dialogue", row=8, column=0, pady=2
    )
    dialogue_box = create_entry_box(spawn_window, row=8, column=1, width=16, pady=2)

    save_pet_button = create_button(
        spawn_window,
        text="Save pet",
        row=10,
        column=0,
        width=16,
        height=1,
        pady=0,
        command=lambda: save_pet(
            name_text_box=name_text_box,
            spawn_amount_box=spawn_amount_box,
            image_path_box=image_path_box,
        ),
    )


def save_pet(name_text_box, spawn_amount_box, image_path_box):
    # input validation
    if name_text_box.get() == "":
        tk.messagebox.showerror(
            title="Failed saving pet", detail="Name field cannot be empty"
        )
        return

    if spawn_amount_box.get() == "":
        messagebox.showerror(
            title="Failed saving pet", detail="Spawn amount field cannot be empty"
        )
        return

    config = py_pet.PetConfig(
        name=name_text_box.get(),
        spawn_amount=int(spawn_amount_box.get()),  # Convert to int if necessary
        initial_position=[0, 0],
        move_speed=0,
        initial_position_type=py_pet.InitialPositionType.SET,
        border_reaction_type=py_pet.BorderReactionType.BOUNCE,
        direction_type=py_pet.DirectionType.RANDOMIZED_ONCE,
        image_path=image_path_box.get(),
        dialogue=[],
    )

    py_assets.pet_config_to_json(config)


# endregion


# region Main loop
def main():
    pass


if __name__ == "__main__":
    main()
# endregion
