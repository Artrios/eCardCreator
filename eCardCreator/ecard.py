import sys
import functools
import subprocess
import eCardCreator.regionalize
import eCardCreator.stripgbc
import eCardCreator.ereadertext
import eCardCreator.checksum

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)
from werkzeug.security import check_password_hash, generate_password_hash

from eCardCreator.db import get_db

bp = Blueprint('ecard', __name__, url_prefix='/ecard')

@bp.route('/battle-e', methods=('GET', 'POST'))
def cardmaker():
    if request.method == 'POST':
        print_request_form(request.form)
        print(request.form)
        
        #subprocess.run(["python3", "eCardCreator/build/scripts/regionalize.py", f"eCardCreator/build/{request.form['TrainerName']}.asm", f"eCardCreator/build/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.tx", get_region(request.form['LanguageSelect']), get_region(request.form['LanguageSelect'])])
        
        print(get_region(request.form['LanguageSelect']))
        eCardCreator.regionalize.regionalize(f"eCardCreator/build/{request.form['TrainerName']}.asm",f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.tx",get_region(request.form['LanguageSelect']),get_region(request.form['LanguageSelect']))
        subprocess.run(["eCardCreator/bin/rgbds/rgbasm", "-M", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.o.d", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.o", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.tx"])
        subprocess.run(["eCardCreator/bin/rgbds/rgblink", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.o"])
        #subprocess.run(["python3", "eCardCreator/build/scripts/stripgbc.py", f"eCardCreator/build/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.bin"])
        #subprocess.run(["python3", "eCardCreator/build/scripts/checksum.py", f"eCardCreator/build/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.bin", f"eCardCreator/build/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.mev"])
        #subprocess.run(["python3", "eCardCreator/build/scripts/ereadertext.py", f"eCardCreator/build/{request.form['TrainerName']}-card.asm",f"eCardCreator/build/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.tx", get_region(request.form['LanguageSelect'])])
        eCardCreator.stripgbc.stripgbc(f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.bin")
        eCardCreator.checksum.checksum(f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.bin", f"eCardCreator/build/output/{request.form['TrainerName']}-{get_region(request.form['LanguageSelect'])}.mev")
        eCardCreator.ereadertext.ereadertext(f"eCardCreator/build/{request.form['TrainerName']}-card.asm", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.tx", get_region(request.form['LanguageSelect']))

        #subprocess.run(["python3", "eCardCreator/build/scripts/regionalize.py", "eCardCreator/build/prologue.asm", "eCardCreator/build/prologue-EN.tx", "EN", "EN"])
        eCardCreator.regionalize.regionalize("eCardCreator/build/prologue.asm",f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.tx",get_region(request.form['LanguageSelect']),get_region(request.form['LanguageSelect']))
        subprocess.run(["eCardCreator/bin/rgbds/rgbasm", "-M", f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.o.d", "-o", f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.o", f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.tx"])
        subprocess.run(["eCardCreator/bin/rgbds/rgblink", "-o", f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.o"])
        #subprocess.run(["python3", "eCardCreator/build/scripts/stripgbc.py", "eCardCreator/build/prologue-EN.gbc", "eCardCreator/build/prologue-EN.bin"])
        eCardCreator.stripgbc.stripgbc(f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/output/prologue-{get_region(request.form['LanguageSelect'])}.bin")

        #subprocess.run(["python3", "eCardCreator/build/scripts/ereadertext.py", "eCardCreator/build/battletrainer.asm", "eCardCreator/build/battletrainer-EN.tx", get_region(request.form['LanguageSelect'])])
        eCardCreator.ereadertext.ereadertext("eCardCreator/build/battletrainer.asm", f"eCardCreator/build/output/battletrainer-{get_region(request.form['LanguageSelect'])}.tx", get_region(request.form['LanguageSelect']))
        subprocess.run(["eCardCreator/bin/rgbds/rgbasm", "-I", "eCardCreator/build", "-M", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.o.d", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.o", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.tx"])
        subprocess.run(["eCardCreator/bin/rgbds/rgblink", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.o"])
        #subprocess.run(["python3", "eCardCreator/build/scripts/stripgbc.py", f"eCardCreator/build/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.z80"])
        eCardCreator.stripgbc.stripgbc(f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.gbc", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.z80")
        subprocess.run(["eCardCreator/bin/nedc/nevpk", "-c", "-i", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.z80", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.vpk"])
        subprocess.run(["eCardCreator/bin/nedc/nedcmake", "-i", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}.vpk", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}", "-type", "1", "-region", "1"])
        subprocess.run(["eCardCreator/bin/nedc/raw2bmp", "-i", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw", "-o", f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01", "-dpi", "600"])

        try:
            return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw")
        except Exception as e:
            return str(e)


    pokelist=[]
    classlist=[]
    naturelist=[]
    itemlist=[]
    movelist=[]
    easychat=[]

    with open("eCardCreator/data/Pokemon.txt","r") as infile:
        for line in infile:
            pokelist.append(line.split('=')[0])

    with open("eCardCreator/data/TrainerClass.txt","r") as infile:
        for line in infile:
            classlist.append(line.strip())

    with open("eCardCreator/data/Natures.txt","r") as infile:
        for line in infile:
            naturelist.append(line.strip())

    with open("eCardCreator/data/Items.txt","r") as infile:
        for line in infile:
            itemlist.append(line.split('=')[0])

    with open("eCardCreator/data/Moves.txt","r") as infile:
        for line in infile:
            movelist.append(line.split('=')[0])

    with open("eCardCreator/data/EasyChat.txt","r") as infile:
        for line in infile:
            easychat.append(line.split('=')[0])
    
    return render_template('ecard/battle-e.html', pokelist=pokelist, classlist=classlist, naturelist=naturelist, itemlist=itemlist, movelist=movelist, easychat=easychat)

def get_region(region):
    match region:
        case "0":
            return "JP"
        case "1":
            return "EN"
        case "3":
            return "FR"
        case "2":
            return "DE"
        case "5":
            return "ES"
        case "4":
            return "IT"

def get_easy(easy_chat):
    with open("eCardCreator/data/EasyChat.txt","r") as infile:
        for line in infile:
            if easy_chat==line.split('=')[0]:
                return line.split('=')[1].strip()
            return '$FFFF'

def get_pokemon(pokemon):
    with open("eCardCreator/data/Pokemon.txt","r") as infile:
        for line in infile:
            if pokemon==line.split('=')[0]:
                return line.split('=')[1].strip()
            return 'SPECIES_NONE'
            
def get_item(item):
    with open("eCardCreator/data/Items.txt","r") as infile:
        for line in infile:
            if item==line.split('=')[0]:
                return line.split('=')[1].strip()
            return 'ITEM_NONE'
            
def get_move(move):
    with open("eCardCreator/data/Moves.txt","r") as infile:
        for line in infile:
            if move==line.split('=')[0]:
                return line.split('=')[1].strip()
            return 'MOVE_NONE'

def get_class(trainerclass):
    with open("eCardCreator/data/TrainerClass.txt","r") as infile:
        for line in infile:
            if trainerclass==line.split('=')[0]:
                return line.split('=')[1].strip()
            return 'AROMA_LADY'
            

def get_color(hexcol):
    rcol=int(hexcol[1:2], 16)
    gcol=int(hexcol[3:4], 16)
    bcol=int(hexcol[5:6], 16)
    return f'{rcol>>3}, {gcol>>3}, {bcol>>3}'

def check_empty(formval):
    if formval=='':
        return '0'
    return formval

def print_request_form(in_form):
    with open(f"eCardCreator/build/{in_form["TrainerName"]}.asm","w") as outfile:
        outfile.write('INCLUDE "eCardCreator/build/trainer_macros.asm"\n')
        outfile.write('    Battle_Trainer\n')
        outfile.write(f'    BT_Level {in_form["BTLevel"]}\n')
        outfile.write(f'    db {get_class(in_form["TrainerClass"])}\n')
        outfile.write(f'    BT_Floor {in_form["BTFloor"]}\n')
        outfile.write(f'    Text_{get_region(in_form['LanguageSelect'])} "{in_form["TrainerName"]}"8\n')
        outfile.write(f'    OT_ID 00000,00000\n')
        outfile.write('\n')
        outfile.write(f'    Intro_{get_region(in_form['LanguageSelect'])} {get_easy(in_form["intro1"])},{get_easy(in_form["intro2"])},{get_easy(in_form["intro3"])},{get_easy(in_form["intro4"])},{get_easy(in_form["intro5"])},{get_easy(in_form["intro6"])}\n')
        outfile.write(f'    Win_{get_region(in_form['LanguageSelect'])} {get_easy(in_form["win1"])},{get_easy(in_form["win2"])},{get_easy(in_form["win3"])},{get_easy(in_form["win4"])},{get_easy(in_form["win5"])},{get_easy(in_form["win6"])}\n')
        outfile.write(f'    Loss_{get_region(in_form['LanguageSelect'])} {get_easy(in_form["lose1"])},{get_easy(in_form["lose2"])},{get_easy(in_form["lose3"])},{get_easy(in_form["lose4"])},{get_easy(in_form["lose5"])},{get_easy(in_form["lose6"])}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {get_pokemon(in_form["Pokemon1"])}\n')
        outfile.write(f'    Holds {get_item(in_form["Pokemon1Item"])}\n')
        outfile.write(f'    Moves {get_move(in_form["Pokemon1Move1"])}, {get_move(in_form["Pokemon1Move2"])}, {get_move(in_form["Pokemon1Move3"])}, {get_move(in_form["Pokemon1Move4"])}\n')
        outfile.write(f'    Level {in_form["Pokemon1Level"]}\n')
        outfile.write(f'    PP_Ups {check_empty(in_form['Pokemon1PP1'])},{check_empty(in_form['Pokemon1PP2'])},{check_empty(in_form['Pokemon1PP3'])},{check_empty(in_form['Pokemon1PP4'])}\n')
        outfile.write(f'    EVs {check_empty(in_form["Pokemon1HPEV"])},{check_empty(in_form["Pokemon1AtkEV"])},{check_empty(in_form["Pokemon1DefEV"])},{check_empty(in_form["Pokemon1SpAtkEV"])},{check_empty(in_form["Pokemon1SpDefEV"])},{check_empty(in_form["Pokemon1SpdEV"])}\n')
        outfile.write(f'    OT_ID {in_form["Pokemon1TID"]},{in_form["Pokemon1SID"]}\n')
        outfile.write(f'    IVs {check_empty(in_form["Pokemon1HPIV"])},{check_empty(in_form["Pokemon1AtkIV"])},{check_empty(in_form["Pokemon1DefIV"])},{check_empty(in_form["Pokemon1SpAtkIV"])},{check_empty(in_form["Pokemon1SpDefIV"])},{check_empty(in_form["Pokemon1SpdIV"])}, {in_form["Pokemon1Nature"]}\n')
        outfile.write(f'    PV ${in_form["Pokemon1PID"]}\n')
        outfile.write(f'    Text_{get_region(in_form['LanguageSelect'])} "{in_form["Pokemon1Nickname"]}"11\n')
        outfile.write(f'    Friendship {in_form['Pokemon1Friendship']}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {get_pokemon(in_form["Pokemon2"])}\n')
        outfile.write(f'    Holds {get_item(in_form["Pokemon2Item"])}\n')
        outfile.write(f'    Moves {get_move(in_form["Pokemon2Move1"])}, {get_move(in_form["Pokemon2Move2"])}, {get_move(in_form["Pokemon2Move3"])}, {get_move(in_form["Pokemon2Move4"])}\n')
        outfile.write(f'    Level {in_form["Pokemon2Level"]}\n')
        outfile.write(f'    PP_Ups {check_empty(in_form['Pokemon2PP1'])},{check_empty(in_form['Pokemon2PP2'])},{check_empty(in_form['Pokemon2PP3'])},{check_empty(in_form['Pokemon2PP4'])}\n')
        outfile.write(f'    EVs {check_empty(in_form["Pokemon2HPEV"])},{check_empty(in_form["Pokemon2AtkEV"])},{check_empty(in_form["Pokemon2DefEV"])},{check_empty(in_form["Pokemon2SpAtkEV"])},{check_empty(in_form["Pokemon2SpDefEV"])},{check_empty(in_form["Pokemon2SpdEV"])}\n')
        outfile.write(f'    OT_ID {in_form["Pokemon2TID"]},{in_form["Pokemon2SID"]}\n')
        outfile.write(f'    IVs {check_empty(in_form["Pokemon2HPIV"])},{check_empty(in_form["Pokemon2AtkIV"])},{check_empty(in_form["Pokemon2DefIV"])},{check_empty(in_form["Pokemon2SpAtkIV"])},{check_empty(in_form["Pokemon2SpDefIV"])},{check_empty(in_form["Pokemon2SpdIV"])}, {in_form["Pokemon2Nature"]}\n')
        outfile.write(f'    PV ${in_form["Pokemon2PID"]}\n')
        outfile.write(f'    Text_{get_region(in_form['LanguageSelect'])} "{in_form["Pokemon2Nickname"]}"11\n')
        outfile.write(f'    Friendship {in_form['Pokemon2Friendship']}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {get_pokemon(in_form["Pokemon3"])}\n')
        outfile.write(f'    Holds {get_item(in_form["Pokemon3Item"])}\n')
        outfile.write(f'    Moves {get_move(in_form["Pokemon3Move1"])}, {get_move(in_form["Pokemon3Move2"])}, {get_move(in_form["Pokemon3Move3"])}, {get_move(in_form["Pokemon3Move4"])}\n')
        outfile.write(f'    Level {in_form["Pokemon3Level"]}\n')
        outfile.write(f'    PP_Ups {check_empty(in_form['Pokemon3PP1'])},{check_empty(in_form['Pokemon3PP2'])},{check_empty(in_form['Pokemon3PP3'])},{check_empty(in_form['Pokemon3PP4'])}\n')
        outfile.write(f'    EVs {check_empty(in_form["Pokemon3HPEV"])},{check_empty(in_form["Pokemon3AtkEV"])},{check_empty(in_form["Pokemon3DefEV"])},{check_empty(in_form["Pokemon3SpAtkEV"])},{check_empty(in_form["Pokemon3SpDefEV"])},{check_empty(in_form["Pokemon3SpdEV"])}\n')
        outfile.write(f'    OT_ID {in_form["Pokemon3TID"]},{in_form["Pokemon3SID"]}\n')
        outfile.write(f'    IVs {check_empty(in_form["Pokemon3HPIV"])},{check_empty(in_form["Pokemon3AtkIV"])},{check_empty(in_form["Pokemon3DefIV"])},{check_empty(in_form["Pokemon3SpAtkIV"])},{check_empty(in_form["Pokemon3SpDefIV"])},{check_empty(in_form["Pokemon3SpdIV"])}, {in_form["Pokemon3Nature"]}\n')
        outfile.write(f'    PV ${in_form["Pokemon3PID"]}\n')
        outfile.write(f'    Text_{get_region(in_form['LanguageSelect'])} "{in_form["Pokemon3Nickname"]}"11\n')
        outfile.write(f'    Friendship {in_form['Pokemon3Friendship']}\n')
        outfile.write('\n')
        outfile.write(f'    End_Trainer')

    with open(f"eCardCreator/build/{in_form["TrainerName"]}-card.asm","w") as outfile:
        outfile.write('INCLUDE "eCardCreator/build/card_macros.asm"\n')
        outfile.write(f'DEF CLASS EQUS   "{get_class(in_form["TrainerClass"]).lower()}"\n')
        outfile.write('DEF TRAINER EQUS "devin"\n')
        outfile.write(f'INCLUDE "eCardCreator/build/battletrainer-{get_region(in_form['LanguageSelect'])}.tx"\n')

    with open(f"eCardCreator/build/sprites/battletrainer1.pal","w") as outfile:
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser11"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser12"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser13"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser14"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser15"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser16"])}\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0')

    with open(f"eCardCreator/build/sprites/battletrainer2.pal","w") as outfile:
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser21"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser22"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser23"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser24"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser25"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser26"])}\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0')

    with open(f"eCardCreator/build/sprites/battletrainer3.pal","w") as outfile:
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser31"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser32"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser33"])}\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write('	RGB  0,  0,  0')

    with open(f"eCardCreator/build/sprites/battletrainer4.pal","w") as outfile:
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser41"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser42"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser43"])}')

    with open(f"eCardCreator/build/sprites/battletrainer5.pal","w") as outfile:
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser51"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser52"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser53"])}')

    with open(f"eCardCreator/build/sprites/trainerdoor.pal","w") as outfile:
        outfile.write('	RGB  0,  0,  0\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser61"])}\n')
        outfile.write(f'	RGB  {get_color(in_form["colorChooser62"])}\n')
        outfile.write('	RGB  0,  0,  0')

