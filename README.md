#Instructions for running hazmath in the container

1. Obtain image `docker pull mirok/fenics-hazmath:latest`
2. Run image somewhere where HAZMath lib is accessible as a subdirectory.
   Here we make `/home/fenics/shared` bound to the directory from which
   docker is launched
   `docker run -it -v $(pwd):/home/fenics/shared hazmath_dev'
3. In `simple_test.py` edit the `hazmath_path` to point to HAZMath dynamic
   lib
4. Run `python3 simple_test.py`