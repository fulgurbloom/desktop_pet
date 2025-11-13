from pet import Pet, PetConfig
from PIL import Image, ImageTk
import json
import numpy
import random

#region To-do
    # Support more than png (file loading related)
#endregion

#region JSON serialization methods
def pet_serializer(obj):
    """Serialize Pet and PetConfig objects for JSON"""
    
    if isinstance(obj, Pet):
        print(f"Serializing Pet: {obj.name}")
        # Only serialize the data we need to recreate the pet
        return {
            'name': obj.name,
            'position': obj.position,
            'move_speed': obj.move_speed,
            'current_direction': obj.current_direction
            # Skip: shape (Tkinter), tk_img (PhotoImage)
        }
    elif isinstance(obj, PetConfig):
        print(f"Serializing PetConfig: {obj.name}")
        return obj.__dict__
    
    print(f"Cannot serialize type: {type(obj).__name__}, value: {obj}")
    raise TypeError(f"Type {type(obj).__name__} not serializable")

def pet_to_json(pet):
    """Save Pet to json file"""
    try:
        # Convert Pet to dictionary first
        pet_dict = {
            'name': pet.name,
            'move_speed': pet.move_speed,
        }
        json_str = json.dumps(pet_dict, indent=4)
        with open(f"assets\\pets\\{pet.name}.json", 'w') as file:
            file.write(json_str)
    except AttributeError as e:
        print(f"Pet object missing required attribute: {e}")
        raise
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Serialization error: {e}")
        raise
    except IOError as e:
        print(f"File error: {e}")
        raise

def json_to_pet(name) -> Pet:
    """Return Pet from loaded json"""
    try:
        with open(name + ".json", 'r') as file:
            json_str = json.loads(file.read())
        
        return Pet(
            name=json_str['name'],
            #position=[0,0],
            move_speed=json_str['move_speed'],
            #current_direction=json_str['current_direction'],
            #shape=None,
            #tk_img=None
        )
    except FileNotFoundError as e:
        print(f"Pet file not found: {e}")
        raise
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Invalid pet data: {e}")
        raise
#endregion

#region Image
def load_image(file, random_color: bool) -> ImageTk:
    """
    Load image from file and convert to PhotoImage.
    Optionally recolor with random RGB values.
    """
    try:
        img = Image.open(file)
        
        if random_color:
            img = recolor_image(img, (random.randint(50,255), random.randint(50,255), random.randint(50,255)))
        
        tk_img = ImageTk.PhotoImage(img)
        img.close()
        
        return tk_img
    except FileNotFoundError as e:
        print(f"Image file not found: {file}")
        raise
    except (IOError, OSError) as e:
        print(f"Error reading image file: {e}")
        raise
    except Exception as e:
        print(f"Error loading image: {e}")
        raise

def recolor_image(image: Image.Image, new_rgb: tuple) -> Image.Image:
    """
    Fast recolor using numpy. Replaces all non-transparent pixels' RGB with new_rgb, preserving alpha.
    """
    try:
        if not isinstance(image, Image.Image):
            raise TypeError("Input must be a PIL Image object")
        if not isinstance(new_rgb, tuple) or len(new_rgb) != 3:
            raise ValueError("new_rgb must be a tuple of 3 integers (R, G, B)")
        
        img = image.convert("RGBA")
        arr = numpy.array(img) # shape (h, w, 4)
        mask = arr[..., 3] > 0 # alpha > 0
        arr[..., :3][mask] = new_rgb
        return Image.fromarray(arr, mode="RGBA")
    except (TypeError, ValueError) as e:
        print(f"Invalid argument: {e}")
        raise
    except Exception as e:
        print(f"Error recoloring image: {e}")
        raise
#endregion