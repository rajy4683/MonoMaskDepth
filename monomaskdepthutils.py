import os

import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage.color import label2rgb

import albumentations as A
import random
from google.colab.patches import cv2_imshow
from PIL import Image
import glob
from zipfile import ZipFile
import re
import pandas as pd

def load_return_fgbg_lists():
    base_dir = "/content/S15EVA4/"
    file_format = "*png"
    folder_list = ["classroom", "college_outdoors", 
                   "corridors", "dining_room",
                   "lobby","malls", "meeting_rooms",
                   "people_cropresize"]
    folder_dict = dict()
    for folder_name in folder_list:
        full_path = base_dir+folder_name+"/"+"*png"
        print(full_path)
        folder_dict[folder_name] = [ val for val in glob.glob(full_path)]
    return folder_dict

fg_bg_file_list = load_return_fgbg_lists()

BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

def visualize_bbox(img, bbox, color=BOX_COLOR, thickness=2, **kwargs):
    #height, width = img.shape[:2]

    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    return img

def visualize_titles(img, bbox, title, color=BOX_COLOR, thickness=2, font_thickness = 2, font_scale=0.35, **kwargs):
    #height, width = img.shape[:2]
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    
    ((text_width, text_height), _) = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(img, title, (x_min, y_min - int(0.3 * text_height)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, TEXT_COLOR,
                font_thickness, lineType=cv2.LINE_AA)
    return img


def augment_and_show(aug, image, mask=None, bboxes=[], categories=[], category_id_to_name=[], filename=None, 
                     font_scale_orig=0.35, 
                     font_scale_aug=0.35, show_title=True, **kwargs):

    augmented = aug(image=image, mask=mask, bboxes=bboxes, category_id=categories)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_aug = cv2.cvtColor(augmented['image'], cv2.COLOR_BGR2RGB)

    for bbox in bboxes:
        visualize_bbox(image, bbox, **kwargs)

    for bbox in augmented['bboxes']:
        visualize_bbox(image_aug, bbox, **kwargs)

    if show_title:
        for bbox,cat_id in zip(bboxes, categories):
            visualize_titles(image, bbox, category_id_to_name[cat_id], font_scale=font_scale_orig, **kwargs)
        for bbox,cat_id in zip(augmented['bboxes'], augmented['category_id']):
            visualize_titles(image_aug, bbox, category_id_to_name[cat_id], font_scale=font_scale_aug, **kwargs)

    
    if mask is None:
        f, ax = plt.subplots(1, 2, figsize=(16, 8))
        
        ax[0].imshow(image)
        ax[0].set_title('Original image')
        
        ax[1].imshow(image_aug)
        ax[1].set_title('Augmented image')
    else:
        f, ax = plt.subplots(2, 2, figsize=(16, 16))
        
        if len(mask.shape) != 3:
            mask = label2rgb(mask, bg_label=0)            
            mask_aug = label2rgb(augmented['mask'], bg_label=0)
        else:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
            mask_aug = cv2.cvtColor(augmented['mask'], cv2.COLOR_BGR2RGB)
            
        ax[0, 0].imshow(image)
        ax[0, 0].set_title('Original image')
        
        ax[0, 1].imshow(image_aug)
        ax[0, 1].set_title('Augmented image')
        
        ax[1, 0].imshow(mask, interpolation='nearest')
        ax[1, 0].set_title('Original mask')

        ax[1, 1].imshow(mask_aug, interpolation='nearest')
        ax[1, 1].set_title('Augmented mask')

    f.tight_layout()
    if filename is not None:
        f.savefig(filename)
        
    return augmented['image'], augmented['mask'], augmented['bboxes']

def find_in_dir(dirname):
    return [os.path.join(dirname, fname) for fname in sorted(os.listdir(dirname))]

def generate_mask(img,debug=False):    
    lower_white = np.array([1, 1,1,4])
    upper_white = np.array([255,255,255,4])
    mask = cv2.inRange(img, lower_white, upper_white)
    if debug == True:
        cv2_imshow(img)
        cv2_imshow(mask)
    return mask

def image_overlay(background, foreground, x_offset, y_offset):
    #x_offset=y_offset=100

    #x1, x2 = x_offset, x_offset + foreground_img.shape[0]
    #y1, y2 = y_offset, y_offset + foreground_img.shape[1]

    background_full = Image.open(background)#.resize((250,250))
    foreground = Image.open(foreground).convert('RGBA')
    background_full.paste(foreground, (x_offset, y_offset), foreground)
    return background_full


#cv2.imread('images/parrot.jpg')

flip = A.Compose([
    A.IAAFliplr(p=1,always_apply=True),
    # A.RandomBrightnessContrast(p=1),    
    # A.RandomGamma(p=1),    
    # A.CLAHE(p=1),    
], p=1)

resize_bg = A.Compose([
    A.Resize(250,250,always_apply=True,p=1),
    #A.CLAHE(p=1),
    #A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=50, val_shift_limit=50, p=1),
], p=1)


strong = A.Compose([
    A.ChannelShuffle(p=1),
], p=1)

def image_overlay_numpy(background, foreground, x_offset, y_offset):
    #x_offset=y_offset=100

    #x1, x2 = x_offset, x_offset + foreground_img.shape[0]
    #y1, y2 = y_offset, y_offset + foreground_img.shape[1]

    background_full = Image.fromarray(background)
    #Image.open(background)#.resize((250,250))
    foreground = Image.fromarray(foreground).convert('RGBA')
    #Image.open(foreground).convert('RGBA')
    background_full.paste(foreground, (x_offset, y_offset), foreground)
    return background_full.convert('RGB')

def rand_run_name():
    ran = random.randrange(10**80)
    myhex = "%064x" % ran
    #limit string to 64 characters
    myhex = myhex[:10]
    return myhex

def generate_mask(img,debug=False):    
    lower_white = np.array([1, 1,1])
    upper_white = np.array([255,255,255])
    mask = cv2.inRange(img[:,:,:-1], lower_white, upper_white)
    if debug == True:
        cv2_imshow(img)
        cv2_imshow(mask)
    return mask

def generate_fg_set(base_image_list, debug=False):
    for base_image_name in base_image_list:
        save_dir = os.path.join(os.path.dirname(base_image_name),"aug_images")
        basefile_name = os.path.basename(base_image_name)
        mask_name = "mask_"+basefile_name
        flip_name = "flip_"+basefile_name
        flip_mask_name = "mask_"+flip_name
        print(basefile_name, mask_name, flip_name,flip_mask_name)

        base_image = np.array(Image.open(base_image_name))
        base_mask = generate_mask(np.array(base_image))
        
        flipped_image = flip(image=base_image, mask=base_mask)
        Image.fromarray(base_mask).save(os.path.join(save_dir,mask_name))
        Image.fromarray(flipped_image['image']).save(os.path.join(save_dir,flip_name))
        Image.fromarray(flipped_image['mask']).save(os.path.join(save_dir,flip_mask_name))
        
        if (debug == True):
            display(Image.fromarray(base_image))
            display(Image.fromarray(base_mask))
            display(Image.fromarray(flipped_image['image']))
            display(Image.fromarray(flipped_image['mask']))


def get_resize_aug(height_val, width_val):
    return A.Compose([
            A.Resize(height_val,width_val,always_apply=True,p=1),
            ], p=1)

def get_fg_image_masks(fg_file_name, bg_height, bg_width, debug=False):
    save_dir = os.path.join(os.path.dirname(fg_file_name),"aug_images")
    basefile_name = os.path.basename(fg_file_name)

    basefile = np.array(Image.open(fg_file_name))
    mask = np.array(Image.open(os.path.join(save_dir, "mask_"+basefile_name)))
    flip = np.array(Image.open(os.path.join(save_dir, "flip_"+basefile_name)))
    mask_flip = np.array(Image.open(os.path.join(save_dir, "mask_flip_"+basefile_name)))


    aspect_ratio = basefile.shape[0]/basefile.shape[1]
    final_fg_height = bg_height//2
    final_fg_width = np.int(final_fg_height // aspect_ratio)

    

    resized_orig_fg = get_resize_aug( final_fg_height, final_fg_width)(image=basefile, mask=mask)
    resized_flip_fg = get_resize_aug( final_fg_height, final_fg_width)(image=flip, mask=mask_flip)

    #print(resized_orig_fg['image'].shape)
    if (debug == True):
        print("Original shape:{} New Shape: {}".format(basefile.shape, (final_fg_height, final_fg_width)))
        display(Image.fromarray(basefile))
        display(Image.fromarray(resized_orig_fg['image']))
        display(Image.fromarray(resized_orig_fg['mask']))

        display(Image.fromarray(resized_flip_fg['image']))
        display(Image.fromarray(resized_flip_fg['mask']))

    return resized_orig_fg, resized_flip_fg

    #return os.path.join(save_dir, mask_name), os.path.join(save_dir, flip_name),  os.path.join(save_dir, mask_flip_name)

"""
  Given BG, FG and Flipped FG, retrieves/creates a new overlayed image and mask   
"""

def create_overlayed_img(background, 
                         foreground, 
                         flip_foreground, 
                         x_offset,
                         y_offset, 
                         bg_image, 
                         debug=False, 
                         save_images=True):

    save_dir = os.path.join(os.path.dirname(bg_image),"aug_images/")
    filename = os.path.basename(bg_image)
    counter = 1
    for val in [foreground, flip_foreground]:
        rand_str = str(rand_run_name())
        image = image_overlay_numpy(background['image'], val['image'], x_offset,y_offset)
        mask = image_overlay_numpy(background['mask'], val['mask'], x_offset,y_offset)
        if(debug == True):
            display(image)
            display(mask)
        if(save_images == True):
            image_save_path = os.path.join(save_dir+"image_"+rand_str+"_"+filename.replace("png","jpg"))
            mask_save_path = os.path.join(save_dir+"mask_"+rand_str+"_"+filename.replace("png","jpg"))
            #print(image_save_path,mask_save_path)
            image.save(image_save_path,'JPEG',quality=80)
            mask.save(mask_save_path,'JPEG',quality=80)

"""
    Top level-handler function:
    1. Calls albumentations to resize both BG, FG and Flipped FG
    2. Retrieves the resized masks for BG, FG and Flipped G
    3. Calls 'create_overlayed_img()' to blend/overlay the FG and Flipped FG on the BG 
"""
def overlay_images(background_path, foreground_path, 
                   bg_height=250,bg_width=250, 
                   replica_count=20, save_images=True,
                   debug=False):
    #print(background_path)
    #save_dir = os.path.join(os.path.dirname(fg_file_name),"aug_images")
    image = np.array(Image.open(background_path))
    # Masked output 
    mask_bg = np.zeros_like(image, dtype='uint8')
    
    resized_bg = get_resize_aug(bg_height,bg_width)(image=image, mask=mask_bg)    
    #print(resized_bg['image'].shape)
    
    
    resized_fg, resized_flip_fg  = get_fg_image_masks(foreground_path, bg_height, bg_width)
    ### Preventing FG to get thrown out of the FG
    max_y_offset = resized_bg['image'].shape[0]-resized_fg['image'].shape[0]
    max_x_offset = resized_bg['image'].shape[1]-resized_fg['image'].shape[1]
    randn_y = np.random.randint(0, max_y_offset, replica_count)
    randn_x = np.random.randint(0, max_x_offset, replica_count)
    for tuple_val in zip(randn_y,randn_x):
        y_offset=tuple_val[0]
        x_offset=tuple_val[1]
        create_overlayed_img(resized_bg, resized_fg, resized_flip_fg,
                             x_offset, y_offset, background_path, debug=debug, save_images=save_images)



