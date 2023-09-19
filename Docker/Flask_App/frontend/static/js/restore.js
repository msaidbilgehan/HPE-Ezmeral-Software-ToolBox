import { endpoint_action_2_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
import { get_ip_host_addresses } from './ip_hostname_table.js';
import { flex_Element_Add_Device, flex_Element_Update_Device, flex_Element_Clear_Devices } from './flex_container.js';
import { showNotification } from './notification.js';
import { button_disable_by_element } from './tools.js';



function restore_control(button = null) {
    button_disable_by_element(button, true);
    
    flex_Element_Clear_Devices();
    let device_ip_addresses = get_ip_host_addresses(true);
    let device_elements = flex_Element_Add_Device(device_ip_addresses.map(device => device.ip));
    
    let ipAddressesJson = JSON.stringify(
        device_ip_addresses.map(device => {
            return { "ip": device.ip }
        })
    );

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
        for (const [key, value] of Object.entries(data.message)) {
            // data.message = "IP: " + item.ip_address + " | " + "Response: " + item.response + " | " + "Message: " + item.message;

            // flex_Element_Update_Device:
            // element: str,
            // ip_list: str,
            // connection_status: str,
            // cron_job_status: str,
            // backup_script_status: str,
            // background_class: str
            console.log(key, value);

            if (value.check === "True") {
                value["backup_information"]

                // TODO: Check if statuses are correct
                flex_Element_Update_Device(
                    device_elements[key],
                    key,
                    "🟢",
                    "🟢",
                    "🟢",
                    "bg-gif-ok-green",
                );

            } else if (value.check === "False") {
                flex_Element_Update_Device(
                    device_elements[key],
                    key,
                    "🔴",
                    "🔴",
                    "🔴",
                    "bg-gif-alert-red-4",
                );
            } else {
                console.warn(`Unexpected value for ${key} => value.check: ${value.check}`);
                flex_Element_Update_Device(
                    device_elements[key],
                    key,
                    "⚫",
                    "⚫",
                    "⚫",
                    "bg-gif-noise-1",
                );
            }
        }

        // showNotification(notification, "info");

        if (button !== null || button !== undefined) {
            button.disabled = false;
        }
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
        button_disable_by_element(button, false);
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