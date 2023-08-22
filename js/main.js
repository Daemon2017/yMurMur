function sendRequest() {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var blob = new Blob([xhr.response], { type: "octet/stream" });
            var fileName = "result.zip";
            saveAs(blob, fileName);
        }
    }
    xhr.responseType = "arraybuffer";

    xhr.open("POST", "https://bbak5ugcncih5o367egr.containers.yandexcloud.net/" + document.getElementById("formatID").value);
    xhr.setRequestHeader("rankdir", document.getElementById("directionID").value);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.send(document.getElementById("textareaID").value);
}