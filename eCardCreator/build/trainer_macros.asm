INCLUDE "eCardCreator/build/card_macros.asm"
INCLUDE "eCardCreator/build/constants/abilities.asm"
INCLUDE "eCardCreator/build/constants/easychat.asm"
INCLUDE "eCardCreator/build/constants/items.asm"
INCLUDE "eCardCreator/build/constants/moves.asm"
INCLUDE "eCardCreator/build/constants/natures.asm"
INCLUDE "eCardCreator/build/constants/pokemon.asm"
INCLUDE "eCardCreator/build/constants/trainerclasses.asm"

DEF MOSSDEEP EQU 0

MACRO Battle_Trainer
	Section "battle",ROM0[$100]
	db $01
	dd $02000000
	db REGION,0,REGION,0,0,0,$04,0,$80,$01,0,0
	db $0D
	dd $02000018
	db $02,$00
	ENDM

MACRO Hill_Trainer
	REPT 253
		db $00 ; pads the data to 256 bytes
	ENDR
	ENDM

DEF Hill_Num EQUS "dd"
DEF BT_Level EQUS "db"
DEF Class EQUS "db"
DEF BT_Floor EQUS "dw" ; the byte after it is 00, but apparently means something…
MACRO Intro_Text
	dw \1, \2, \3, \4, \5, \6
	ENDM
MACRO Win_Text
	dw \1, \2, \3, \4, \5, \6
	ENDM
MACRO Loss_Text
	dw \1, \2, \3, \4, \5, \6
	ENDM
MACRO After_Text
	dw \1, \2, \3, \4, \5, \6
	ENDM

DEF Pokemon EQUS "dw"
DEF Holds EQUS "dw"
DEF Moves EQUS "dw"
DEF Level EQUS "db"
MACRO PP_Ups
	db (\1) + (\2 << 2) + (\3 << 4) + (\4 << 6)
	ENDM
DEF EVs EQUS "db"
DEF OT_ID EQUS "dw"
MACRO IVs
	dw \1 + (\2 << 5) + (\3 << 10) + ((\4 & 1) << 15)
	dw (\4 >> 1) + (\5 << 4) + (\6 << 9) + (\7 << 15)
	ENDM
MACRO PV
	dw (\1 & $FFFF), (\1 >> 16)
	ENDM
DEF Friendship EQUS "db"

MACRO End_Trainer
	db 0,0,0,0
	EOF
	ENDM
