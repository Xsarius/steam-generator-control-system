function sendSetpoints() {
    var data = {};

    data['temp_setpoint'] = document.getElementById("temp_setpoint").value;

    sendPOST(data ,"/");
}