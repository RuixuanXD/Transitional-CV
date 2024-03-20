import numpy as np
import os
from PIL import Image
import random


folder_path = './textures'
result_folder = './result_m1'
os.makedirs(result_folder, exist_ok=True)


for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        input = Image.open(file_path)
        file_name = os.path.basename(file_path)
        file_name, extension = os.path.splitext(file_name)

        patch_size = 50

        size = input.size
        # print(size)
        # print(type(size))
        new_size = [size[0]*5, size[1]*5]
        new_texture = Image.new('RGB', new_size)

        num_patches_x = new_size[0] // patch_size
        num_patches_y = new_size[1] // patch_size

        for x in range(num_patches_x):
            for y in range(num_patches_y):
                patch_x = random.randint(0, input.size[0] - patch_size)
                patch_y = random.randint(0, input.size[1] - patch_size)
                patch = input.crop((patch_x, patch_y, patch_x + patch_size, patch_y + patch_size))
                #print(patch_x)
                #print(patch_y)
                #print(input.size[0])
                #print(num_patches_x)
                #print(patch)
                new_texture.paste(patch, (x * patch_size, y * patch_size))
                #break
            #break
        #new_texture.show()
        result_path = os.path.join(result_folder, f'{file_name}.jpg')
        new_texture.save(result_path)
        break
