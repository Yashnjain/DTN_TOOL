var set1 = new Set();
var set_size = 0;

function setField(event) {
    var input1 = document.getElementById(event.id);
    if (input1.value === "0" || input1.value == "0.0") {
        input1.value = "";
    } else {
        input1.selectionStart = input1.selectionEnd = input1.value.length;
    }
}

function checkOver(event) {
    var id1 = event.id;
    var num = id1.match(/\d+/)[0]
    var icon1 = "iconW" + num;
    var field = document.getElementById(id1);
    if (field.value >= 0.05 || field.value <= -0.05) {
        field.classList.add("warn");
    } else {
        field.classList.remove("warn");
    }
    if (field.value == "") {
        field.value = "0.0";
    }
}
function checkover2(id1) {
    // var id1 = event.id;
    // console.log(event)
    var field = document.getElementById(id1);
    // console.log(field);
    if (field.value === "") {
        field.value = "0.0";
    }
    if (field.value !== "0.0" && field.value !== "0") {
        field.classList.add("cust-val");
    } else {
        field.classList.remove("cust-val");
    }
}

function AutoCalc(event) {

    var id1 = event.id;
    var num = id1.match(/\d+/)[0]
    var prev = "prev" + num;
    var curr = "curr" + num;

    var c;
    var a = document.getElementById(event.id);
    var b = document.getElementById(prev);
    var m = document.getElementById(curr);
    var temp = b.getAttribute("data");
    var temp_diff = a.getAttribute("data");
    var check1 = temp_diff + ".0"
    a.onkeyup = function () {
        if (!isNaN(a.value)) {
            var add1 = parseFloat(a.value || 0)
            var result = parseFloat(a.value || 0) + parseFloat(temp || 0);
            if (result >= 0) {
                m.innerText = result.toFixed(4);
                m.innerText = m.innerText.replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.0*$/, '');
            } else {
                a.value = 0.0;
                m.innerText = parseFloat(temp);
                alert("Please enter a Valid Value");
            }
        }
    }
}

document.addEventListener('keydown', function (event) {
    var element = event.target;
    var tagName = element.tagName.toLowerCase();

    if (event.keyCode === 9 && tagName === 'input' && element.classList.contains('moveFocusDown')) {
        var table = document.getElementById("myTable");
        var rowNum = element.parentNode.parentNode.rowIndex;
        var colNum = element.parentNode.cellIndex;
        var nextRow = table.rows[rowNum + 1];
        if (nextRow) {
            var nextInput = nextRow.cells[colNum].querySelector('input');
            if (nextInput) {
                event.preventDefault();
                nextInput.focus();
                nextInput.click();
            }
        }
    }
});

function isEnable(event) {

    var a = event.id;
    var num = a.match(/\d+/)[0]
    var cstinput = "P" + num;
    var drp = "DRP_btn" + num;

    var checkbox = document.getElementById(a);
    var input = document.getElementById(cstinput);
    var drp_inp = document.getElementById(drp);
    checkbox.addEventListener("change", function () {
        if (this.checked) {
            input.removeAttribute("disabled");
            drp_inp.removeAttribute("disabled");
        } else {
            input.setAttribute("disabled", "disabled");
            drp_inp.setAttribute("disabled", "disabled");
        }
    });
}

const custfield = document.querySelectorAll('.cust-inp');
custfield.forEach(element => {
  if (element.value !== "0.0" && element.value !== "0") {
    const id_temp = element.id; // get the id attribute of the current element
    checkover2(id_temp);
    console.log(id_temp);
  }
});

const inputFields = document.querySelectorAll('input');

var regex = /^(?!C)\w+$/;
inputFields.forEach(input => {
    input.addEventListener('change', () => {
        // console.log(`Input field with id ${input.id} was clicked`);
        if (input.id && regex.test(input.id)) {
            set1.add(input.id);
        }
        var newValue = input.value || "0.0";
        input.value = newValue;
    });
});


function updateSetSize() {

    set_size = set1.size;

    var loader1 = document.querySelector(".loader");
    loader1.style.display = "flex";
    loader1.classList.remove("loader--hidden");
}

// Javascript for custom step function
function increaseValue(num) {

    var cstinput2 = "P" + num;
    inputField = document.getElementById(cstinput2);

    if (!(inputField.disabled)) {
        var value = parseFloat(document.getElementById(cstinput2).value);
        value = isNaN(value) ? 0 : value;
        value = value + parseFloat(0.0025);

        value = value.toFixed(4);
        value = value.replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.0*$/, '');
        document.getElementById(cstinput2).value = value;
        checkover2(cstinput2)
    }
}

function decreaseValue(num) {

    var cstinput1 = "P" + num;
    inputField = document.getElementById(cstinput1);
    if (!(inputField.disabled)) {
        var value = parseFloat(document.getElementById(cstinput1).value);
        value = isNaN(value) ? 0 : value;
        value = value - parseFloat(0.0025);

        value = value.toFixed(4);
        value = value.replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.0*$/, '');
        document.getElementById(cstinput1).value = value;
        checkover2(cstinput1)
    }
}


//function to prevent digits after 4 places of decimal point
function checkDecimal(input) {
    var value = input.value;
    // var regex = /^-?\d+(\.\d{0,4})?$/; // regex to match up to 4 decimal places
    var regex = /^-?\d*(\.\d{0,4})?$/; // updated ragex for minus
    if (!regex.test(value)) {
        input.value = value.slice(0, -1); // remove the last character if it's invalid
    }
}

function logoutFun() {
    document.getElementById("signout").submit();
}



var form10 = document.querySelector('#uploadForm');
var button10 = form10.querySelector('input[value="Upload"]');

form10.addEventListener('submit', function () {

    var loader1 = document.querySelector(".loader");
    loader1.style.display = "flex";
    loader1.classList.remove("loader--hidden");
    button10.disabled = true;
});

function setCustV(event) {

    var id1 = event.id;
    var num = id1.match(/\d+/)[0]
    var cust_inp = "P" + num;
    var todiff = event.getAttribute("data_val");
    var val1 = parseFloat(event.value);

    var result1 = parseFloat(val1) - parseFloat(todiff);

    var cust = document.getElementById(cust_inp);
    var drp_inp = document.getElementById(event.id);
    if (parseFloat(val1) < parseFloat(0)) {
        alert("Please enter a Valid Value");
        drp_inp.value = todiff;
    }
    // else if (todiff != val1) {
    //     cust.value = result1.toFixed(4);
    // }

}
function checkSet(e) {
    e.preventDefault();
    var cust_form = e.target.parentNode;
    if (set1.size == set_size) {
        showSpin();
        cust_form.submit();

    } else {
        showConfirmation(cust_form);
    }
}
function checkSet2(event, form) {
    event.preventDefault(); // prevent the default form submission
    const url = form.action;
    const params = new URLSearchParams(new FormData(form)).toString();
    const newTab = window.open();
    newTab.location.href = url + "?" + params; // set the URL of the new tab to the form submission result
  }

function showSpin() {

    var loader1 = document.querySelector(".loader");
    loader1.style.display = "flex";
    loader1.classList.remove("loader--hidden");
}
function hideSpin() {
    var loader1 = document.querySelector(".loader");
    loader1.classList.add("loader--hidden");
    loader1.style.display = "none";
}

function showConfirmation(form2) {
    var result = window.confirm("Changes may not be saved?");
    if (result == true) {
        showSpin();
        form2.submit();
    } else {
        // Perform the action if the user selects "Cancel"
        hideSpin();
    }
}

function closeDRP(event) {
    var num = event.id.match(/\d+/)[0];
    var drp_B = "DRP_B" + num;
    var drp_M = "DRP_M" + num;
    dropdown = document.getElementById(drp_B)
    dropdown_menu = document.getElementById(drp_M)
    dropdown.classList.remove("show");
    dropdown_menu.classList.remove("show");
}
function disableTab(e) {
    var readOnly = e.target.readOnly;
    if (e.key === 'Tab' && readOnly) {
        e.preventDefault();
        return false;
    }
}


$(document).ready(function () {
    $("input[type=number]").on("focus", function () {
        $(this).on("keydown", function (event) {
            if (event.keyCode === 38 || event.keyCode === 40) {
                event.preventDefault();
            }
        });
    });

});

function generateDRP(event) {
    // console.log(event);
    // console.log(event.id);
    var DRPbtn = document.getElementById(event.id);
    var ctpm = DRPbtn.getAttribute("data_for_id");

    var DRP_Mid = "DRP_M" + ctpm;
    var drp_id = "DRP_INP" + ctpm;
    var btn_id = "DRP_cl" + ctpm;

    var divM = document.getElementById(DRP_Mid);
    var make_form = DRPbtn.getAttribute("data_for_form");

    const dropdownMenuHtml = generateDropdownMenuHtml(event);
    // console.log(dropdownMenuHtml);

    if(make_form == "1")
    {
        divM.innerHTML = dropdownMenuHtml;

    }
}

function generateDropdownMenuHtml(event) {

    var DRPbtn = document.getElementById(event.id);
    var curr_id = DRPbtn.getAttribute("data-curr");
    var curr = document.getElementById(curr_id);

    var ctpm = DRPbtn.getAttribute("data_for_id");
    var drp = DRPbtn.getAttribute("data_drp");
    // var new_price = DRPbtn.getAttribute("data_c");
    // var yesterday_price = DRPbtn.getAttribute("data_p");

    // var valText = curr.innerText
    var valText = drp;

    var make_form = DRPbtn.getAttribute("data_for_form");
    if(make_form == "1")
    {
    // console.log("generating form");
    var DRP_Mid = "DRP" + ctpm;
    var drp_id = "DRP_INP" + ctpm;
    var btn_id = "DRP_cl" + ctpm;
    var divM = document.getElementById(DRP_Mid);

    const form = document.createElement('form');
    const divFormGroup = document.createElement('div');
    divFormGroup.style.padding = "2px";
    divFormGroup.classList.add('form-group');

    const label = document.createElement('label');
    label.classList.add('form-label');
    label.setAttribute('for', 'fm1');
    label.style.marginLeft = "2px";
    label.textContent = 'Update Base Price';
    divFormGroup.appendChild(label);

    const divInput = document.createElement('div');

    const input = document.createElement('input');
    input.classList.add('form-control');
    input.setAttribute('id', `DRP_INP${ctpm}`);
    input.setAttribute('type', 'text');
    input.setAttribute('placeholder', 'Update Base Price');
    input.setAttribute('value', valText);
    input.setAttribute('data_val', valText);
    input.setAttribute('required', 'true');
    input.setAttribute('name', `SP${ctpm}`);
    input.style.marginRight = "2px";
    input.style.height = "30px";
    input.setAttribute('onblur', 'setCustV(this);');
    input.setAttribute('oninput', 'checkDecimal(this);');
    divInput.appendChild(input);

    divFormGroup.appendChild(divInput);
    
    const inputButton = document.createElement('input');
    inputButton.setAttribute('type', 'button');
    inputButton.classList.add('btn', 'btn-primary', 'cust-btn');
    inputButton.setAttribute('id', `DRP_cl${ctpm}`);
    inputButton.setAttribute('value', 'Save');
    inputButton.style.marginTop = "0.4em";
    inputButton.style.height = "25px";
    inputButton.style.fontSize = "15px";
    inputButton.style.marginLeft = "0px";
    inputButton.setAttribute('onclick', 'closeDRP(this);');
    DRPbtn.setAttribute("data_in_curr", curr.innerText);
    DRPbtn.setAttribute('data_for_form', "0");
    // inputButton.addEventListener('click', function () {
    //     closeDRP(this);
    // });


    divFormGroup.appendChild(inputButton);
    form.appendChild(divFormGroup);
    // div.appendChild(form);
    return form.outerHTML;
    }
    else{
        data_to_compare = DRPbtn.getAttribute("data_in_curr");
        // console.log(data_to_compare);
        // console.log(curr.innerText);
        // console.log("Inside else");
        if (data_to_compare != curr.innerText) {
            // console.log("new part");
            // console.log(ctpm);
            var inp_id= "DRP_INP"+ctpm;
            input1 = document.getElementById(inp_id);
            // console.log(input1);	
            input1.value = curr.innerText;
            DRPbtn.setAttribute("data_in_curr", curr.innerText);
        }
    }
}


