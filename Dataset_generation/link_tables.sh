#!/bin/bash

tables=(co_classidx co_rep co_sym conj_twist conj_ud_edges fs_classidx fs_rep fs_sym move_corners move_d_edges move_flip move_slice_sorted move_twist move_u_edges move_ud_edges phase1_prun phase2_cornsliceprun phase2_edgemerge phase2_prun)

for file in ${tables[*]}
do
	ln -sv RubiksCube_TwophaseSolver/$file || :
done
