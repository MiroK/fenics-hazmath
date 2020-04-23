# Running hazmath in the container pulled from dockerhub

1. Obtain image `docker pull mirok/fenics-hazmath:latest`
2. Run image somewhere where HAZMath lib is accessible as a subdirectory
   Here we make `/home/fenics/shared` bound to the directory from which
   docker is launched
   
   ```
   docker run -it -v $(pwd):/home/fenics/shared hazmath_dev
   ```
   
3. In `simple_test.py` edit the `hazmath_path` to point to HAZMath dynamic
   lib. As an example, if docker was launched from `~/Documents` and __libhazmath.so__
   resides in `~/Documents/Software/hazmath/lib` then
 
   ```
   hazmath_path = '/home/fenics/shared/Software/hazmath/lib/libhazmath.so'
   ```
   
   in the script.
4. Run `python3 simple_test.py`

# Building image locally based on dockerfile

Our `Dockerfile` is based on FEniCS dev image from `quay.io/fenicsproject/dev`
and adds [FEniCS_ii](https://github.com/MiroK/fenics_ii) with its dependencies and [cbc.block](https://bitbucket.org/fenics-apps/cbc.block).
For the moment, specific branches/commits of the repos are used but we can always
update this to, e.g., work with their latest master. To build the image locally
run (in this directory)

```
docker build --no-cache -t (IMAGE_NAME) .
```

Optionally, you can push the image to dockerhub having tagged it

```
docker tag IMAGE_NAME:TAG_NAME DOCKER_HUB_USER/IMAGE_NAME
docker push DOCKER_HUB_USER/IMAGE_NAME
```

