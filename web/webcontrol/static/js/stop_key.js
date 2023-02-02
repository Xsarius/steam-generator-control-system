function KeyPress(e) {
    var evtobj = window.event? event : e
    // Emergency stop - ctrl + q
    if (evtobj.keyCode == 81 && evtobj.ctrlKey) curr_vals['emergency_stop'] = 1;
    // Soft stop - ctrl + c
    else if (evtobj.keyCode == 67 && evtobj.ctrlKey) curr_vals['soft_stop'] = 1;

    sendPOST();
}

document.onkeydown = KeyPress;