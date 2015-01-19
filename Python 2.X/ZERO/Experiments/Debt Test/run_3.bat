@echo off
C:\Python25\python.exe debt_gen.py > input.txt
C:\Python25\python.exe debt_1.py < input.txt > output_1.txt
C:\Python25\python.exe debt_2.py < input.txt > output_2.txt
