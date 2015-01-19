@echo off
C:\Python25\python.exe debt_gen.py > input.txt
C:\Python25\python.exe debt_1.py < input.txt > output_1.txt
type output_1.txt
pause
