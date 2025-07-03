# -*- coding: utf-8 -*-
import sys
import eCardCreator.gen3text
import eCardCreator.asmquote

def regionalize(infile, outfile, region, lang):
	out = open(outfile, 'w')
	
	with open(infile, 'r') as f:
		for asm in f:
			asms = asm.split('"')
			command = asms[0].strip()
			if (command == "Text_" + lang) or (command == "Text"):
				asms[1] = eCardCreator.gen3text.utf8ToRSText(asms[1], lang)
				try:
					length = asms[2].split(';')[0] # strip trailing comment
					padding = int(length) - len(asms[1])
					if padding > 0:
						asms[1] += '\xFF'
					for i in range(padding - 1):
						asms[1] += "\x00"
				except ValueError:
					pass
				out.write("\tdb " + eCardCreator.asmquote.asmQuoteBytes(asms[1]) + "\n")
			elif len(command) < 5 or command[0:5] != "Text_":
				out.write(asm)
				if "macros.asm" in asm:
					# can’t do this until after REGION_EN, etc. are loaded
					out.write("DEF REGION EQU REGION_" + region + "\n")
			# else this is foreign text, delete it
	f.closed
