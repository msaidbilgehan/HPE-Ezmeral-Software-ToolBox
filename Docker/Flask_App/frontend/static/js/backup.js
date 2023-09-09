import { endpoint_action_2_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
import { terminal_source } from './terminal_stream.js';
import { get_Devices } from './device_table.js';


function backup_cron_control() {

    // Encode the IP addresses array into a JSON string
    // let ipAddressesJson = get_ip_host_addresses(true);
    let ipAddressesJson = "";
    let devices = get_Devices();
    console.log("devices:", devices);
    devices.forEach(device => {
        if (ipAddressesJson) {
            ipAddressesJson = ipAddressesJson + ", " + device.name;
        } else {
            ipAddressesJson = device.name;
        }
    });
    ipAddressesJson = JSON.stringify(ipAddressesJson);


    let credentials = get_ssh_credentials();
    console.log("credentials:", credentials);
    let ssh_usernameJson = credentials[0];
    let ssh_passwordJson = credentials[1];

    console.log("ipAddressesJson:", ipAddressesJson);
    console.log("ssh_usernameJson, ssh_passwordJson:", ssh_usernameJson, ssh_passwordJson);

    // Append the IP addresses as a query parameter
    let url = endpoint_action_2_url
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesJson);

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