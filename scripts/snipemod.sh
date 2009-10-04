#!/bin/bash

find ~/quarantine/* -type d -amin -1 -print| while read FILE
do	
	chmod -R 000 $FILE
done

find ~/quarantine/* -type f -amin -1 -print| while read FILE
do	
	chmod -R 000 $FILE
done
