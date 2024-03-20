import numpy as np
import os
from PIL import Image
from tqdm import tqdm


folder_path = './textures'
result_folder = './result_m2'
os.makedirs(result_folder, exist_ok=True)


patch_size = 50
overlap = 15
tolerance = 0.05

def ssd(patch1, patch2):
    if patch1.shape[2] == 3 and patch2.shape[2] == 4:
        patch2 = patch2[:, :, :3]
    elif patch1.shape[2] == 3 and patch2.shape[2] == 2:
        patch1 = patch1[:, :, :2]
    return np.sum((patch2 - patch1) ** 2)

def random_select(bests):
    index = np.random.choice(len(bests))
    _, x, y = bests[index]
    return x, y

def best_patches(input, input_height, input_width, patch_size, overlap, tolerance, new_size):
    new_array = np.array(input)

    errors = []


    height, width, _ = input_array.shape
    for y in range(0, height - patch_size + 1):
        for x in range(0, width - patch_size + 1):
            current_patch = input_array
            error = 0

            #print(current_patch.shape)
            if y > 0:

                error += ssd(new_array[input_height+patch_size-overlap:input_height+patch_size, input_width:input_width+patch_size, :], current_patch[y:y+overlap, x:x+patch_size, :])
                
            if x > 0:
            
                error += ssd(new_array[input_height:input_height+patch_size, input_width+patch_size-overlap:input_width+patch_size, :], current_patch[y:y+patch_size, x:x+overlap, :])

            errors.append((error, x, y))
            #break
            
    errors.sort(key=lambda x: x[0])
    min_error = errors[0][0]

    bests = [e for e in errors if e[0] <= min_error * (1 + tolerance)]

    return bests



for root, dirs, files in os.walk(folder_path):
    for file in tqdm(files):
        file_path = os.path.join(root, file)
        input = Image.open(file_path)
        size = input.size
        input_array = np.array(input)

        file_name = os.path.basename(file_path)
        file_name, extension = os.path.splitext(file_name)

        new_size = (size[0], size[1])
        new_texture = Image.new('RGB', new_size)

        num_patches_x = new_size[0] // patch_size
        num_patches_y = new_size[1] // patch_size

        patch_x = np.random.randint(0, input_array.shape[0] - patch_size - overlap)
        patch_y = np.random.randint(0, input_array.shape[1] - patch_size - overlap)


        for x in tqdm(range(num_patches_x)):
            for y in range(num_patches_y):

                patches = best_patches(new_texture, x * patch_size, y * patch_size, patch_size, overlap, tolerance, new_size)
                patch_x, patch_y = random_select(patches)

                if patch_x + patch_size >= input_array.shape[0]:
                    patch_x = input_array.shape[0] - patch_size
                if patch_y + patch_size >= input_array.shape[1]:
                    patch_y = input_array.shape[1] - patch_size

                    
                patch = input.crop((patch_x, patch_y, patch_x + patch_size, patch_y + patch_size))
                new_texture.paste(patch, (x * patch_size, y * patch_size))
            #break

        result_path = os.path.join(result_folder, f'{file_name}.jpg')
        new_texture.save(result_path)
        break