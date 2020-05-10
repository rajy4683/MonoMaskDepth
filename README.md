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
