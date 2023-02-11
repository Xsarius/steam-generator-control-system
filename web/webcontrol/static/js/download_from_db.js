function downloadFile() {
    $.getJSON("/download/", function (data) {
        var json = JSON.stringify(data);
        var fs = require('fs');

        fs.writeFile('file.json', json, function(err) {
            if (err) throw err;
            console.log('complete');
            });
        });
}