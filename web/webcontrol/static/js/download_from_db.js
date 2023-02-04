function downloadFile() {
    var download_vals = {
        file_name: "test_file"
    };
    sendPOST(download_vals, "/download/");
}