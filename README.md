### MonoDepthMask - A Dataset for multi-task learning of Monocular Depth Estimation and Mask Prediction


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
| fg_bg_images |  484320 |     250x250x3 |  RGB |           [0.56632738, 0.51567622, 0.45670792]  | [0.1076622,  0.10650349, 0.12808967]| <>|
| bg_images |      484320 |     250x250x3|  RGB|          [0.57469445, 0.52241555, 0.45992244] |  [0.11322354, 0.11195428, 0.13441683] | <> |
| mask_images|    484320|     250x250x3|  RGB|           [0.05795104, 0.05795104, 0.05795104] | [0.02640032, 0.02640032, 0.02640032] | <>|
| depth_images|   484320|     320x240x3|  RGB|           [0.61635181, 0.21432114, 0.50569604] | [0.09193359, 0.07619106, 0.04919082] | <> |
