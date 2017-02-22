.orig xFB

; These functions add trap routines to the LC-3 computer. 
; The trap routines are described in the comments beside them
; use trap xfb for read integer
; use trap xfc for print integer
; use trap xfd for subtraction
; use trap xfe for multiplication
; use trap xff for division
; to use these assemble this code and load it before loading your program
; Author: Robert Flack

; 2005/04/24: Adapted to work with current Unix LC-3 simulator
; - replaced "putc" with "OUT" instead
; - replaced binary number literal with hex number literal
; Peter Froehlich <phf@acm.org>

        .fill GetIntProgram   ; Gets an integer into r0 from the keybaord in decimal format
        .fill WriteIntProgram	; Writes r0 as an integer in decimal format
	.fill SubProgram	; Subtracts r0 - r1, storing result in r0
	.fill MultiplyProgram	; Multiplies r0 by r1, storing product in r0
	.fill DivideProgram	; Divides r0 by r1, storing quotient in r0 and remainder in r1

GetIntProgram:

; This trap service routine will input a number naturally, storing it in r0.
; Note: You can press negative (-) as many times as you want and keep reversing
; the sign of the number.

	st r1,SAVE1r1
	st r2,SAVE1r2
	st r3,SAVE1r3
	st r7,SAVE1r7
	and r1,r1,#0
	and r3,r3,#0	; Will the number be negative?
	ld r2,SUBAMT
GetIntNextNum:
	getc
	OUT
	add r0,r0,r2
	brn GetIntNonnumeral
	add r4,r1,r1
	add r1,r4,r4
	add r1,r1,r1
	add r1,r1,r4
	add r1,r1,r0
	brnzp GetIntNextNum
GetIntNonnumeral:
	add r0,r0,#3
	brn GetIntDoneInput
	not r3,r3
	brnzp GetIntNextNum
GetIntDoneInput:
	not r3,r3
	brn GetIntDone
	not r1,r1
	add r1,r1,#1
GetIntDone:
	and r0,r1,#-1
	ld r1,SAVE1r1
	ld r2,SAVE1r2
	ld r3,SAVE1r3
	ld r7,SAVE1r7
	ret
SUBAMT: .fill x-30
SAVE1r1: .blkw 1
SAVE1r2: .blkw 1
SAVE1r3: .blkw 1
SAVE1r7:	.blkw 1

WriteIntProgram:
; Output r0 as a decimal number
	st r1,Save2r1
	st r2,Save2r2
	st r3,Save2r3
	st r4,Save2r4
	st r5,Save2r5
	st r7,Save2r7

	and r5,r5,#0
	and r0,r0,#-1
	brzp WriteBegin
	not r5,r5
	not r0,r0
	add r0,r0,#1

WriteBegin:
	ld r2,WriteIntBaseNum
	lea r4,NumAsStr
	
WriteDetNext:
	ld r1,WriteIntBase
	trap xFF	; Divide number by 10
	
	and r3,r0,#-1	; Save quotient
	add r0,r1,r2	; Add the char "0" to remainder
	
	; Add to stack now
	add r4,r4,#-1
	str r0,r4,#0
	
	and r0,r3,#-1	; Return quotient to r0
	brp WriteDetNext
	
	not r5,r5
	brnp WritePuts
	ld r0,NegSign
	OUT
WritePuts:
	and r0,r4,#-1
	puts
	and r0,r0,#0
	add r0,r0,#10
	OUT

	ld r1,Save2r1
	ld r2,Save2r2
	ld r3,Save2r3
	ld r4,Save2r4
	ld r5,Save2r5
	ld r7,Save2r7
	ret
Save2r1: .blkw 1
Save2r2: .blkw 1
Save2r3: .blkw 1
Save2r4: .blkw 1
Save2r5: .blkw 1
Save2r7: .blkw 1
NegSign: .fill x2D
WriteIntBase: .fill 10
WriteIntBaseNum: .fill x30
	.blkw 7
NumAsStr:
	.fill 0
SubProgram:
	st r1,Save5r1
	st r7,Save5r7
	not r1,r1
	add r1,r1,#1
	add r0,r0,r1
	ld r1,Save5r1
	ld r7,Save5r7
	ret
Save5r1: .blkw 1
Save5r7: .blkw 1

MultiplyProgram:
; This program will multiply r0 by r1 giving r0.
	st r1,SAVE3r1
	st r2,SAVE3r2
	st r3,SAVE3r3
	st r4,SAVE3r4
	st r7,SAVE3r7

	and r0,r0,#-1	; If r0 is negative, invert r1, make r0 positive
	brzp MultNoChange
	not r0,r0
	add r0,r0,#1
	not r1,r1
	add r1,r1,#1

MultNoChange:
	and r2,r2,#0	; This will contain the answer
	and r3,r3,#0
	add r3,r3,#1
DoNextMult:
	and r4,r0,r3
	brz MultNext
	add r2,r2,r1
MultNext:
	add r1,r1,r1	; Double r1
	add r3,r3,r3	; Bit shift r1 to the left
	brn DoneMult
	brnzp DoNextMult
DoneMult:
	and r0,r2,#-1
	ld r1,SAVE3r1
	ld r2,SAVE3r2
	ld r3,SAVE3r3
	ld r4,SAVE3r4
	ld r7,SAVE3r7
	ret
SAVE3r1: .blkw 1
SAVE3r2: .blkw 1
SAVE3r3: .blkw 1
SAVE3r4: .blkw 1
SAVE3r7: .blkw 1
LastMult: .fill x8000;

DivideProgram:
; This program will divide r0 by r1, storing the quotient in r0 and the remainder in r1
	st r2,SAVE4r2
	st r3,SAVE4r3
	st r4,SAVE4r4
	st r5,SAVE4r5
	st r7,SAVE4r7

	and r5,r5,#0

	and r0,r0,#-1	; Check if r0 is negative
	brzp #3
	not r5,r5	; If so, make it positive, but set r5
	not r0,r0
	add r0,r0,#1

	lea r2,DivideNumbers
	add r2,r2,#2

	and r1,r1,#-1	; Check if r1 is negative
	brzp #2
	not r5,r5	; If so, set r5, and skip taking negative of r1
	brnzp #2
	not r1,r1	; Negative of r1
	add r1,r1,#1

	and r4,r4,#0	; Initialize r4 = 0 for quotient

	and r3,r3,#0	; Initalize r3 = 0
	add r3,r3,#1
DivideStoreNext:	; Create a list of all 2^x multiples of numbers
	str r1,r2,#0
	str r3,r2,#1
	add r1,r1,r1
	brzp StartDivision
	add r2,r2,#2
	add r3,r3,r3
	brnzp DivideStoreNext
StartDivision:
	ldr r1,r2,#0
	brzp DoneDivision
	add r0,r0,r1
	brzp DivideNumFits
	not r1,r1		; If num doesn't fit, add it back
	add r1,r1,#1
	add r0,r0,r1
	brnzp DivideNextNum
DivideNumFits:
	ldr r3,r2,#1
	add r4,r4,r3
DivideNextNum:
	add r2,r2,#-2
	brnzp StartDivision
DoneDivision:
	and r1,r0,#-1
	and r0,r4,#-1
	not r5,r5	; Check if it should be negative
	brnp #4
	not r0,r0	; If so, make both quotient and remainder negative
	add r0,r0,#1
	not r1,r1
	add r1,r1,#1

	ld r2,SAVE4r2
	ld r3,SAVE4r3
	ld r4,SAVE4r4
	ld r5,SAVE4r5
	ld r7,SAVE4r7
	ret
SAVE4r2: .blkw 1
SAVE4r3: .blkw 1
SAVE4r4: .blkw 1
SAVE4r5: .blkw 1
SAVE4r7: .blkw 1

DivideNumbers:
	.fill 0
	.fill 0
	.blkw 32
.end

