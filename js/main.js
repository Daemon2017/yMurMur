function sendRequest() {
    document.getElementById("errorTextareaID").value = "";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if (xhr.response.byteLength > 256) {
                var blob = new Blob([xhr.response], { type: "octet/stream" });
                var fileName = "result.zip";
                saveAs(blob, fileName);
                document.getElementById("errorTextareaID").value = "Success!";
            } else {
                var error = String.fromCharCode.apply(null, new Uint8Array(this.response));
                document.getElementById("errorTextareaID").value = JSON.parse(error)['error'];
            }
        }
    }
    xhr.responseType = "arraybuffer";

    xhr.open("POST", "https://bbak5ugcncih5o367egr.containers.yandexcloud.net/" + document.getElementById("formatID").value);
    xhr.setRequestHeader("rankdir", document.getElementById("directionID").value);
    xhr.setRequestHeader("ypg", document.getElementById("ypgID").value);
    xhr.setRequestHeader("amr", document.getElementById("amrID").value);
    xhr.setRequestHeader("aa", document.getElementById("aaID").value);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.send(document.getElementById("textareaID").value);
}