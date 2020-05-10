
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
A Dataset for multi-task learning of Monocular Depth Estimation and Mask Prediction

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

### Code Blocks (multi-language) & highlighting

#### Inline code

`$ npm install marked`


### Sample Images

##### Base Images：

[![](https://github.com/rajy4683/MonoMaskDepth/blob/master/allimg.png)](https://github.com/rajy4683/MonoMaskDepth/blob/master/allimg.png "Samples of BG/FG_BG/Masks")
----
#### Depth Images：

[![](https://github.com/rajy4683/MonoMaskDepth/blob/master/depthmap.png)](https://github.com/rajy4683/MonoMaskDepth/blob/master/depthmap.png "Depth Images")
----
