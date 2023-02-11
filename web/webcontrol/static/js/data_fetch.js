var json_data = {};

var refresh_interval = 1000; // Miliseconds

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

  document.getElementById("heater_1").textContent = json_data.heater_w1;

  document.getElementById("heater_2").textContent = json_data.heater_w2;

  document.getElementById("heater_3").textContent = json_data.heater_w3;

  document.getElementById("heater_st1").textContent = json_data.heater_st;

  document.getElementById("valve").textContent = json_data.valve;

  document.getElementById("save").textContent = json_data.save;
}

setInterval(reloadData, refresh_interval);
