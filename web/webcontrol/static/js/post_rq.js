var curr_vals = {
    heater_w1: 0,
    heater_w2: 0,
    heater_w3: 0,
    heater_st: 0,
    valve: 0,
    save: 0,
    emergency_stop: 0,
    soft_stop: 0,
    manual_mode: 0,
};

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  function keySendPOST(elementname){
    curr_vals[elementname] = 1 - curr_vals[elementname];
    curr_vals['manual_mode'] = 1;
    sendPOST(curr_vals,"/");
    curr_vals['manual_mode'] = 0;
  }

  function sendPOST(data, url) {
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"), // don't forget to include the 'getCookie' function
      },
    });
  }
  