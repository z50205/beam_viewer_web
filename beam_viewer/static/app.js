// async function getJoke(){
//     // let data=await fetch("https://v2.jokeapi.dev/joke/Any");
//     // let parsedData=await data.json();
//     // console.log(parsedData);
//     // .then((d)=>{
//     //     console.log(d);
//     // })
//     // .catch((e)=>{
//     //     console.log(e);
//     // })
// }

async function readFile() {
    var htmlCheck = document.getElementsByName("Checkhtml");
    const fileUploader = document.getElementById("files");
    fileUploader.addEventListener('change', event => {
        const reader = new FileReader();
        reader.readAsText(event.target.files[0]);
        reader.onload = function (Res) {
            // htmlCheck[0].innerHTML=Res.target.result;
            sr = Res.target.result;
            cantilever = getCantilever(sr);
            var cantilever_checkbox = document.getElementsByName("3")[0];
            if (cantilever_checkbox.checked) 
            {
                var nodeCheckbox = document.getElementsByName("nodeCheckbox")[0];
                nodeCheckbox.innerHTML = "";
                checkboxMake(cantilever);
            }
            // var the_checkbox = document.getElementsByName("3");
            // checkboxMake(cantilever);
        }

        // var reader = new FileReader();
        // reader.onload = function () {
        //     var file = event.target.files;
        //     console.log(file);
        // for (var line = 0; line < file.length - 1; line++) {
        //     console.log(file[line]);
        // }
        // };
    });
    return cantilever;
}

function getCantilever(sr) {
    const srs = sr.split("\n");
    const cantileverName = [];
    for (var i = 0; i < srs.length; i++) {
        if (srs[i].substr(0, 4) == "BEAM") {
            var namebracket = srs[i].indexOf(")");
            if (srs[i].substr(namebracket + 1, 1) == "C")
                cantileverName.push(srs[i].substr(5, 20));
        }

    }
    return cantileverName;
}
function checkboxMake(cantileverName) {
    var t = document.createElement("TABLE");
    t.setAttribute("class","table table-striped table-bordered")
    var newColumn = t.insertRow(0);
    newColumn.setAttribute("class","align-top")
    var nodeCheckbox = document.getElementsByName("nodeCheckbox");
    nodeCheckbox[0].appendChild(t);
    const allHead=[];
    for (var i = 0; i < cantileverName.length; i++) {
        namebracket = cantileverName[i].indexOf(")");
        head=cantileverName[i].substr(namebracket + 1,20);
        head=head.padEnd(30,' ');
        headChecker(head,allHead,newColumn);
        var beamname = document.createElement("label");
        beamname.innerHTML = cantileverName[i];
        beamname.setAttribute("name", cantileverName[i]);
        var lCheckbox = document.createElement("input");
        lCheckbox.setAttribute("type", "radio");
        lCheckbox.setAttribute("name", cantileverName[i]);
        lCheckbox.setAttribute("value", "left");
        lCheckbox.setAttribute("class", head);
        var rCheckbox = document.createElement("input");
        rCheckbox.setAttribute("type", "radio");
        rCheckbox.setAttribute("name", cantileverName[i]);
        rCheckbox.setAttribute("value", "right");
        rCheckbox.setAttribute("class", head);
        t.getElementsByTagName("td")[allHead.indexOf(head)].appendChild(beamname);
        t.getElementsByTagName("td")[allHead.indexOf(head)].appendChild(lCheckbox);
        t.getElementsByTagName("td")[allHead.indexOf(head)].appendChild(rCheckbox);
        var nextRow = document.createElement("br");
        t.getElementsByTagName("td")[allHead.indexOf(head)].appendChild(nextRow);
    }
    var header = t.createTHead();
    var headerRow = header.insertRow(0);
    for(var i = 0; i < allHead.length; i++) {
        newHead=headerRow.insertCell(i);
        newHead.innerHTML = allHead[i];
        var lCheckbox = document.createElement("input");
        lCheckbox.setAttribute("type", "radio");
        lCheckbox.setAttribute("name", allHead[i]);
        lCheckbox.setAttribute("value", "left");
        lCheckbox.setAttribute("class", "beamName");
        var rCheckbox = document.createElement("input");
        rCheckbox.setAttribute("type", "radio");
        rCheckbox.setAttribute("name", allHead[i]);
        rCheckbox.setAttribute("value", "right");
        rCheckbox.setAttribute("class", "beamName");
        newHead.appendChild(lCheckbox);
        newHead.appendChild(rCheckbox);
    }
    addlistener();
  }

function addlistener() {
    var allBeamname = document.getElementsByClassName("beamName");
    for(var i = 0; i < allBeamname.length; i++)
    {
        allBeamname[i].addEventListener('click',function(e){
            e.stopPropagation;
            changeState(this);

        })
    }
  }
function changeState(a){
    var allBeam = document.getElementsByClassName(a.name);
    for (var ii = 0; ii < allBeam.length; ii++)
        if(allBeam[ii].value==a.value)
        allBeam[ii].checked=true;
}
  
function headChecker(head,allHead,row) {
    if (allHead.indexOf(head)==-1)
    {
        allHead.push(head);
        console.log(allHead.length-1);
        var newColumn=row.insertCell(-1);
        newColumn.setAttribute("class","align-top")
    }
  }

// function checkboxMake(cantileverName) {
//     var nodeCheckbox = document.getElementsByName("nodeCheckbox");
//     for (var i = 0; i < cantileverName.length; i++) {
//         var beamname = document.createElement("label");
//         beamname.innerHTML = cantileverName[i];
//         beamname.setAttribute("name", cantileverName[i]);
//         var lCheckbox = document.createElement("input");
//         lCheckbox.setAttribute("type", "radio");
//         lCheckbox.setAttribute("name", cantileverName[i]);
//         lCheckbox.setAttribute("value", "left");
//         var rCheckbox = document.createElement("input");
//         rCheckbox.setAttribute("type", "radio");
//         rCheckbox.setAttribute("name", cantileverName[i]);
//         rCheckbox.setAttribute("value", "right");
//         nodeCheckbox[0].appendChild(beamname);
//         nodeCheckbox[0].appendChild(lCheckbox);
//         nodeCheckbox[0].appendChild(rCheckbox);
//     }
//     console.log(document.getElementsByName("nodeCheckbox")[0].innerHTML)
//   }

var cantilever = readFile();
var cantilever_checkbox = document.getElementsByName("3")[0];
cantilever_checkbox.addEventListener('change', () => {
    if (cantilever && cantilever_checkbox.checked)
        checkboxMake(cantilever);
    else {
        var nodeCheckbox = document.getElementsByName("nodeCheckbox")[0];
        nodeCheckbox.innerHTML = "";
    }
});

// getJoke();