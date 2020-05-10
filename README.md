
## **Table of Contents**

* [MonoDepthMask](#monodepthmask)
    * [Dataset Description](#dataset-description)
    * [Dataset Stats](#dataset-stats)
* [Dataset Generation Process](#dataset-generation-process)
    * [Links](#links)
      + [fg_bg_images and mask_images](#fg_bg_images-and-mask_images)
      + [depth_images](#depth_images)
      + [bg_images](#bg_images)
    * [Sample Images](#sample-images)
      + [Base Images](#base-images)
      + [Depth Images](#depth-images)


<!-- toc -->


## MonoDepthMask
A Dataset for multi-task learning of Monocular Depth Estimation and Mask Prediction. 
The data was generated by taking:
   - ~100 random background images
   - ~100 random foreground images + flipped images of these originals
   - Overlaying these 100 fg images on each of the background at 20 different places (Yup! sometimes you could see poeple flying)
   - Using [DenseDepth](https://github.com/ialhashim/DenseDepth) model to generate Depth maps of the overlayed images
   
### Dataset Description
MonoDepthMask Dataset consists of following images:
- **bg_image:** Images with Only Background E.g: Malls, classrooms, college_outdoors, lobbies etc;
- **fg_bg_images:** Images with an object/person overlayed randomly on a Background
- **mask_images:** Ground truth of Masked Images of foregroud object/person.
- **depth_images:** Ground truth of Depth Map generated from fg_bg_images.
- **DepthMapDataSet.csv:** CSV file for the dataset contains following columns:

| Column Name  | Column Description  |
| :------------ | :------------ |
|  ImageName | fg_bg_image  |
| MaskName  | mask_image   |
| Depthname  |  depth_image |
| BGImageName  | bg_image  |
| BaseImageFName  |  Zip file containing fg_bg_images and mask_images |
|  DepthImageFName | Zip file containing depth_images  |
| BGType  | Class to which the bg_image belongs  |
| BGImageFName  | Zip file containing bg_images |

### Dataset Stats
| ImageType  | Count  |  Dimension  | Channel Space  | Channelwise Mean  | Channelwise StdDev  | Link |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| fg_bg_images |  484320 |     250x250x3 |  RGB |           [0.56632738, 0.51567622, 0.45670792]  | [0.1076622,  0.10650349, 0.12808967]| https://github.com/rajy4683/MonoMaskDepth/blob/master/README.md#fg_bg_images-and-mask_images |
| bg_images |      484320 |     250x250x3|  RGB|          [0.57469445, 0.52241555, 0.45992244] |  [0.11322354, 0.11195428, 0.13441683] | https://github.com/rajy4683/MonoMaskDepth/blob/master/README.md#bg_images |
| mask_images|    484320|     250x250x3|  RGB|           [0.05795104, 0.05795104, 0.05795104] | [0.02640032, 0.02640032, 0.02640032] | https://github.com/rajy4683/MonoMaskDepth/blob/master/README.md#fg_bg_images-and-mask_images |
| depth_images|   484320|     320x240x3|  RGB|           [0.61635181, 0.21432114, 0.50569604] | [0.09193359, 0.07619106, 0.04919082] | https://github.com/rajy4683/MonoMaskDepth/blob/master/README.md#depth_images |

All the above data is indexed in the below CSVs:           
   * [FullDataSet](https://drive.google.com/open?id=1AlU-92oJHPrbAX-GMheRIWZGXAsHcp8U) (~480K)   
   * [Training Data](https://drive.google.com/open?id=1-2X21tqGlwrJ93RBlOPQEeGsqfQmSyJ2) (~340K)
   * [Test Data](https://drive.google.com/open?id=1-2yGqzdVQ9FycQcdYw91JvK2o7cvn2wC) (~150K)
   * [Sample Data](https://drive.google.com/open?id=1e4dbAD6RbSnhPrMOln6jTH5m79mCLkKR) (500)
 


## Dataset Generation Process
* How to create transparent foreground images:
	* Download PNG/JPG format images of people with any background
	* Upload individual images to https://www.remove.bg/upload 
	* Since I was using the free version so images had to be transformed one at a time
	* Download and save the transparent images
* How to create masks for above foreground images:
	* Used a simple OpenCV based [conversion](https://github.com/rajy4683/MonoMaskDepth/blob/c58e18fd0357453ae09f643c3f1ca8e53db7fcf4/monomaskdepthutils.py#L118)
   ```
   def generate_mask(img,debug=False):    
      lower_white = np.array([1, 1,1,4])
      upper_white = np.array([255,255,255,4])
      mask = cv2.inRange(img, lower_white, upper_white)
      if debug == True:
         cv2_imshow(img)
         cv2_imshow(mask)
      return mask
   ```
* How were fg overlayed over bg and created 20 variants:
   * Please refer to [this notebook](https://github.com/rajy4683/MonoMaskDepth/blob/master/DataGeneratorPipeline.ipynb) for end-to-end flow
   * Primarily used albumentations to generate flipped images and for resizing images to fit the background. Code can be found [here](https://github.com/rajy4683/MonoMaskDepth/blob/c58e18fd0357453ae09f643c3f1ca8e53db7fcf4/monomaskdepthutils.py#L188)
   * Main advantage of albumentation was that it operates on masks/bboxes also in the same operation
   * FG images were of the size (125,125) or (64,64)
   * Range of 20 random positions within ((0, height_bg - height_fg), (0, width_bg - width_fg)) was used to prevent images being cropped at the edge. Code can be found [here](https://github.com/rajy4683/MonoMaskDepth/blob/c58e18fd0357453ae09f643c3f1ca8e53db7fcf4/monomaskdepthutils.py#L227)
   * A csv file with a tuple of every background with 40 positions (flipped + regular) was created.
   * Slices of this CSV file was run parallely on 4 Colab instances to generate 4 files listed in [this section](https://github.com/rajy4683/MonoMaskDepth/blob/master/README.md#fg_bg_images-and-mask_images).
      + All the files generated were stored locally on the colab instance
      + All the input files were copied at the start of the run to the colab instance's local directory
      + The files were later zipped and saved back on to Google drive.
      + Currently analyzing how to make this process faster and streamlined
   * To overcome disk space and colab file handling issue,

* How did you create your depth images?
   * Base Model used was [DenseDepth](https://github.com/ialhashim/DenseDepth/blob/master/DenseDepth.ipynb)
   * The test utilities were modified to handle the following:
      * From input zip files generated above, directly read ~300 images
      * Resize these images using albumentations to 480x640 
      * Run the model on the inputs and save the output depth data in 'plasma' cmap. This will be modified to grayscale.
      * Similar to above step, this step was also run of 4 colab instances in parallel to generate respective depth images
      * Code for this handling can be found [here](https://colab.research.google.com/drive/1QpcN8SE82asljEr5_m_yOFkWE3jvnJhq?authuser=1#scrollTo=vR3sAKJX_CZY)
      

### Links

#### fg_bg_images and mask_images:
   - https://drive.google.com/open?id=1ie4YjMIlyc66PYXiUsBlNm5HL71p0he1 
   - https://drive.google.com/open?id=1zxIl558rvx_OFES0uSyvV5ZvPHrJGbYs 
   - https://drive.google.com/open?id=1LLZdirDlNv6eyddE6cyBQm3tztk6K4Rw 
   - https://drive.google.com/open?id=1ecYc8UWWq8s5-P_amn3r0hjCrdcP3yZv 
#### depth_images:
   - https://drive.google.com/open?id=1ie4YjMIlyc66PYXiUsBlNm5HL71p0he1 
   - https://drive.google.com/open?id=1zxIl558rvx_OFES0uSyvV5ZvPHrJGbYs 
   - https://drive.google.com/open?id=1LLZdirDlNv6eyddE6cyBQm3tztk6K4Rw 
   - https://drive.google.com/open?id=1ecYc8UWWq8s5-P_amn3r0hjCrdcP3yZv
#### bg_images:
   - https://drive.google.com/open?id=15l6UxsJEq1dndPqS18QSRuR5Wqz24EZi    
#### csv_files:
   - [FullDataSet](https://drive.google.com/open?id=1AlU-92oJHPrbAX-GMheRIWZGXAsHcp8U) (~480K)   
   - [Training Data](https://drive.google.com/open?id=1-2X21tqGlwrJ93RBlOPQEeGsqfQmSyJ2) (~340K)
   - [Test Data](https://drive.google.com/open?id=1-2yGqzdVQ9FycQcdYw91JvK2o7cvn2wC) (~150K)
   - [Sample Data](https://drive.google.com/open?id=1e4dbAD6RbSnhPrMOln6jTH5m79mCLkKR) (500)

### Sample Images

##### Base Images：

[![](https://github.com/rajy4683/MonoMaskDepth/blob/master/allimg.png)](https://github.com/rajy4683/MonoMaskDepth/blob/master/allimg.png "Samples of BG/FG_BG/Masks")
----
#### Depth Images：

[![](https://github.com/rajy4683/MonoMaskDepth/blob/master/depthmap.png)](https://github.com/rajy4683/MonoMaskDepth/blob/master/depthmap.png "Depth Images")
----

