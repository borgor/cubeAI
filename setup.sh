#!/bin/bash

git submodule init
git submodule update

pushd Dataset_generation

RENDERER_DIR=MagicCube
SOLVER_DIR=RubiksCube_TwophaseSolver

pushd $RENDERER_DIR/code
git checkout -q 0c2d023d78b1942218d9fd75c3430c67ff462208
2to3 -w cube.py
popd

pushd $SOLVER_DIR
git checkout -q ff6c6ed2a8566826a9d373071b78e3ffa33e3dff
python3 example.py
popd
bash ./link_tables.sh

