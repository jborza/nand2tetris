python VMTranslator.py StackArithmetic\StackTest\StackTest.vm > StackArithmetic\StackTest\StackTest.asm
python ..\06\asm.py StackArithmetic\StackTest\StackTest.asm > StackArithmetic\StackTest\StackTest.hack
..\..\tools\CPUEmulator.bat StackArithmetic\StackTest\StackTest.tst