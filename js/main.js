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

    xhr.open("POST", "https://bbak5ugcncih5o367egr.containers.yandexcloud.net/" + document.getElementById("outputFormatID").value);
    xhr.setRequestHeader("TreeDirection", document.getElementById("treeDirectionID").value);
    xhr.setRequestHeader("YearsPerGeneration", document.getElementById("yearsPerGenerationID").value);
    xhr.setRequestHeader("AverageMutationRate", document.getElementById("averageMutationRateID").value);
    xhr.setRequestHeader("AverageAge", document.getElementById("averageAgeID").value);
    xhr.setRequestHeader("ImproveAppearance", document.getElementById("improveAppearanceID").value);
    xhr.setRequestHeader("InputFormat", document.getElementById("inputFormatID").value);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.send(document.getElementById("textareaID").value);
}