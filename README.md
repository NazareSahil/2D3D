
![2D_IMAGES_TO_3D_MODEL](https://user-images.githubusercontent.com/77661670/174957440-c922665c-57fa-453a-a1db-fe1828fe01bb.png)
# 2D Images to 3D Model

This project makes a 3D model out of 2D medical (DICOM) images.


## DICOM images dataset

You can download the whole dataset of DICOM images from __[here](https://academictorrents.com/details/015f31a94c600256868be155358dc114157507fc)__.

OR

You can use datasets from the *__sample_dataset__* folder, which has some selective DICOM folders.

## Run Locally

* Clone the project

  ```DOS
    git clone https://github.com/NazareSahil/2D3D
  ```

* Go to the project directory

  ```DOS
    cd 2D3D
  ```

* Create virtual environment

  ```DOS
    pip install virtualenv

    # For Python 2
    python -m virtualenv 2d3denv

    # For Python 3
    python -m venv 2d3denv
  ```

* Activate virtual environment

  ```DOS
    .\2d3denv\Scripts\activate
  ```

* Install required libraries

  ```DOS
    pip install -r requirements.txt
  ```

* Create an empty *uploads* folder

  ```DOS
    mkdir uploads
  ```

* Run the project

  ```DOS
    python 2d3d.py
  ```

* Copy the localhost link onto the browser and you are good to go!
## Demo

![2d3dGIF](https://user-images.githubusercontent.com/77661670/175058057-5c55a731-1360-4535-a073-a74e3691c56a.gif)
