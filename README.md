# algokartoss15mvfb
Implementation of the Berg et al. algorithm [A New Approach to Subdivision Simplification](http://dspace.library.uu.nl/handle/1874/17364). 

The algorithm is implemented in `python2`(!) and utilizes a few third party packages:

* `numpy`
* `shapely`
* `osgeo` (via gdal)

Usage:
`python[2] simp.py MaxEdgesToKeep LineInputFilePath PointInputFilePath OutputFilePath` 