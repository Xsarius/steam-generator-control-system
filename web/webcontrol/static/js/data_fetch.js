var json_data = {};

var refresh_interval = 200; // Miliseconds

function reloadData() {
  $.getJSON("/update_data/", function (data) {
    json_data = data;
  });

  console.log(json_data);

  document.getElementById("curr_temp_set").textContent =
    json_data["curr_temp_set"];

  document.getElementById("water_temp").textContent = json_data["water_temp"];
  document.getElementById("steam_temp_1").textContent =
    json_data["steam_temp_1"];
  document.getElementById("steam_temp_2").textContent =
    json_data["steam_temp_2"];
  document.getElementById("pressure").textContent = json_data["pressure"];
  // Phase 1
  document.getElementById("voltage_ph1").textContent = json_data["voltage_ph1"];
  document.getElementById("current_ph1").textContent = json_data["current_ph1"];
  document.getElementById("active_power_ph1").textContent =
    json_data["active_power_ph1"];
  // Phase 2
  document.getElementById("voltage_ph2").textContent = json_data["voltage_ph2"];
  document.getElementById("current_ph2").textContent = json_data["current_ph2"];
  document.getElementById("active_power_ph2").textContent =
    json_data["active_power_ph2"];
  //Phase 3
  document.getElementById("voltage_ph3").textContent = json_data["voltage_ph3"];
  document.getElementById("current_ph3").textContent = json_data["current_ph3"];
  document.getElementById("active_power_ph3").textContent =
    json_data["active_power_ph3"];

  var temp = "OFF";
  if (json_data["heater_w1"][0]) {
    temp = "ON";
  }
  document.getElementById("heater_1").textContent = temp;

  temp = "OFF";
  if (json_data["heater_w2"][0]) {
    temp = "ON";
  }
  document.getElementById("heater_2").textContent = temp;

  temp = "OFF";
  if (json_data["heater_w3"][0]) {
    temp = "ON";
  }
  document.getElementById("heater_3").textContent = temp;

  temp = "OFF";
  if (json_data["heater_st"][0]) {
    temp = "ON";
  }
  document.getElementById("heater_st1").textContent = temp;

  temp = "CLOSED";
  if (json_data["valve"][0]) {
    temp = "OPEN";
  }
  document.getElementById("valve").textContent = temp;

  temp = "INACTIVE";
  if (json_data["save"][0]) {
    temp = "ACTIVE";
  }
  document.getElementById("save").textContent = temp;
}

setInterval(reloadData, refresh_interval);
