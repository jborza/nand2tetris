python VMTranslator.py StackArithmetic\SimpleAdd\SimpleAdd.vm > StackArithmetic\SimpleAdd\SimpleAdd.asm
python ..\06\asm.py StackArithmetic\SimpleAdd\SimpleAdd.asm > StackArithmetic\SimpleAdd\SimpleAdd.hack
..\..\tools\CPUEmulator.bat StackArithmetic\SimpleAdd\SimpleAdd.tst