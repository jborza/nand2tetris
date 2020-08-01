#!/bin/bash

DIR=$1
PROG=$(echo $1 | cut -d / -f 2)
#echo $DIR
#echo $PROG

python3 VMTranslator.py $DIR/$PROG.vm > $DIR/$PROG.asm
python3 ../06/asm.py $DIR/$PROG.asm > $DIR/$PROG.hack
../../tools/CPUEmulator.sh $DIR/$PROG.tst