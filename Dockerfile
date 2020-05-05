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
    git checkout hsfrac-minimal       && \
    cd ..
    
ENV PYTHONPATH="/home/fenics/fenics_ii/":"$PYTHONPATH"

# cbc.block
RUN git clone https://mirok-w-simula@bitbucket.org/mirok-w-simula/cbc.block.git && \
    cd cbc.block && \
    python3 setup.py install --user && \
    cd ..

RUN git clone https://github.com/MiroK/ulfy.git && \
    cd ulfy && \
    python3 setup.py install --user && \
    cd ..

USER root
