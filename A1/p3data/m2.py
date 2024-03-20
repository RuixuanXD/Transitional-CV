import numpy as np
import os
from PIL import Image
import random


folder_path = './textures'
result_folder = './result_m2'
os.makedirs(result_folder, exist_ok=True)

patch_size = 50
overlap = 10

def ssd(patch, target):
    if patch.shape[2] == 2 and target.shape[2] == 3:
        target = target[:, :, :2]
    elif patch.shape[2] == 4 and target.shape[2] == 3:
        patch = patch[:, :, :3]
    return np.sum((patch - target) ** 2)




def best_patches(input_array, patch_size, overlap, new_array):

    errors = []

    for y in range(input_array.shape[0] - patch_size + 1):
        for x in range(input_array.shape[1] - patch_size + 1):
            error = 0
            current_array = input_array[y:y+patch_size, x:x+patch_size, :3]
            #if y > 0:
                
            error += ssd(input_array[y:y+overlap, x:x+patch_size, :], new_array[y+patch_size-overlap:y+patch_size, x:x+patch_size, :])
                
            #if x > 0:

            #error += ssd(input_array[y:y+patch_size, x:x+overlap, :], new_array[y:y+patch_size, x+patch_size-overlap:x+patch_size, :])

            errors.append((error, current_array))
            #break
            
    errors.sort(key=lambda x: x[0])
    errors = [e for e in errors if e[0] != 0]
    min_error = errors[0][0]
    #print(min_error)
    bests = [e for e in errors if e[0] <= min_error * (1 + 0.15)]
    #print(bests)
    return random.choice(bests)


for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        input = Image.open(file_path)
        file_name = os.path.basename(file_path)
        file_name, extension = os.path.splitext(file_name)
        
        size = input.size

        new_size = [size[0]*5, size[1]*5]
        new_texture = Image.new('RGB', new_size)
        new_array = np.array(new_texture)
        #print(new_array.shape)
        num_patches_x = new_size[1] // (patch_size)
        num_patches_y = new_size[0] // (patch_size)
        #print(new_size[1])
        # print(num_patches_y)

        for i in range(num_patches_x):
            for j in range(num_patches_y):

                x = i * (patch_size - overlap)
                y = j * (patch_size - overlap)

                #print(size[0])
                patch = best_patches(np.array(input), patch_size, overlap, new_array)[1]
                #print(patch.shape)
                #print(x+patch_size)
                new_array[x:x+patch_size, y:y+patch_size, :] = patch
                #break
            #break

        result_path = os.path.join(result_folder, f'{file_name}.jpg')
        image = Image.fromarray(new_array)
        image.save(result_path)
        break
