[![PyPI version](https://badge.fury.io/py/facialmask.svg)](https://badge.fury.io/py/facialmask)

# facial-mask
Pixelate faces in images through a Python CLI.

![alt-text](https://github.com/dhorvay/facial-mask/blob/master/example/result.png)

# Installation

```py
pip install facialmask
```
# Usage

``` sh
facialmask --file [relative-path to file]
```
The output will be saved in the same directory the script is ran with the filename 'result.png'

# References

Facial detection code is done using OpenCV and the default Haar Cascade pretrained model - what I wrote is a modified version of what is found [here by Shantnu Tiwari on RealPython](https://realpython.com/face-recognition-with-python/) with features to add the pixelated mask on top.
