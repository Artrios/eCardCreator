function pokemonchoicechange(val,outselect){

    var abilitychoice = document.getElementById(outselect);

    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", '/data/Abilities.txt', false);
    xmlhttp.send();
    if (xmlhttp.status==200) {
        result = xmlhttp.responseText;
    }

    abilities=result.split('\n');
    var count=0;
    var items=[];

    for (let i = 0; i < abilities.length; i++) {

        if(abilities[i].includes(val.replace(" ","_")+"_")){
            items.push(abilities[i].replace(val.replace(" ","_")+"_","").split(" ")[0].replace("_"," "));
            count++;

        }
    }

    var str = ""
    let i = 0;
    for (var item of items) {
        str += "<option value="+i+">" + item + "</option>";
        i++;
    }

    abilitychoice.innerHTML = str;
    if(count<=1){
        abilitychoice.disabled=true;
    }
    else{
        abilitychoice.disabled=false;
    }
}

function openDropdown(i) {
    const dropdown = document.querySelectorAll(".dropdown-box");
    const searchInput = document.querySelectorAll(".search-input input");

    dropdown[i].classList.add("active");
    searchInput[i].focus();
}

function closeDropdown(i) {
    const dropdown = document.querySelectorAll(".dropdown-box");

    dropdown[i].classList.remove("active");
}


function drawMap(tilemapHeight, tilemapWidth, tileSize, tileset) {
  let mapIndex = 0;
  let tilesetCol = 0;
  const canvas = document.getElementById('layer1-canvas');
  const ctx = canvas.getContext('2d')
  const imageData = ctx.createImageData(240, 160);

    for (let row = 0; row < tilemapHeight; row += tileSize) {
      for (let col = 0; col < tilemapWidth; col += tileSize) {
        if(col < 240){
            drawTile(parseInt(level1Map.charCodeAt(mapIndex)), parseInt(level1Map.charCodeAt(mapIndex+1)) >> 4, col, row, tileSize, tileset, imageData, parseInt(level1Map.charCodeAt(mapIndex+1)) & 0xF);
        }
         mapIndex=mapIndex+2;
      }
      tilesetCol++;
    }

    ctx.putImageData(imageData,0, 0);
    ctx.c
}

function drawSprite(spriteHeight, spriteWidth, tileSize, tileset, imgdata, palindex) {

    let tile = 0;
    for (let row = 0; row < spriteHeight; row += tileSize) {
      for (let col = 0; col < spriteWidth; col += tileSize) {
        drawTile(tile, palindex, col, row, tileSize, tileset, imgdata, 0);
        tile++;
      }
    }

}

function drawTile(tileIndex, palIndex, col, row, tilesize, tileset, imageData, flip) {
  // imgpalette = getPalette();
  //console.log(imgpalette);
  //console.log(tileIndex);

  if(flip==4){
    for(let i = 0; i < (tilesize*tilesize)/2; i++){
        setPixelColor(col, row, parseInt(tileset.charCodeAt(((tileIndex)*tilesize*tilesize/2)+(3*(1+Math.floor(i/4))+Math.floor(i/4))-i%4).toString(16),16), palIndex, i, imageData, true);
    }
  }
  else{
    for(let i = 0; i < (tilesize*tilesize)/2; i++){
        setPixelColor(col, row, parseInt(tileset.charCodeAt(((tileIndex)*tilesize*tilesize/2)+i).toString(16),16), palIndex, i, imageData, false);
    }
  }
}

function setPixelColor(col, row, data, palIndex, index, imageData, xflip) {
  //console.log(imgpalette2);
  const byteIndex = Math.floor(index / 2);
  const pixelPosition = index % 2;
  index=index*2;

  switch(palIndex){
    default:
    case 0:
        imgpalette=imgpal1;
        break;
    case 1:
        imgpalette=imgpal2;
        break;
    case 2:
        imgpalette=imgpal3;
        break;
    case 3:
        imgpalette=imgpal4;
        break;
    case 4:
        imgpalette=imgpal5;
        break;
    case 5:
        imgpalette=imgpal6;
        break;
  }



  //if(col===0 && row===0){
  //  console.log((row + Math.floor(index/8))*240+(col + index%8) + 0);
  //  console.log(imgpalette[(data & 0xF)][1]);
  //  console.log((row + Math.floor((index+1)/8))*240+(col + (index+1)%8) + 0);
  //  console.log(imgpalette[(data & 0xF0) >> 4][1]);
  //}
  //else {
  //  console.log(palIndex);
  //  console.log(data >> 4);
  //}
  if(xflip){
    //if(imgpalette[(data & 0xF)][3] != 0){
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 0] = imgpalette[(data & 0xF)][0]; // R
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 1] = imgpalette[(data & 0xF)][1]; // G
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 2] = imgpalette[(data & 0xF)][2]; // B
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 3] = imgpalette[(data & 0xF)][3]; // A
    //}
    //if(imgpalette[(data & 0xF0) >> 4][3] != 0){
        imageData.data[(row + Math.floor((index)/8))*240*4+(col + (index)%8)*4 + 0] = imgpalette[(data & 0xF0) >> 4][0]; // R
        imageData.data[(row + Math.floor((index)/8))*240*4+(col + (index)%8)*4 + 1] = imgpalette[(data & 0xF0) >> 4][1]; // G
        imageData.data[(row + Math.floor((index)/8))*240*4+(col + (index)%8)*4 + 2] = imgpalette[(data & 0xF0) >> 4][2]; // B
        imageData.data[(row + Math.floor((index)/8))*240*4+(col + (index)%8)*4 + 3] = imgpalette[(data & 0xF0) >> 4][3]; // A
    //}
  }
  else{
    //if(imgpalette[(data & 0xF)][3] != 0){
        imageData.data[(row + Math.floor(index/8))*240*4+(col + index%8)*4 + 0] = imgpalette[(data & 0xF)][0]; // R
        imageData.data[(row + Math.floor(index/8))*240*4+(col + index%8)*4 + 1] = imgpalette[(data & 0xF)][1]; // G
        imageData.data[(row + Math.floor(index/8))*240*4+(col + index%8)*4 + 2] = imgpalette[(data & 0xF)][2]; // B
        imageData.data[(row + Math.floor(index/8))*240*4+(col + index%8)*4 + 3] = imgpalette[(data & 0xF)][3]; // A
    //}
    //if(imgpalette[(data & 0xF0) >> 4][3] != 0){
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 0] = imgpalette[(data & 0xF0) >> 4][0]; // R
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 1] = imgpalette[(data & 0xF0) >> 4][1]; // G
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 2] = imgpalette[(data & 0xF0) >> 4][2]; // B
        imageData.data[(row + Math.floor((index+1)/8))*240*4+(col + (index+1)%8)*4 + 3] = imgpalette[(data & 0xF0) >> 4][3]; // A
    //}
  }  //ctx[byteIndex] = imgpalette[data & 0xF0 >> 4];
  
  
  //console.log('5');
}

function getPalette(palettepath) {
  const palette = [];
  var xmlhttp = new XMLHttpRequest();
  var imgpal = null;
  xmlhttp.open("GET", palettepath, false);
  xmlhttp.send();
  if (xmlhttp.status==200) {
      imgpal=xmlhttp.responseText;
  }
  
  // By lines
  var lines = imgpal.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const color = [parseInt(lines[i].split(',')[0]) << 3, parseInt(lines[i].split(',')[1]) << 3, parseInt(lines[i].split(',')[2]) << 3, Math.min(i*255,255)];
    palette.push(color);
  }
  console.log(palette);
  return palette;
}


window.addEventListener("load", () => {
    const dropdownItems = document.querySelectorAll(".dropdown-item");
    const searchInput = document.querySelectorAll(".search-input input");
    const dropdownContent = document.querySelectorAll(".dropdown-content");
    const selectedItem = document.querySelectorAll(".selected-item");
    const dropdown = document.querySelectorAll(".dropdown-box");
    console.log('start')

    window.addEventListener("click", windowClickEvent => {
      for(let i = 0; i < dropdown.length; i++){
        if (dropdown[i].classList.contains("active")) {
            if (!dropdownContent[i].contains(windowClickEvent.target)) {
              closeDropdown(i);
            }
        }
        else if (selectedItem[i].contains(windowClickEvent.target)) {
            searchInput[i].value = "";
            for(let j = 0; j < dropdownContent[i].children[1].children.length; j++){
                dropdownContent[i].children[1].children[j].classList.remove("hide");
            }

            openDropdown(i);
        }
      }
    });

    for(let i = 0; i < dropdown.length; i++){
        for(let j = 0; j < dropdownContent[i].children[1].children.length; j++){
            dropdownContent[i].children[1].children[j].addEventListener("click", () => {
                for(let k = 0; k < dropdownContent[i].children[1].children.length; k++){
                    dropdownContent[i].children[1].children[k].classList.remove("active");
                }

                dropdownContent[i].children[1].children[j].classList.add("active");

                const selectedItemInput = document.querySelectorAll(".selected-item input");

                selectedItemInput[i].value = dropdownContent[i].children[1].children[j].innerHTML;
                selectedItemInput[i].id = dropdownContent[i].children[1].children[j].value;
                if(selectedItem[i].id.includes("Pokemon")){
                    pokemonchoicechange(selectedItemInput[i].value,"Ability"+selectedItemInput[i].name.slice(-1));
                }
                closeDropdown(i);
            })
            
        }
    }

    for(let i = 0; i < dropdown.length; i++){
        searchInput[i].addEventListener("keyup", () => {
        const filter = searchInput[i].value.toLocaleLowerCase();

        for(let j = 0; j < dropdownContent[i].children[1].children.length; j++){
            if (dropdownContent[i].children[1].children[j].innerHTML.toLocaleLowerCase().includes(filter)) {
                dropdownContent[i].children[1].children[j].classList.remove("hide");
            }
            else{
                dropdownContent[i].children[1].children[j].classList.add("hide");
            }
        }
    });
    }

    //Image functions///////////////////////////////////////////
    var xmlhttp = new XMLHttpRequest();
    const canvas = document.getElementById('layer1-canvas');
    const ctx = canvas.getContext('2d');// Setting the color of the rectangle
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, 240, 160);

    console.log('1')
    imgpal1 = getPalette('/data/images/battletrainer1.pal');
    imgpal2 = getPalette('/data/images/battletrainer2.pal');
    imgpal3 = getPalette('/data/images/battletrainer3.pal');
    imgpal4 = getPalette('/data/images/battletrainer4.pal');
    imgpal5 = getPalette('/data/images/battletrainer5.pal');
    imgpal6 = getPalette('/data/images/trainerdoor.pal');
    //xmlhttp.open("GET", '/data/images/battletrainer1.pal', false);
    //xmlhttp.send();
    //if (xmlhttp.status==200) {
    //    imgpal=xmlhttp.responseText;
    //}

    console.log('2')
    var tileset = new ArrayBuffer();
    xmlhttp.open("GET", '/data/images/battletrainer.4bpp', false);
    //xmlhttp.responseType = "arraybuffer";
    xmlhttp.send();
    if (xmlhttp.status==200) {
        tileset=xmlhttp.response;
    }

    console.log('3')
    level1Map = new ArrayBuffer();
    xmlhttp.open("GET", '/data/images/battletrainer.tilemap', false);
    //xmlhttp.responseType = "arraybuffer";
    xmlhttp.send();
    if (xmlhttp.status==200) {
        level1Map=xmlhttp.response;
    }

    //tileset.src = '/data/images/battletrainer.4bpp';
    // tileset.onload = drawFunction;

    let tileSize = 8;
    let tileOutputSize = 1; // can set to 1 for 32px or higher
    let updatedTileSize = tileSize * tileOutputSize;

    let tilesetCol = 16;
    let tilesetRow = 14;
    let tilemapCols = 32;
    let tilemapRows = 20;
    let tilemapHeight = tilemapRows * tileSize;
    let tilemapWidth = tilemapCols * tileSize;

    let mapIndex = 0;
    let sourceX = 0;
    let sourceY = 0;

    drawMap(tilemapHeight, tilemapWidth, tileSize, tileset);


    spriteImage1 = new ArrayBuffer();
    xmlhttp.open("GET", '/data/images/trainers/aroma_lady.4bpp', false);
    //xmlhttp.responseType = "arraybuffer";
    xmlhttp.send();
    if (xmlhttp.status==200) {
        spriteImage1=xmlhttp.response;
    }
    canvas2 = document.getElementById('layer2-canvas');
    ctx2 = canvas2.getContext('2d')
    imageData2 = ctx2.createImageData(240, 160);
    drawSprite(64, 64, 8, spriteImage1, imageData2, 4);
    ctx2.putImageData(imageData2,88, 32);

    spriteImage2 = new ArrayBuffer();
    xmlhttp.open("GET", '/data/images/trainerdoor.4bpp', false);
    //xmlhttp.responseType = "arraybuffer";
    xmlhttp.send();
    if (xmlhttp.status==200) {
        spriteImage2=xmlhttp.response;
    }
    canvas3 = document.getElementById('layer3-canvas');
    ctx3 = canvas3.getContext('2d')
    imageData3 = ctx3.createImageData(240, 160);
    drawSprite(64, 64, 8, spriteImage2, imageData3, 5);
    ctx3.putImageData(imageData3,88, 32);
    ctx3.putImageData(imageData3,88, 64);

    console.log('here1');
    const selectElement = document.querySelector(".TrainerClass");
    const trainerClass = [];
    trainerClass.push('aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'ruin_maniac', 'aroma_lady', 'tuber_f', 'aroma_lady', 'cooltrainer_m', 'cooltrainer_f', 'hex_maniac', 'lady', 'beauty', 'rich_boy', 'pokemaniac', 'aroma_lady', 'black_belt', 'guitarist', 'kindler', 'camper', 'bug_maniac', 'psychic_m', 'psychic_f', 'gentleman', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'school_kid_m', 'school_kid_f', 'aroma_lady', 'pokefan_m', 'pokefan_f', 'expert_m', 'expert_f', 'youngster', 'aroma_lady', 'fisherman', 'triathlete_m_bike', 'aroma_lady', 'triathlete_m_run', 'aroma_lady', 'triathlete_m_swim', 'triathlete_f_swim', 'dragon_tamer', 'bird_keeper', 'ninja_boy', 'battle_girl', 'parasol_lady', 'swimmer_f', 'picnicker', 'aroma_lady', 'sailor', 'aroma_lady', 'aroma_lady', 'collector', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'pkmn_breeder_m', 'pkmn_breeder_f', 'pkmn_ranger_m', 'pkmn_ranger_f', 'aroma_lady', 'aroma_lady', 'aroma_lady', 'lass', 'bug_catcher', 'hiker', 'aroma_lady', 'aroma_lady', 'aroma_lady');
    console.log('here2');

    selectElement.addEventListener("change", (event) => {
        console.log('selected');
        spriteImage1 = new ArrayBuffer();
        xmlhttp.open("GET", '/data/images/trainers/'+trainerClass[event.target.value]+'.4bpp', false);
        //xmlhttp.responseType = "arraybuffer";
        xmlhttp.send();
        if (xmlhttp.status==200) {
            spriteImage1=xmlhttp.response;
        }
        drawSprite(64, 64, 8, spriteImage1, imageData2, 4);
        ctx2.putImageData(imageData2,88, 32);
    });

    
    const colorElement = document.querySelectorAll(".colorChooser");
    for(let i = 0; i < colorElement.length; i++){
        colorElement[i].addEventListener("input", (event) => {
            var palNum = event.target.id.split("-")[1];
            var palIndex = event.target.id.split("-")[2];
            console.log(palNum);
            console.log(palIndex);
            if(palNum === '1'){
                imgpal1[palIndex][0]=parseInt(event.target.value.substring(1), 16) >> 16;
                imgpal1[palIndex][1]=parseInt(event.target.value.substring(1), 16) >> 8 & 0xFF;
                imgpal1[palIndex][2]=parseInt(event.target.value.substring(1), 16) & 0xFF;
            }
            else if(palNum === '2'){
                imgpal2[palIndex][0]=parseInt(event.target.value.substring(1), 16) >> 16;
                imgpal2[palIndex][1]=parseInt(event.target.value.substring(1), 16) >> 8 & 0xFF;
                imgpal2[palIndex][2]=parseInt(event.target.value.substring(1), 16) & 0xFF;
            }
            else if(palNum === '3'){
                imgpal3[palIndex][0]=parseInt(event.target.value.substring(1), 16) >> 16;
                imgpal3[palIndex][1]=parseInt(event.target.value.substring(1), 16) >> 8 & 0xFF;
                imgpal3[palIndex][2]=parseInt(event.target.value.substring(1), 16) & 0xFF;
            }
            else if(palNum === '4'){
                imgpal4[palIndex][0]=parseInt(event.target.value.substring(1), 16) >> 16;
                imgpal4[palIndex][1]=parseInt(event.target.value.substring(1), 16) >> 8 & 0xFF;
                imgpal4[palIndex][2]=parseInt(event.target.value.substring(1), 16) & 0xFF;
            }
            else if(palNum === '5'){
                imgpal5[palIndex][0]=parseInt(event.target.value.substring(1), 16) >> 16;
                imgpal5[palIndex][1]=parseInt(event.target.value.substring(1), 16) >> 8 & 0xFF;
                imgpal5[palIndex][2]=parseInt(event.target.value.substring(1), 16) & 0xFF;
            }
            else if(palNum === '6'){
                imgpal6[palIndex][0]=parseInt(event.target.value.substring(1), 16) >> 16;
                imgpal6[palIndex][1]=parseInt(event.target.value.substring(1), 16) >> 8 & 0xFF;
                imgpal6[palIndex][2]=parseInt(event.target.value.substring(1), 16) & 0xFF;
            }

            drawMap(tilemapHeight, tilemapWidth, tileSize, tileset);
            drawSprite(64, 64, 8, spriteImage1, imageData2, 4);
            ctx2.putImageData(imageData2,88, 32);

            drawSprite(64, 64, 8, spriteImage2, imageData3, 5);
            ctx3.putImageData(imageData3,88, 32);
            ctx3.putImageData(imageData3,88, 64);

        });
    };
});

function openDoors() {
  // Get the checkbox
  var checkBox = document.getElementById("myCheck");

  if (checkBox.innerHTML == "Open Doors"){
    checkBox.innerHTML = "Close Doors";
    ctx3.clearRect(0, 0, 240, 160);
  } else {
    checkBox.innerHTML = "Open Doors";
    ctx3.putImageData(imageData3,88, 32);
    ctx3.putImageData(imageData3,88, 64);
  }
};


function changeColour() {
  // Get the checkbox
  var checkBox = document.getElementById("myCheck");

  if (checkBox.innerHTML == "Open Doors"){
    checkBox.innerHTML = "Close Doors";
    ctx3.clearRect(0, 0, 240, 160);
  } else {
    checkBox.innerHTML = "Open Doors";
    ctx3.putImageData(imageData3,88, 32);
    ctx3.putImageData(imageData3,88, 64);
  }
};
