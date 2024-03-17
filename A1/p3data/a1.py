import numpy as np
from PIL import Image, ImageDraw
import random

# Load the input texture image
input_size = 'textures/text.jpg'
input = Image.open(input_size)

# Define the size of the patches (e.g., 50x50 pixels)
patch_size = 30

# Define the size of the new texture
new_size = input.size

# Create a new blank image for the synthesized texture
new_texture = Image.new('RGB', new_size)

# Calculate the number of patches to cover the new texture
num_patches_x = new_size[0] // patch_size
num_patches_y = new_size[1] // patch_size

for x in range(num_patches_x):
    for y in range(num_patches_y):
        # Randomly select a patch from the input texture
        patch_x = random.randint(0, input.size[0] - patch_size)
        patch_y = random.randint(0, input.size[1] - patch_size)
        patch = input.crop((patch_x, patch_y, patch_x + patch_size, patch_y + patch_size))
        
        # Paste the patch onto the new texture
        # Note: This simple method does not handle overlapping regions specially
        new_texture.paste(patch, (x * patch_size, y * patch_size))

# Save or display the new texture
new_texture.show()