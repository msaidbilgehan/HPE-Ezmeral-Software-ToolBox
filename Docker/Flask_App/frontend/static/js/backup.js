import { endpoint_action_2_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
import { terminal_source } from './terminal_stream.js';
import { get_Devices } from './device_table.js';


function backup_cron_control() {

    let devices = get_Devices();
    let ipAddresses = devices.map(device => device.name);
    
    let ipAddressesJson = JSON.stringify(ipAddresses);


    let credentials = get_ssh_credentials();
    let ssh_usernameJson = credentials[0];
    let ssh_passwordJson = credentials[1];

    // Append the IP addresses as a query parameter
    let url = endpoint_action_2_url
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesJson);
    console.log("ipAddressesJson", ipAddressesJson);
    console.log("url", url);

    if (!terminal_source || terminal_source.readyState === 2) {
        terminal_EventSource_Start();
    }

    // Call Endpoint
    fetch(url).then(response => response.json()).then(data => {
        console.log(data);
        data.message.forEach(item => {
            let notification = "IP: " + item.ip_address + " | " + "Message: " + item.message;
            showNotification(notification, "info");
        });

        // showNotification(notification, "info");
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
    });
};
window.backup_cron_control = backup_cron_control;

export function get_Backup_Type(){
    let selectedRadio = document.querySelector('input[name="backup_type"]:checked');
    if (selectedRadio) {
        let selectedBackupType = selectedRadio.id;
        return selectedBackupType;
    } else {
        console.error("Backup type should be selected!");
    }
}