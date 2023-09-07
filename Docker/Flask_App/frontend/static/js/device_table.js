import { download_action_files_url, action_folder_info_url } from './page_specific_urls.js';


const tbodyElement = document.getElementById("device_list");


function add_device() {
    var input_device_ip = document.getElementById('device_ip').value;

    // Split the IP addresses by a newline or comma
    var device_ip = input_device_ip.split(/\s*[,|\n]\s*/);

    // You can further validate each IP if needed
    device_ip = device_ip.map(function (entry) {
        var match = entry.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
        return match ? match[0] : null;
    }).filter(Boolean);

    device_ip.forEach(element => {
        var deviceInfo = {
            name: element,
            status: "Unknown"
        }
        addRowToFileTable(deviceInfo, tbodyElement);
    });
}
window.add_device = add_device;


function clear_all_devices() {
    tbodyElement.innerHTML = "";
}
window.clear_all_devices = clear_all_devices;


function addRowToFileTable(deviceInfo, tableElement) {
    let newRow = tableElement.insertRow();

    let nameCell = newRow.insertCell(0);
    let statusCell = newRow.insertCell(1);

    nameCell.textContent = deviceInfo.name;
    statusCell.textContent = deviceInfo.status;
}

function get_Devices() {
    return Array.from(tbodyElement.rows).map(row => {
        return {
            name: row.cells[0].textContent,
            status: row.cells[1].textContent
        }
    });
}