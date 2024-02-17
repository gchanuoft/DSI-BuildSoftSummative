# Manual Test

## Notification to ntfy.sh topic:

Notification will be sent to the following when using the demo default config files\
[https://ntfy.sh/dsiBuildSoftSummative](https://ntfy.sh/dsiBuildSoftSummative)

## Running Unit Tests:
  Important: The unit test needed to be run at the **root** folder of the source code directory. The unit test config directory is located at the **root** directory hence unit test needed to be run at **root**.

  To run unit test, at the root directory run the following command:\
  ```pytest -v```

## Demos:

To run the demos, first navigate to the **demo** directory in the source code package

In the demo folder there are the following folders:
  1. configs - configuration files folder
  2. customPath - one of the demo output folder for PNG file
  4. figure - one of the demo output folder for PNG file
  3. my_plot - one of the demo output folder for PNG file
  4. plot - one of the demo output folder for PNG file

There are 6 demos.

  1. Demo using job config file 'configs/job_config.yml' and output figure to folder specificed in the config file (demo.py).\
  ```python demo.py```    
  2. Demo using job config file 'configs/job2_config.yml' and output folder is specified in the code as parameter (customPath.py).\
  ```python customPath.py```   
  3. Demo using job config file 'configs/job_config.yml' and output folder specified in the code as parameter with a folder that does not exist (customPathNotExist.py).  To show logging error messages.\
  ```python customPathNotExist.py```
  4. Demo calling compute_analysis() before data is loaded (beforeDataLoadCompute.py) To test assert.\
  ```python beforeDataLoadCompute.py```
  5. Demo calling plot_data() before data is computed (beforeComputePlot.py) To test assert.\
  ```python beforeComputePlot.py```
  6. Demo calling compute_analysis() before data is computed (beforeComputeSendDone.py) To test assert.\
  ```python beforeComputeSendDone.py```
  