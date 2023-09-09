import { download_action_files_url, action_folder_info_url } from './page_specific_urls.js';


const deviceListElement = document.getElementById("device_list");


function add_device() {
    var input_device_ip = document.getElementById('device_ip').value;

    // Split the IP addresses by a newline or comma
    var device_ip = input_device_ip.split(/\s*[,|\n| ]\s*/);

    // You can further validate each IP if needed
    device_ip = device_ip.map(function (entry) {
        var match = entry.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
        return match ? match[0] : null;
    }).filter(Boolean);

    device_ip.forEach(element => {
        if (!document.getElementById("device_" + element)) {
            var deviceInfo = {
                id: "device_" + element,
                name: element,
                status: "start"
            }
            addDeviceToDeviceList(deviceInfo);
        }
    });
}
window.add_device = add_device;


function clear_all_devices() {
    // 'device_list' ID'sine sahip ana div elementini al
    let deviceListElement = document.getElementById('device_list');

    // Bu div'in içindeki 'device_x.x.x.x' pattern'ine uyan cihaz elementlerini al
    let deviceElements = deviceListElement.querySelectorAll('div[id^="device_"]');

    // Bu cihaz elementlerini tek tek sil
    deviceElements.forEach(deviceElement => {
        deviceElement.remove();
    });
}
window.clear_all_devices = clear_all_devices;


function addDeviceToDeviceList(deviceInfo) {
    let newIcon = document.createElement("i");
    newIcon.className = "fa fa-trash fa-lg";

    let newButton = document.createElement("button");
    newButton.className = "btn btn-sm";
    newButton.appendChild(newIcon);
    newButton.setAttribute("id", deviceInfo.id)
    newButton.addEventListener('click', removeDevice);

    let newDiv = document.createElement("div");
    newDiv.setAttribute("class", "d-flex align-items-center border-bottom p-2")
    newDiv.setAttribute("id", deviceInfo.id)
    newDiv.appendChild(newButton);
    
    let newDiv2 = document.createElement("div");
    newDiv2.className = "w-100 m-1 pe-3";
    
    let newDiv3 = document.createElement("div");
    newDiv3.className = "d-flex w-100 align-items-center justify-content-around";
    
    let newSpan = document.createElement("span");
    newSpan.textContent = deviceInfo.name;
    
    let newIcon2 = document.createElement("i");
    if (deviceInfo.status === "start") {
        newIcon2.className = "fa fa-play fa-2x fa-fw margin-bottom color-green";
    } else if (deviceInfo.status === "waiting") {
        newIcon2.className = "fa fa-spinner fa-pulse fa-2x fa-fw margin-bottom color-yellow";
    } else if (deviceInfo.status === "completed") {
        newIcon2.className = "fa fa-check-circle fa-2x fa-fw margin-bottom color-green";
    } else if (deviceInfo.status === "error") {
        newIcon2.className = "fa fa-exclamation-triangle fa-2x fa-fw margin-bottom color-red";
    }

    newDiv3.appendChild(newSpan);
    newDiv3.appendChild(newIcon2);
    newDiv2.appendChild(newDiv3);
    newDiv.appendChild(newDiv2);
    deviceListElement.appendChild(newDiv);

}

export function get_Devices() {
    // 'device_list' ID'sine sahip ana div elementini al
    let deviceListElement = document.getElementById('device_list');

    // Bu div'in içindeki her bir cihazı temsil eden div elementlerini al
    let deviceDivs = Array.from(deviceListElement.querySelectorAll('div.d-flex.align-items-center.border-bottom.p-2'));

    return deviceDivs.map(deviceDiv => {
        // Her bir cihaz div'inin id'sini al (bu id cihazın IP adresini temsil ediyor)
        let deviceIP = deviceDiv.textContent;
        // Cihaz durumunu temsil eden ikonları kontrol et
        let spinnerIcon = deviceDiv.querySelector('i.fa-spinner');
        let checkCircleIcon = deviceDiv.querySelector('i.fa-check-circle');
        let exclamationTriangleIcon = deviceDiv.querySelector('i.fa-exclamation-triangle');

        let status;
        if (spinnerIcon) {
            status = 'waiting';
        } else if (checkCircleIcon) {
            status = 'completed';
        } else if (exclamationTriangleIcon) {
            status = 'error';
        } else {
            status = 'unknown';
        }

        return {
            name: deviceIP,
            status: status,
            element: deviceDiv
        };
    });
}

function __removeDevice(event) {
    // 'device_list' ID'sine sahip ana div elementini al
    let deviceListElement = document.getElementById('device_list');

    // Bu div'in içindeki 'device_x.x.x.x' pattern'ine uyan cihaz elementlerini al
    let deviceElements = deviceListElement.querySelectorAll('div[id^="device_"]');

    // Bu cihaz elementlerini tek tek sil
    deviceElements.forEach(deviceElement => {
        deviceElement.remove();
    });
}
function removeDevice(event) {
    // Tıklanan elementi (çöp ikonunu veya butonunu) al
    let targetElement = event.target;
    // console.log(targetElement.parentElement.id);
    // console.log(targetElement.parentElement.parentElement.id);
    let buttonElement = targetElement.parentElement;
    let targetID = buttonElement.id;
    let parentDivElement = buttonElement.parentElement;
    if (buttonElement.id.startsWith('device_') && parentDivElement.id.startsWith(targetID)) {
        parentDivElement.remove();
    }

    // Tıklanan elementin en üstteki ebeveyn elementini bul (bu durumda 'device_x.x.x.x' ID'li <div> elementi)
    // while (targetElement && !targetElement.id.startsWith('device_')) {
    //     targetElement = targetElement.parentElement;
    // }

    // Ebeveyn elementi sil
    // if (targetElement && targetElement.id.startsWith('device_')) {
    //     targetElement.remove();
    // }
}



// Tüm çöp ikonlarına 'click' event listener'ı ekleyin
// document.querySelectorAll('i.fa-trash').forEach(icon => {
//     icon.addEventListener('click', removeDevice);
// });

