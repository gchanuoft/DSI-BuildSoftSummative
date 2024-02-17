# dsiBuildSoftSummative

Building Robust Software Summative Assignment

## Prerequisite: 
[UofT-DSI onboarding steps](https://github.com/UofT-DSI/Onboarding/tree/main/environment_setup)

## Demo

A **demo** folder is located within the package source code with sample configuration files.  To use the demo, follow the installation steps below first.  For running the demo, refer to [TEST.md](https://github.com/gchanuoft/dsiBuildSoftSummative/blob/main/TEST.md)

## Installation Steps:

  1. Create a new conda envrionment\
  ```conda create --name <my-env>```    
  2. Activate the new conda envrionment\
  ```conda activate <my-env>``` 
  3. Install pip\
  ```conda install pip```
  4. Install the package\
  ```pip install git+https://github.com/gchanuoft/dsiBuildSoftSummative```

## Running Unit Tests:
  1. Clone the repository\
  ```git clone https://github.com/gchanuoft/dsiBuildSoftSummative.git```
  2. Install pytest\
  ```pip install pytest```
  3. In the **dsiBuildSoftSummative** folder  
  ```pytest -v```