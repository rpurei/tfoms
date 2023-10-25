function add_lek_pr(sl_pr_id) {
  let current_sl_id = sl_pr_id.split("##")[1];
  var lekpr_elements = document.querySelectorAll("div[id^=" + CSS.escape("LEK_PR%lek%" + current_sl_id + "$lek$") + "]");
  let parent_div;
  if (lekpr_elements.length === 0) {
    document.getElementById(sl_pr_id).value = 1;
    parent_div = document.getElementById("SL###" + current_sl_id);
  } else {
    document.getElementById(sl_pr_id).value = lekpr_elements.length + 1;
    parent_div = document.getElementById("LEK_PR%lek%" + current_sl_id + "$lek$" + lekpr_elements.length);
    //alert("LEK_PR%div%" + current_sl_id + "$div$" + lekpr_elements.length)
  }
  let current_lekpr_count = parseInt(document.getElementById(sl_pr_id).value);
  var lek_pr_div = document.createElement('div');
  lek_pr_div.className = "card";
  lek_pr_div.style = 'margin: 20px;';
  lek_pr_div.innerHTML = `
        <div class="card-body" id="LEK_PR%lek%` + current_sl_id + `$lek$` + current_lekpr_count + `">
        <h5 style="margin-bottom: 20px; margin-top: 20px;">Секция LEK_PR</h5>
            <div class="input-group mb-3">
                <span class="input-group-text">DATA_INJ</span>
                <input type="text" name="LEK_PR%%%` + current_sl_id + `$$$` + current_lekpr_count + `###DATA_INJ" class="form-control" value=""/>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">CODE_SH</span>
                <input type="text" name="LEK_PR%%%` + current_sl_id + `$$$` + current_lekpr_count + `###CODE_SH" class="form-control" value=""/>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">REGNUM</span>
                <input type="text" name="LEK_PR%%%` + current_sl_id + `$$$` + current_lekpr_count + `###REGNUM" class="form-control" value=""/>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">COD_MARK</span>
                <input type="text" name="LEK_PR%%%` + current_sl_id + `$$$` + current_lekpr_count + `###COD_MARK" class="form-control" value=""/>
            </div>
            <input type="hidden" id="LEK_DOSE%%` + current_sl_id + `$$` + current_lekpr_count + `" class="form-control" value="1"/>
            <a class="btn btn-outline-success" href="javascript:void(0);" onclick="add_lek_dose('LEK_PR%%` + current_sl_id + `$$` + current_lekpr_count + `')" role="button" style="margin-top: 20px;"> Добавить LEK_DOSE</a>
        </div>
  `;
  parent_div.appendChild(lek_pr_div);
  current_lekpr_count += 1;
  document.getElementById(sl_pr_id).value = current_lekpr_count;
}

function add_lek_dose(lek_pr_id) {
  let lekpr_array = lek_pr_id.split("%%")[1].split("$$");
  let current_sl_id = lekpr_array[0];
  let current_lekpr_id = lekpr_array[1];
  var lekdose_elements = document.querySelectorAll("div[id^=" + CSS.escape("LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*") + "]");
  let parent_div;
  if (lekdose_elements.length === 0) {
    document.getElementById("LEK_DOSE%%" + current_sl_id + "$$" + current_lekpr_id).value = 1;
    parent_div = document.getElementById("LEK_PR%lek%" + current_sl_id + "$lek$" + current_lekpr_id);
  } else {
    document.getElementById("LEK_DOSE%%" + current_sl_id + "$$" + current_lekpr_id).value = lekdose_elements.length + 1;
    parent_div = document.getElementById("LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*" + lekdose_elements.length);
  }
  let current_lekdose_count = parseInt(document.getElementById("LEK_DOSE%%" + current_sl_id + "$$" + current_lekpr_id).value);
  var lek_dose_div = document.createElement('div');
  lek_dose_div.className = "card";
  lek_dose_div.style = 'margin: 20px;';
  lek_dose_div.innerHTML = `
      <div class="card-body" id="LEK_PR%dose%` + current_sl_id + `$dose$` + current_lekpr_id + `*dose*` + current_lekdose_count +`">
      <h5 style="margin-bottom: 20px; margin-top: 20px;">Секция LEK_DOSE</h5>
          <div class="input-group mb-3">
              <span class="input-group-text">ED_IZM</span>
              <input type="text" name="LEK_DOSE%%%` + current_sl_id + `$$$` + current_lekpr_id + `***` + current_lekdose_count + `###ED_IZM" class="form-control" value=""/>
          </div>
          <div class="input-group mb-3">
              <span class="input-group-text">DOSE_INJ</span>
              <input type="text" name="LEK_DOSE%%%` + current_sl_id + `$$$` + current_lekpr_id + `***` + current_lekdose_count + `###DOSE_INJ" class="form-control" value=""/>
          </div>
          <div class="input-group mb-3">
              <span class="input-group-text">METHOD_INJ</span>
              <input type="text" name="LEK_DOSE%%%` + current_sl_id + `$$$` + current_lekpr_id + `***` + current_lekdose_count + `###METHOD_INJ" class="form-control" value=""/>
          </div>
          <div class="input-group mb-3">
              <span class="input-group-text">COL_INJ</span>
              <input type="text" name="LEK_DOSE%%%` + current_sl_id + `$$$` + current_lekpr_id + `***` + current_lekdose_count + `###COL_INJ" class="form-control" value=""/>
          </div>
      </div> 
   `;
  parent_div.appendChild(lek_dose_div);
  current_lekdose_count += 1;
  document.getElementById("LEK_DOSE%%" + current_sl_id + "$$" + current_lekpr_id).value = current_lekdose_count;
}

function del_lek_pr(lek_pr_id) {
    let id_to_remove = parseInt(lek_pr_id.split("$lek$")[1]);
    let current_sl_id = lek_pr_id.split("LEK_PR%lek%")[1].split("$lek$")[0];
    let lekprs_array = document.querySelectorAll("div[id^=" + CSS.escape("LEK_PR%lek%" + current_sl_id + "$lek$") + "]");
    //console.log('ID ti remove: ' + id_to_remove + ' SL ID: ' + current_sl_id)
    for (let element of lekprs_array) {
        let current_id = parseInt(element.getAttribute('id').split("$lek$")[1]);
        if (current_id === id_to_remove) {
            let child = document.getElementById("LEK_PR%lek%" + current_sl_id + "$lek$" + (id_to_remove).toString());
            child.parentNode.removeChild(child);
        }
        else if (current_id > id_to_remove) {
            document.getElementById("LEK_PR%lek%" + current_sl_id + "$lek$" + current_id).setAttribute("id", "LEK_PR%lek%" + current_sl_id + "$lek$" + (current_id - 1));
            document.getElementsByName("LEK_PR%%%" + current_sl_id + "$$$" + current_id + "###DATA_INJ")[0].setAttribute("name","LEK_PR%%%" + current_sl_id + "$$$" + (current_id - 1) + "###DATA_INJ");
            document.getElementsByName("LEK_PR%%%" + current_sl_id + "$$$" + current_id + "###CODE_SH")[0].setAttribute("name","LEK_PR%%%" + current_sl_id + "$$$" + (current_id - 1) + "###CODE_SH");
            document.getElementsByName("LEK_PR%%%" + current_sl_id + "$$$" + current_id + "###REGNUM")[0].setAttribute("name","LEK_PR%%%" + current_sl_id + "$$$" + (current_id - 1) + "###REGNUM");
            document.getElementsByName("LEK_PR%%%" + current_sl_id + "$$$" + current_id + "###COD_MARK")[0].setAttribute("name","LEK_PR%%%" + current_sl_id + "$$$" + (current_id - 1) + "###COD_MARK");
            let doses_array = document.querySelectorAll("div[id^=" + CSS.escape("LEK_PR%dose%" + current_sl_id + "$dose$" + current_id + "*dose*") + "]");
             for (let elem of doses_array) {
                 let curr_dose_id = parseInt(element.getAttribute('id').split("*dose*")[1]);
                 document.getElementById("LEK_PR%dose%" + current_sl_id + "$dose$" + current_id + "*dose*" + curr_dose_id).setAttribute("id", "LEK_PR%dose%" + current_sl_id + "$dose$" + current_id + "*dose*" + (curr_dose_id - 1));
                 document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + curr_dose_id + "###ED_IZM")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + (curr_dose_id - 1) + "###ED_IZM");
                 document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + curr_dose_id + "###DOSE_INJ")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + (curr_dose_id - 1) + "###DOSE_INJ");
                 document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + curr_dose_id + "###METHOD_INJ")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + (curr_dose_id - 1) + "###METHOD_INJ");
                 document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + curr_dose_id + "###COL_INJ")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_id + "***" + (curr_dose_id - 1) + "###COL_INJ");
             }
        }
    }
}

function del_lek_dose(lek_dose_id) {
    let id_to_remove = parseInt(lek_dose_id.split("*dose*")[1]);
    let current_sl_id = lek_dose_id.split("LEK_PR%dose%")[1].split("$dose$")[0];
    let current_lekpr_id = lek_dose_id.split("$dose$")[1].split("*dose*")[0];
    let doses_array = document.querySelectorAll("div[id^=" + CSS.escape("LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*") + "]");
    for (let element of doses_array) {
        let current_id = parseInt(element.getAttribute('id').split("*dose*")[1]);
        if (current_id === id_to_remove) {
            //console.log("LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*" + id_to_remove.toString());
            let child = document.getElementById("LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*" + (id_to_remove).toString());
            child.parentNode.removeChild(child);
        }
        else if (current_id > id_to_remove) {
            document.getElementById("LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*" + current_id).setAttribute("id", "LEK_PR%dose%" + current_sl_id + "$dose$" + current_lekpr_id + "*dose*" + (current_id - 1));
            document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + current_id + "###ED_IZM")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + (current_id - 1) + "###ED_IZM");
            document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + current_id + "###DOSE_INJ")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + (current_id - 1) + "###DOSE_INJ");
            document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + current_id + "###METHOD_INJ")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + (current_id - 1) + "###METHOD_INJ");
            document.getElementsByName("LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + current_id + "###COL_INJ")[0].setAttribute("name","LEK_DOSE%%%" + current_sl_id + "$$$" + current_lekpr_id + "***" + (current_id - 1) + "###COL_INJ");
        }
    }
}