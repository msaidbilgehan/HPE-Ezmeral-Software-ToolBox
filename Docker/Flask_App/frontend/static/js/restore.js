import { endpoint_action_2_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
import { get_Devices, set_Device_Property } from './device_table.js';
import { add_Element_to_Flex_Container } from './flex_container.js';
import { showNotification } from './notification.js';


function restore_control() {
    let devices = get_Devices();

    devices.forEach(device => {
        let deviceElement = document.getElementById(device.element.id);
        let propertyName = "status";
        let propertyValue = "waiting";
        set_Device_Property(deviceElement, propertyName, propertyValue);
    })

    let ipAddresses = devices.map(device => {
        return {"ip": device.name}
    });
    
    let ipAddressesJson = JSON.stringify(ipAddresses);

    let credentials = get_ssh_credentials();
    let ssh_usernameJson = credentials[0];
    let ssh_passwordJson = credentials[1];

    // Append the IP addresses as a query parameter
    let url = endpoint_action_2_url;
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesJson);

    // Call Endpoint
    fetch(url).then(response => response.json()).then(data => {
        data.message.forEach(item => {
            // let notification = "IP: " + item.ip_address + " | " + "Response: " + item.response + " | " + "Message: " + item.message;
            devices.forEach(device => {
                if (device.name === item.ip_address) {

                    let deviceElement = document.getElementById(device.element.id);
                    let propertyName = "status";

                    let propertyValue;
                    if (item.check === "True") {
                        propertyValue = "completed";
                    } else if (item.check === "False") {
                        propertyValue = "error";
                    } else {
                        console.warn(`Unexpected value for item.check: ${item.check}`);
                    }

                    set_Device_Property(deviceElement, propertyName, propertyValue);
                    add_Element_to_Flex_Container(device.name);
                }
            })
            // showNotification(notification, "info");
        });

        // showNotification(notification, "info");
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
    });
};
window.restore_control = restore_control;

export function get_Backup_Type(){
    let selectedRadio = document.querySelector('input[name="backup_type"]:checked');
    if (selectedRadio) {
        let selectedBackupType = selectedRadio.id;
        return selectedBackupType;
    } else {
        console.error("Backup type should be selected!");
    }
}