#!/bin/bash

dirlist=$(ls "./tmp_files/split_videos/val/"| sort -n)

for dir in $dirlist
do
	pushd ./tmp_files/split_videos/val/$dir

	for f in *.avi
	do
		mkdir -p "../../../../datasets/UCF101/ValData/0.25_196/"
		ffmpeg -ss 1 -i "$f" -r 0.25 -s 196x196 "../../../../datasets/UCF101/ValData/0.25_196/${f%.avi}"_%02d.jpg
	done
	echo $dir
	ls
	popd
done

