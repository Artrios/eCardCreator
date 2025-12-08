function pokemonchoicechange(val,outselect){
    var languageBox = document.getElementById("language-field");
    var abilitychoice = document.getElementById(outselect);

    var lang = "EN";
    if (languageBox.value == 0) {
        lang="JP";
    }
    else if (languageBox.value == 1) {
        lang = "EN";
    }
    else if (languageBox.value == 2) {
        lang = "DE";
    }
    else if (languageBox.value == 3) {
        lang = "FR";
    }
    else if (languageBox.value == 4) {
        lang = "IT";
    }
    else if (languageBox.value == 5) {
        lang = "ES";
    }

    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", '/data/'+lang+'/Abilities.txt', false);
    xmlhttp.send();
    if (xmlhttp.status==200) {
        result = xmlhttp.responseText;
    }

    abilities=result.split('\n');
    var count=0;
    var items=[];

    for (let i = 0; i < abilities.length; i++) {

        if(abilities[i].includes(val.replace(" ","_")+"=")){
            items.push(abilities[i].replace(val.replace(" ","_")+"=","").split("=")[0].replace("_"," "));
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
    //if(count<=1){
    //    abilitychoice.disabled=true;
    //}
    //else{
    //    abilitychoice.disabled=false;
    //}
}

function getBase64Image(img) {
    // Create an empty canvas element
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    // Copy the image contents to the canvas
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    // Get the data-URL formatted image
    // Firefox supports PNG and JPEG. You could check img.src to
    // guess the original format, but be aware the using "image/jpg"
    // will re-encode the image.
    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
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
    const searchInput = document.querySelectorAll(".search-input input");
    const dropdownContent = document.querySelectorAll(".dropdown-content");
    const selectedItem = document.querySelectorAll(".selected-item");
    const dropdown = document.querySelectorAll(".dropdown-box");
    const canvastileset = document.getElementById("layer2-canvas");
    const tileset = document.getElementById("tileset");
    const tilemap = document.getElementById("tilemap");
    console.log('start')
    var x = 0;
    var y = 0;

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
                const nicknameInput = document.querySelectorAll(".PokemonNickname");

                selectedItemInput[i].value = dropdownContent[i].children[1].children[j].innerHTML;
                selectedItemInput[i].id = dropdownContent[i].children[1].children[j].value;
                if(selectedItem[i].id.includes("Pokemon")){
                    pokemonchoicechange(selectedItemInput[i].value,"Ability"+selectedItemInput[i].name.slice(-1));
                    nicknameInput[selectedItemInput[i].name.slice(-1)-1].value = selectedItemInput[i].value;
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


    canvas1 = document.getElementById('map-canvas');
    mapImage = new Image();
    mapImage.src = '/data/images/TH_map.png'
    ctx = canvas1.getContext('2d');
    mapImage.onload = () => {
        ctx.drawImage(mapImage, 0, 0, 240, 320); // Draw the image at position (0,0)
    };
    //canvas1.width=240;
    //canvas1.height=320;

    canvasTileSet = document.getElementById('tiles-canvas');
    mapImage2 = new Image();
    mapImage2.src = '/data/images/TH_tileset.png'
    ctx3 = canvasTileSet.getContext('2d');
    mapImage2.onload = () => {
        ctx3.drawImage(mapImage2, 0, 0, 128, 512); // Draw the image at position (0,0)
    };


    canvas2 = document.getElementById('layer2-canvas');
    var xmlhttp = new XMLHttpRequest();
    var imgpal = null;
    spriteImage1 = new Image();
    xmlhttp.open("GET", '/data/images/tile_selector.png', false);
    //xmlhttp.responseType = "arraybuffer";
    xmlhttp.send();
    if (xmlhttp.status==200) {
        imgpal=xmlhttp.response;
    }
    spriteImage1.src = '/data/images/tile_selector.png';
    ctx2 = canvas2.getContext('2d');


    canvastileset.addEventListener("click", function(event) {
        const rect = canvastileset.getBoundingClientRect();
        x = event.clientX - rect.left;
        y = event.clientY - rect.top;
        ctx2.clearRect(0, 0, 128, 512);
        
        //imageData2 = ctx2.createImageData(128, 512);
        x = x - (x % 16) - 1;
        y = y - (y % 16) - 1;
        console.log(x);
        console.log(y);
        ctx2.drawImage(spriteImage1, x, y);
    });

    /*canvas1.addEventListener("click", function(event) {
        const rect = canvas1.getBoundingClientRect();
        const imageData = ctx.getImageData(0, 0, canvas1.width, canvas1.height);

        x2 = event.clientX - rect.left;
        y2 = event.clientY - rect.top;
        x2 = x2 - (x2 % 16);
        y2 = y2 - (y2 % 16);
        


        ctx.putImageData(ctx3.getImageData(x+1, y+1, 16, 16), x2, y2, 0, 0, 16, 16);
    });*/

    let isDragging = false;

    canvas1.addEventListener('mousedown', (event) => {
        switch (event.button) {
            case 0:
                isDragging = true;

                const rect = canvas1.getBoundingClientRect();
                const imageData = ctx.getImageData(0, 0, canvas1.width, canvas1.height);

                x2 = event.clientX - rect.left;
                y2 = event.clientY - rect.top;
                x2 = x2 - (x2 % 16);
                y2 = y2 - (y2 % 16);

                if(y2>=80){
                    ctx.putImageData(ctx3.getImageData(x+1, y+1, 16, 16), x2, y2, 0, 0, 16, 16);
                }

                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
                break;
            case 2:
                const rect2 = canvas1.getBoundingClientRect();
                x2 = event.clientX - rect2.left;
                y2 = event.clientY - rect2.top;
                x2 = x2 - (x2 % 16);
                y2 = y2 - (y2 % 16);
                const imageData2 = ctx.getImageData(x2, y2, 16, 16);
                console.log("searching");

                for(i=0;i<128;i=i+16){
                    console.log(i);
                    for(j=0;j<512;j=j+16){
                        console.log(j);
                        if(getBase64Image(imageData2)==getBase64Image(ctx3.getImageData(i,j,16,16))){
                            console.log("found");
                            ctx2.clearRect(0, 0, 128, 512);
                            x=i-1;
                            y=j-1;
                            ctx2.drawImage(spriteImage1, x, y);
                        }
                    }
                }

                break;
            default:
                break;
        }

    });

    function onMouseMove(event) {
        if (!isDragging) return;

        const rect = canvas1.getBoundingClientRect();
        const imageData = ctx.getImageData(0, 0, canvas1.width, canvas1.height);

        x2 = event.clientX - rect.left;
        y2 = event.clientY - rect.top;
        x2 = x2 - (x2 % 16);
        y2 = y2 - (y2 % 16);

        if(y2>=80){
            ctx.putImageData(ctx3.getImageData(x+1, y+1, 16, 16), x2, y2, 0, 0, 16, 16);
        }
    }

    function onMouseUp() {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }

});

function openDoors() {
  // Get the checkbox
  var checkBox = document.getElementById("myCheck");
  var textBox = document.getElementsByName("sendText2");

  if (checkBox.innerHTML == "Open Doors"){
    checkBox.innerHTML = "Close Doors";
    ctx3.clearRect(0, 0, 240, 160);
    textBox[0].style.visibility = "visible";
  } else {
    checkBox.innerHTML = "Open Doors";
    ctx3.putImageData(imageData3,88, 32);
    ctx3.putImageData(imageData3,88, 64);
    textBox[0].style.visibility = "hidden";
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

function changeLanguage() {
    var languageBox = document.getElementById("language-field");
    const easydropdownContent = document.getElementsByName("easychat");
    const pokemondropdownContent = document.getElementsByName("pokemondropdown");
    const movedropdownContent = document.getElementsByName("movedropdown");
    const itemdropdownContent = document.getElementsByName("itemdropdown");
    const classdropdownContent = document.getElementsByName("TrainerClass");
    var lang = "EN";

    var xmlhttp = new XMLHttpRequest();
    if (languageBox.value == 0) {
        lang="JP";
    }
    else if (languageBox.value == 1) {
        lang = "EN";
    }
    else if (languageBox.value == 2) {
        lang = "DE";
    }
    else if (languageBox.value == 3) {
        lang = "FR";
    }
    else if (languageBox.value == 4) {
        lang = "IT";
    }
    else if (languageBox.value == 5) {
        lang = "ES";
    }


    xmlhttp.open("GET", '/data/'+lang+'/TrainerClass.txt', false);

    var easyText = new String();
    xmlhttp.send();
    if (xmlhttp.status==200) {
        easyText=xmlhttp.response;
    }
    easyTextLines=easyText.split('\n');

    for(let i = 0; i < classdropdownContent.length; i++){
        for(let j = 0; j < classdropdownContent[i].length; j++){
            classdropdownContent[i].children[j].innerHTML=easyTextLines[j].split('=')[0];
        }
    }





    xmlhttp.open("GET", '/data/'+lang+'/EasyChat.txt', false);

    var easyText = new String();
    xmlhttp.send();
    if (xmlhttp.status==200) {
        easyText=xmlhttp.response;
    }
    easyTextLines=easyText.split('\n');

    console.log(easydropdownContent[1].children[1].children[1]);
    for(let i = 0; i < easydropdownContent.length; i++){
        for(let j = 0; j < easydropdownContent[i].children[1].children.length; j++){
            easydropdownContent[i].children[1].children[j].innerHTML=easyTextLines[j].split('=')[0];
        }
    }


    xmlhttp.open("GET", '/data/'+lang+'/Pokemon.txt', false);

    var easyText = new String();
    xmlhttp.send();
    if (xmlhttp.status==200) {
        easyText=xmlhttp.response;
    }
    easyTextLines=easyText.split('\n');

    console.log(pokemondropdownContent[1].children[1].children[1]);
    for(let i = 0; i < pokemondropdownContent.length; i++){
        for(let j = 0; j < pokemondropdownContent[i].children[1].children.length; j++){
            pokemondropdownContent[i].children[1].children[j].innerHTML=easyTextLines[j].split('=')[0];
        }
    }

    xmlhttp.open("GET", '/data/'+lang+'/Moves.txt', false);

    var easyText = new String();
    xmlhttp.send();
    if (xmlhttp.status==200) {
        easyText=xmlhttp.response;
    }
    easyTextLines=easyText.split('\n');

    console.log(movedropdownContent[1].children[1].children[1]);
    for(let i = 0; i < movedropdownContent.length; i++){
        for(let j = 0; j < movedropdownContent[i].children[1].children.length; j++){
            movedropdownContent[i].children[1].children[j].innerHTML=easyTextLines[j].split('=')[0];
        }
    }

    xmlhttp.open("GET", '/data/'+lang+'/Items.txt', false);

    var easyText = new String();
    xmlhttp.send();
    if (xmlhttp.status==200) {
        easyText=xmlhttp.response;
    }
    easyTextLines=easyText.split('\n');

    for(let i = 0; i < itemdropdownContent.length; i++){
        for(let j = 0; j < itemdropdownContent[i].children[1].children.length; j++){
            itemdropdownContent[i].children[1].children[j].innerHTML=easyTextLines[j].split('=')[0];
        }
    }

    xmlhttp.open("GET", '/data/'+lang+'/Natures.txt', false);

    var easyText = new String();
    xmlhttp.send();
    if (xmlhttp.status==200) {
        easyText=xmlhttp.response;
    }
    easyTextLines=easyText.split('\n');

    for(let i = 1; i < 4; i++){
        const naturedropdownContent = document.getElementById("nat"+i);
        console.log(naturedropdownContent.children[0].innerHTML);
        for(let j = 0; j < naturedropdownContent.length; j++){
            naturedropdownContent.children[j].innerHTML=easyTextLines[j].split('=')[0];
        }
    }
    
};
