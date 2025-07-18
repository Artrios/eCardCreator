# -*- coding: utf-8 -*-
import sys
from eCardCreator.asmquote import asmQuote

def ereadertext(infile, outfile, region):

	out = open(outfile, 'w')

	with open(infile, 'r') as f:
		for asm in f:
			asms = asm.split('"')
			command = asms[0].strip()
			if command == "db":
				# this is only for the American e-Reader; still need to deal with Japanese
				asms[1] = asms[1].replace('\\0', '\x00')
				asms[1] = asms[1].replace('\\n', '\n')
				asms[1] = asms[1].replace('é', '\x7F')

				out.write("\tdb " + asmQuote(asms[1]) + "\n")
			else:
				out.write(asm)
				if "macros.asm" in asm:
					out.write("DEF REGION EQU REGION_{0}\n".format(region))
					out.write('DEF REGION_NAME EQUS "{0}"\n'.format(region))

	f.closed
