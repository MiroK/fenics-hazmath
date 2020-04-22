# Base image
FROM quay.io/fenicsproject/dev

USER root

ENV PYTHONPATH=""

USER fenics

# xii dependency - which avoids scipy.linalg import eigh_tridiagonal
RUN git clone https://github.com/nschloe/quadpy.git && \
    cd quadpy && \
    git checkout v0.12.10 && \
    python3 setup.py install --user && \
    cd ..

# Get fenics_ii from Ana
RUN git clone https://github.com/MiroK/fenics_ii.git && \
    cd fenics_ii && \
    git fetch --all  && \
    git checkout f2019.1-py3.6       && \
    git checkout -b dcfaa36aef7eb18969e96213e2e758ecb9d6390d && \
    cd ..
    
ENV PYTHONPATH="/home/fenics/fenics_ii/":"$PYTHONPATH"

# cbc.block
RUN git clone https://mirok@bitbucket.org/fenics-apps/cbc.block.git && \
    cd cbc.block && \
    python3 setup.py install --user && \
    cd ..

USER root
# Release
# Might need to do docker login 
# docker build --no-cache -t name .
# docker tag name:latest dockerhub...
# docker push mirok/neuronmi

# To user
# docker run -it -v $(pwd):/home/fenics/shared hazmath_dev
