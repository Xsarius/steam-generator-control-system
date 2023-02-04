var curr_vals = {
  heater_w1: 0,
  heater_w2: 0,
  heater_w3: 0,
  heater_st: 0,
  valve: 0,
  save: 0,
  emergency_stop: 0,
  soft_stop: 0,
};

var json_data = {};

var refresh_interval = 200 // Miliseconds

function reloadData() {
  $.getJSON("/update_data/", function (data) {
    json_data = data;
  });

  console.log(json_data);

  document.getElementById("water_temp").textContent = json_data["water_temp"];
  document.getElementById("steam_temp_1").textContent =
    json_data["steam_temp_1"];
  document.getElementById("steam_temp_2").textContent =
    json_data["steam_temp_2"];
  document.getElementById("ps_temp").textContent = json_data["ps_temp"];
  document.getElementById("pressure").textContent = json_data["pressure"];

  let temp = "OFF";

  if (json_data["heater_1"]) {
    temp = "ON";
  }
  document.getElementById("heater_1").textContent = temp;

  temp = "OFF";

  if (json_data["heater_2"]) {
    temp = "ON";
  }
  document.getElementById("heater_2").textContent = temp;

  temp = "OFF";

  if (json_data["heater_3"]) {
    temp = "ON";
  }
  document.getElementById("heater_3").textContent = temp;

  temp = "OFF";

  if (json_data["heater_st"]) {
    temp = "ON";
  }
  document.getElementById("heater_st1").textContent = temp;

  temp = "CLOSED";

  if (json_data["valve"]) {
    temp = "OPEN";
  }

  document.getElementById("valve").textContent = temp;

  temp = "INACTIVE"

  if(json_data["save"]){
    temp = "ACTIVE"
  }

  document.getElementById("save").textContent = temp;
}

setInterval(reloadData, refresh_interval);

window.onload = function () {
  var dps1 = [];
  var dps2 = [];
  var dps3 = [];
  var chart1 = new CanvasJS.Chart("chartContainer1", {
    title: {
      text: "Water tempearature",
    },
    data: [
      {
        type: "line",
        dataPoints: dps1,
      },
    ],
  });

  var chart2 = new CanvasJS.Chart("chartContainer2", {
    title: {
      text: "Steam tempearature",
    },
    data: [
      {
        type: "line",
        dataPoints: dps2,
      },
    ],
  });

  var chart3 = new CanvasJS.Chart("chartContainer3", {
    title: {
      text: "Pressure",
    },
    data: [
      {
        type: "line",
        dataPoints: dps3,
      },
    ],
  });

  var updateInterval = 1000;
  var dataLength = 1;

  var xVal1 = 0;
  var yVal1 = 0;
  var updateChart1 = function (count) {
    count = count || 1;

    for (var j = 0; j < count; j++) {
      yVal1 = parseFloat(json_data["water_temp"]);
      dps1.push({
        x: xVal1,
        y: yVal1,
      });
      xVal1++;
    }

    // if (dps1.length > dataLength) {
    //     dps1.shift();
    // }

    chart1.render();
  };

  var xVal2 = 0;
  var yVal2 = 0;
  var updateChart2 = function (count) {
    count = count || 1;

    for (var j = 0; j < count; j++) {
      yVal2 =
        (parseFloat(json_data["steam_temp_1"]) +
          parseFloat(json_data["steam_temp_2"])) /
        2;
      dps2.push({
        x: xVal2,
        y: yVal2,
      });
      xVal2++;
    }

    // if (dps2.length > dataLength) {
    //     dps2.shift();
    // }

    chart2.render();
  };

  var xVal3 = 0;
  var yVal3 = 0;
  var updateChart3 = function (count) {
    count = count || 1;

    for (var j = 0; j < count; j++) {
      yVal3 = parseFloat(json_data["pressure"]);
      dps3.push({
        x: xVal3,
        y: yVal3,
      });
      xVal3++;
    }

    // if (dps3.length > dataLength) {
    //     dps3.shift();
    // }

    chart3.render();
  };

  updateChart1(dataLength);
  updateChart2(dataLength);
  updateChart3(dataLength);
  setInterval(updateChart1, updateInterval);
  setInterval(updateChart2, updateInterval);
  setInterval(updateChart3, updateInterval);
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
  sendPOST(curr_vals, "/");
}

function sendPOST(post_data_vals, url) {
  $.ajax({
    type: "POST",
    url: url,
    data: post_data_vals,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"), // don't forget to include the 'getCookie' function
    },
  });
}
