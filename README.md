# VHS-Rip
A small TKinter project to work with the OSPREY-200 Capture Card. Technically rips more than VHSes- anything with a composite out is fair game

Hopefully will be platform independent in the future, but is currently configured to work with an OSPREY-200, a CUDA capable video card, and linux systems

Requires:
* **A capture device!** (currently only OSPREY-200 capture cards)
* Python 3
* Python TKinter
* x265 libraries
    * Support for other encodings will be added later
* FFMPEG
    * (currently) Must be compiled with x265 support
* (currently) A CUDA capable GPU
    * Support for other HW accel options will be added later (alongside CPU encoding)
* (currently) Some form of linux, tested on Ubuntu 20.04
    * Support for Windows coming later
    * I see no reason why MacOS wouldn't work (so long as the capture card works and python/ffmpeg/x265 is installed), but I have no way of testing that