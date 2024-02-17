# Manual Test

## Notification to ntfy.sh topic:

Notification will be sent to the following when using the demo default config files\
[https://ntfy.sh/dsiBuildSoftSummative](https://ntfy.sh/dsiBuildSoftSummative)

## Running Unit Tests:
  
  To run unit test, at the **src/dsiBuildSoftSummative** directory run the following command:\
  ```pytest -v```

## Demos:

**Import: The demo can only be run after the module is installed using the steps specificed in the "Installation Steps" section of README.md(https://github.com/gchanuoft/dsiBuildSoftSummative/blob/main/README.md)**

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
  