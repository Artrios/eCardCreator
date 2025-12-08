import sys
import functools
import subprocess
import eCardCreator.regionalize
import eCardCreator.stripgbc
import eCardCreator.ereadertext
import eCardCreator.checksum
import zipfile

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)
from werkzeug.security import check_password_hash, generate_password_hash

from eCardCreator.db import get_db

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/ecardcreator', methods=('GET', 'POST'))
def mainpage():

    return render_template('ecard/main.html')

@bp.route('/ecardcreator/battle_trainer', methods=('GET', 'POST'))
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

        if request.form['type'] == "raw":
            try:
                return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw")
            except Exception as e:
                return str(e)
        elif request.form['type'] == "bmp":
            try:
                return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.bmp", as_attachment=True)
            except Exception as e:
                return str(e)
        else:
            try:
                zip_file_path = f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as myzip:
                    myzip.write(f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw", arcname=f"{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw")
                    myzip.write(f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.bmp", arcname=f"{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.bmp")
                    myzip.write(f"eCardCreator/build/{request.form['TrainerName']}.asm", arcname=f"{request.form['TrainerName']}.asm")
                    myzip.write(f"eCardCreator/build/{request.form['TrainerName']}-card.asm", arcname=f"{request.form['TrainerName']}-card.asm")
                return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.zip")
            except Exception as e:
                return str(e)


    pokelist=[]
    classlist=[]
    naturelist=[]
    itemlist=[]
    movelist=[]
    easychat=[]

    with open("eCardCreator/data/EN/Pokemon.txt","r") as infile:
        for line in infile:
            pokelist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/TrainerClass.txt","r") as infile:
        for line in infile:
            classlist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/Natures.txt","r") as infile:
        for line in infile:
            naturelist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/Items.txt","r") as infile:
        for line in infile:
            itemlist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/Moves.txt","r") as infile:
        for line in infile:
            movelist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/EasyChat.txt","r") as infile:
        for line in infile:
            easychat.append(line.split('=')[0])
    
    return render_template('ecard/battle-e.html', pokelist=pokelist, classlist=classlist, naturelist=naturelist, itemlist=itemlist, movelist=movelist, easychat=easychat)

@bp.route('/ecardcreator/trainer_hill', methods=('GET', 'POST'))
def cardmaker_th():
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

        if request.form['type'] == "raw":
            try:
                return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw")
            except Exception as e:
                return str(e)
        elif request.form['type'] == "bmp":
            try:
                return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.bmp", as_attachment=True)
            except Exception as e:
                return str(e)
        else:
            try:
                zip_file_path = f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.zip"
                with zipfile.ZipFile(zip_file_path, 'w') as myzip:
                    myzip.write(f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw", arcname=f"{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.raw")
                    myzip.write(f"eCardCreator/build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.bmp", arcname=f"{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.bmp")
                    myzip.write(f"eCardCreator/build/{request.form['TrainerName']}.asm", arcname=f"{request.form['TrainerName']}.asm")
                    myzip.write(f"eCardCreator/build/{request.form['TrainerName']}-card.asm", arcname=f"{request.form['TrainerName']}-card.asm")
                return send_file(f"build/output/{request.form['TrainerName']}-card-{get_region(request.form['LanguageSelect'])}-01.zip")
            except Exception as e:
                return str(e)


    pokelist=[]
    classlist=[]
    naturelist=[]
    itemlist=[]
    movelist=[]
    easychat=[]

    with open("eCardCreator/data/EN/Pokemon.txt","r") as infile:
        for line in infile:
            pokelist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/TrainerClass.txt","r") as infile:
        for line in infile:
            classlist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/Natures.txt","r") as infile:
        for line in infile:
            naturelist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/Items.txt","r") as infile:
        for line in infile:
            itemlist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/Moves.txt","r") as infile:
        for line in infile:
            movelist.append(line.split('=')[0])

    with open("eCardCreator/data/EN/EasyChat.txt","r") as infile:
        for line in infile:
            easychat.append(line.split('=')[0])
    
    return render_template('ecard/trainer-hill.html', pokelist=pokelist, classlist=classlist, naturelist=naturelist, itemlist=itemlist, movelist=movelist, easychat=easychat)


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

def get_easy(easy_chat,region):
    with open(f"eCardCreator/data/{region}/EasyChat.txt","r") as infile:
        for line in infile:
            if easy_chat==line.split('=')[0]:
                return line.split('=')[1].strip()
    return '$FFFF'

def get_pokemon(pokemon,region):
    with open(f"eCardCreator/data/{region}/Pokemon.txt","r") as infile:
        for line in infile:
            if pokemon==line.split('=')[0]:
                return line.split('=')[1].strip()
    return 'SPECIES_NONE'
            
def get_item(item,region):
    with open(f"eCardCreator/data//{region}/Items.txt","r") as infile:
        for line in infile:
            if item==line.split('=')[0]:
                return line.split('=')[1].strip()
    return 'ITEM_NONE'
            
def get_move(move,region):
    with open(f"eCardCreator/data/{region}/Moves.txt","r") as infile:
        for line in infile:
            if move==line.split('=')[0]:
                return line.split('=')[1].strip()
    return 'MOVE_NONE'

def get_class(trainerclass,region):
    with open(f"eCardCreator/data/{region}/TrainerClass.txt","r") as infile:
        for line in infile:
            if trainerclass==line.split('=')[0]:
                return line.split('=')[1].strip()
    return '$00'

def get_class_string(trainerclass,region):
    #if region=='EN':
    #    return trainerclass
    
    #with open(f"eCardCreator/data/{region}/TrainerClass.txt","r") as infile:
    #   for line in infile:
    #        if trainerclass==line.split('=')[0]:
    #            trainerclass=line.split('=')[1].strip()
    #        break
    print('HOHOHO')
    print(f'{int(trainerclass):02X}')
    with open("eCardCreator/data/EN/TrainerClass.txt","r") as infile:
        for line in infile:
            if f'{int(trainerclass):02X}'==line.split('=$')[1].strip():
                return line.split('=')[0].strip()
    
    return 'aroma_lady'

def get_nature(nature):
    with open("eCardCreator/data/EN/Natures.txt","r") as infile:
        i=0
        for line in infile:
            if int(nature)==i:
                return line.split('=')[1].strip()
            i=i+1
    
    return 'HARDY'                  

def get_color(hexcol):
    print(hexcol)
    rcol=int(hexcol[1:3], 16)
    gcol=int(hexcol[3:5], 16)
    bcol=int(hexcol[5:7], 16)
    print(gcol)
    return f'{rcol>>3}, {gcol>>3}, {bcol>>3}'

def check_empty(formval):
    if formval=='':
        return '0'
    return formval

def print_request_form(in_form):
    print(in_form)
    region = get_region(in_form['LanguageSelect'])
    
    if('Pokemon1Shiny' in in_form):
        PV1='SHINY_'+get_nature(in_form['Pokemon1Nature'])+'_'+in_form['Pokemon1Gender']
    else:
        PV1=get_nature(in_form['Pokemon1Nature'])+'_'+in_form['Pokemon1Gender']

    if('Pokemon2Shiny' in in_form):
        PV2='SHINY_'+get_nature(in_form['Pokemon2Nature'])+'_'+in_form['Pokemon2Gender']
    else:
        PV2=get_nature(in_form['Pokemon2Nature'])+'_'+in_form['Pokemon2Gender']

    if('Pokemon3Shiny' in in_form):
        PV3='SHINY_'+get_nature(in_form['Pokemon3Nature'])+'_'+in_form['Pokemon2Gender']
    else:
        PV3=get_nature(in_form['Pokemon3Nature'])+'_'+in_form['Pokemon2Gender']

    with open(f"eCardCreator/build/{in_form["TrainerName"]}.asm","w") as outfile:
        outfile.write('INCLUDE "eCardCreator/build/trainer_macros.asm"\n')
        outfile.write('    Battle_Trainer\n')
        outfile.write(f'    BT_Level {in_form["BTLevel"]}\n')
        outfile.write(f'    db {in_form["TrainerClass"]}\n')
        outfile.write(f'    BT_Floor {in_form["BTFloor"]}\n')
        outfile.write(f'    Text_{region} "{in_form["TrainerName"]}"8\n')
        outfile.write(f'    OT_ID 00000,00000\n')
        outfile.write('\n')
        outfile.write(f'    Intro_Text {get_easy(in_form["intro1"],region)},{get_easy(in_form["intro2"],region)},{get_easy(in_form["intro3"],region)},{get_easy(in_form["intro4"],region)},{get_easy(in_form["intro5"],region)},{get_easy(in_form["intro6"],region)}\n')
        outfile.write(f'    Win_Text {get_easy(in_form["win1"],region)},{get_easy(in_form["win2"],region)},{get_easy(in_form["win3"],region)},{get_easy(in_form["win4"],region)},{get_easy(in_form["win5"],region)},{get_easy(in_form["win6"],region)}\n')
        outfile.write(f'    Loss_Text {get_easy(in_form["lose1"],region)},{get_easy(in_form["lose2"],region)},{get_easy(in_form["lose3"],region)},{get_easy(in_form["lose4"],region)},{get_easy(in_form["lose5"],region)},{get_easy(in_form["lose6"],region)}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {get_pokemon(in_form["Pokemon1"],region)}\n')
        outfile.write(f'    Holds {get_item(in_form["Pokemon1Item"],region)}\n')
        outfile.write(f'    Moves {get_move(in_form["Pokemon1Move1"],region)}, {get_move(in_form["Pokemon1Move2"],region)}, {get_move(in_form["Pokemon1Move3"],region)}, {get_move(in_form["Pokemon1Move4"],region)}\n')
        outfile.write(f'    Level {in_form["Pokemon1Level"]}\n')
        outfile.write(f'    PP_Ups {check_empty(in_form['Pokemon1PP1'])},{check_empty(in_form['Pokemon1PP2'])},{check_empty(in_form['Pokemon1PP3'])},{check_empty(in_form['Pokemon1PP4'])}\n')
        outfile.write(f'    EVs {check_empty(in_form["Pokemon1HPEV"])},{check_empty(in_form["Pokemon1AtkEV"])},{check_empty(in_form["Pokemon1DefEV"])},{check_empty(in_form["Pokemon1SpAtkEV"])},{check_empty(in_form["Pokemon1SpDefEV"])},{check_empty(in_form["Pokemon1SpdEV"])}\n')
        outfile.write(f'    OT_ID 00000, 00000\n')
        outfile.write(f'    IVs {check_empty(in_form["Pokemon1HPIV"])},{check_empty(in_form["Pokemon1AtkIV"])},{check_empty(in_form["Pokemon1DefIV"])},{check_empty(in_form["Pokemon1SpAtkIV"])},{check_empty(in_form["Pokemon1SpDefIV"])},{check_empty(in_form["Pokemon1SpdIV"])}, {in_form["Pokemon1Ability"]}\n')
        outfile.write(f'    PV {PV1}\n')
        outfile.write(f'    Text_{region} "{in_form["Pokemon1Nickname"]}"11\n')
        outfile.write(f'    Friendship {in_form['Pokemon1Friendship']}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {get_pokemon(in_form["Pokemon2"],region)}\n')
        outfile.write(f'    Holds {get_item(in_form["Pokemon2Item"],region)}\n')
        outfile.write(f'    Moves {get_move(in_form["Pokemon2Move1"],region)}, {get_move(in_form["Pokemon2Move2"],region)}, {get_move(in_form["Pokemon2Move3"],region)}, {get_move(in_form["Pokemon2Move4"],region)}\n')
        outfile.write(f'    Level {in_form["Pokemon2Level"]}\n')
        outfile.write(f'    PP_Ups {check_empty(in_form['Pokemon2PP1'])},{check_empty(in_form['Pokemon2PP2'])},{check_empty(in_form['Pokemon2PP3'])},{check_empty(in_form['Pokemon2PP4'])}\n')
        outfile.write(f'    EVs {check_empty(in_form["Pokemon2HPEV"])},{check_empty(in_form["Pokemon2AtkEV"])},{check_empty(in_form["Pokemon2DefEV"])},{check_empty(in_form["Pokemon2SpAtkEV"])},{check_empty(in_form["Pokemon2SpDefEV"])},{check_empty(in_form["Pokemon2SpdEV"])}\n')
        outfile.write(f'    OT_ID 00000, 00000\n')
        outfile.write(f'    IVs {check_empty(in_form["Pokemon2HPIV"])},{check_empty(in_form["Pokemon2AtkIV"])},{check_empty(in_form["Pokemon2DefIV"])},{check_empty(in_form["Pokemon2SpAtkIV"])},{check_empty(in_form["Pokemon2SpDefIV"])},{check_empty(in_form["Pokemon2SpdIV"])}, {in_form["Pokemon2Ability"]}\n')
        outfile.write(f'    PV {PV2}\n')
        outfile.write(f'    Text_{region} "{in_form["Pokemon2Nickname"]}"11\n')
        outfile.write(f'    Friendship {in_form['Pokemon2Friendship']}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {get_pokemon(in_form["Pokemon3"],region)}\n')
        outfile.write(f'    Holds {get_item(in_form["Pokemon3Item"],region)}\n')
        outfile.write(f'    Moves {get_move(in_form["Pokemon3Move1"],region)}, {get_move(in_form["Pokemon3Move2"],region)}, {get_move(in_form["Pokemon3Move3"],region)}, {get_move(in_form["Pokemon3Move4"],region)}\n')
        outfile.write(f'    Level {in_form["Pokemon3Level"]}\n')
        outfile.write(f'    PP_Ups {check_empty(in_form['Pokemon3PP1'])},{check_empty(in_form['Pokemon3PP2'])},{check_empty(in_form['Pokemon3PP3'])},{check_empty(in_form['Pokemon3PP4'])}\n')
        outfile.write(f'    EVs {check_empty(in_form["Pokemon3HPEV"])},{check_empty(in_form["Pokemon3AtkEV"])},{check_empty(in_form["Pokemon3DefEV"])},{check_empty(in_form["Pokemon3SpAtkEV"])},{check_empty(in_form["Pokemon3SpDefEV"])},{check_empty(in_form["Pokemon3SpdEV"])}\n')
        outfile.write(f'    OT_ID 00000, 00000\n')
        outfile.write(f'    IVs {check_empty(in_form["Pokemon3HPIV"])},{check_empty(in_form["Pokemon3AtkIV"])},{check_empty(in_form["Pokemon3DefIV"])},{check_empty(in_form["Pokemon3SpAtkIV"])},{check_empty(in_form["Pokemon3SpDefIV"])},{check_empty(in_form["Pokemon3SpdIV"])}, {in_form["Pokemon3Ability"]}\n')
        outfile.write(f'    PV {PV3}\n')
        outfile.write(f'    Text_{region} "{in_form["Pokemon3Nickname"]}"11\n')
        outfile.write(f'    Friendship {in_form['Pokemon3Friendship']}\n')
        outfile.write('\n')
        outfile.write(f'    End_Trainer')

    with open(f"eCardCreator/build/{in_form["TrainerName"]}-card.asm","w") as outfile:
        outfile.write('INCLUDE "eCardCreator/build/card_macros.asm"\n')
        outfile.write(f'DEF CLASS EQUS   "{get_class_string(in_form["TrainerClass"],region).replace('(','').replace(')','').replace(' ','_').lower()}"\n')
        outfile.write(f'DEF TRAINER EQUS "{in_form["TrainerName"]}"\n')
        outfile.write(f'DEF BOX1LINE1 EQUS "{in_form["sendText"].split("\r\n")[0]}\\n"\n')
        outfile.write(f'DEF BOX1LINE2 EQUS "{in_form["sendText"].split("\r\n")[1]}\\n"\n')
        outfile.write(f'DEF BOX1LINE3 EQUS "{in_form["sendText"].split("\r\n")[2]}\\n"\n')
        outfile.write(f'DEF BOX1LINE4 EQUS "{in_form["sendText"].split("\r\n")[3]}\\0"\n')
        outfile.write(f'DEF BOX2LINE1 EQUS "{in_form["sendText2"].split("\r\n")[0]}\\n"\n')
        outfile.write(f'DEF BOX2LINE2 EQUS "{in_form["sendText2"].split("\r\n")[1]}\\n"\n')
        outfile.write(f'DEF BOX2LINE3 EQUS "{in_form["sendText2"].split("\r\n")[2]}\\0"\n')
        outfile.write(f'INCLUDE "eCardCreator/build/output/battletrainer-{region}.tx"\n')

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

