const tbodyElement = document.getElementById("file_list");

fetch("/folder_info/log_collection_collected").then(response => response.json()).then(data => {

    data.forEach(file => {
        var fileInfo = {
            creationDate: file.creation_date,
            name: file.name,
            size: file.size + " GB",
        };
        addRowToFileTable(fileInfo, tbodyElement);

        if (file && file.message) {
            showNotification(file.message, "warning");
        }
    });

    // showNotification("Files added successfully", "info");

}).catch(error => {
    console.error(error);
    showNotification(error, "error");
});

function addRowToFileTable(fileInfo, tableElement) {
    let newRow = tableElement.insertRow();

    let creationDateCell = newRow.insertCell(0);
    let nameCell = newRow.insertCell(1);
    let sizeCell = newRow.insertCell(2);

    creationDateCell.textContent = fileInfo.creationDate;
    nameCell.textContent = fileInfo.name;
    sizeCell.textContent = fileInfo.size;
}

$(document).ready(function () {
    $("#file_list").on("click", "tr", function () {
        let foldername = $(this).find("td:nth-child(2)").text();
        window.location.href = `/file_table_download/${foldername}`;
    });
});