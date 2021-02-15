# Mystery Box Challenge (MBC App) :cookie: - Object Detection Model

An instance of [YOLOv5](https://github.com/ultralytics/yolov5) trained on custom dataset of food ingredients, collected and annotated manually.

Following are the model parameters used:

    		| Model parameters  		 	|      value    |
    		|-------------------------------|--------------:|
    		| Number of epochs 			 	|  	   100 		|
    		| Training batch Size 		 	| 	    16   	|
    		| Inference batch size 		 	| 		1 		|
    		| Model configuration		 	| 	  yolov5m 	|
    		| Image size 		 			| 	   640 		|

After training, the default export scirpt was modified to make sure the outputs of the inference instance {bounding boxes, confidence, class}.

### Connected repositories

-   [Inference Endpoint](https://github.com/himanshu-dutta/mbc-endpoint)
-   [Frontend Application](https://github.com/himanshu-dutta/mbc-frontend)
