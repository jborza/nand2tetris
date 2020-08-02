#!/bin/bash
# Usage: ./do-test TestDirectory/TestName
# e.g. do-test ProgramFlow/BasicLoop

DIR=$1
PROG=$(echo $1 | cut -d / -f 2)

python3 VMTranslator.py $DIR/$PROG.vm > $DIR/$PROG.asm
python3 ../06/asm.py $DIR/$PROG.asm > $DIR/$PROG.hack
../../tools/CPUEmulator.sh $DIR/$PROG.tst
diff $DIR/$PROG.cmp $DIR/$PROG.out