import { endpoint_action_url, endpoint_stop_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
import { get_ip_host_addresses } from './ip_hostname_table.js';
import { showNotification } from './notification.js';
import { button_disable_by_element } from './tools.js';


function start_Action (button) {
    button_disable_by_element(button, true);
    var pageType = document.body.getAttribute('data-page-type');

    // Encode the IP addresses array into a JSON string

    var ipAddressesHostnamesJson;
    var ipAddressesHostnames;
    // var extra_parameter;
    // var extra_parameter_value;

    if (pageType === 'fqdn') {
        // You can further validate each IP with Hostname if needed
        ipAddressesHostnames = get_ip_host_addresses(false);

    } else {
        ipAddressesHostnames = get_ip_host_addresses(true);
    }

    // Encode the IP addresses array into a JSON string
    var ipAddressesHostnamesJson = JSON.stringify(ipAddressesHostnames);

    var credentials = get_ssh_credentials();
    var ssh_usernameJson = credentials[0];
    var ssh_passwordJson = credentials[1];

    // Append the IP addresses as a query parameter
    var url = endpoint_action_url
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesHostnamesJson);

    // if (pageType === 'backup') {
    //     extra_parameter = "backup_type";
    //     extra_parameter_value = get_Backup_Type();
    //     url = url + '&' + extra_parameter + '=' + encodeURIComponent(extra_parameter_value);
    // }

    // Call Endpoint
    fetch(url).then(response => response.json()).then(data => {
        // console.log(data.message);
        showNotification(data.message, "info");
        
        button_disable_by_element(button, false);
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");

        button_disable_by_element(button, false);
    });
}
window.start_Action = start_Action;



function stop_Action(button) {
    button_disable_by_element(button, true);

    var pageType = document.body.getAttribute('data-page-type');
    fetch(endpoint_stop_url + "/" + pageType)
        .then(response => response.json())
        .then(data => {
            // document.getElementById('output').innerText = data.message;
            showNotification(data.message, "info");
        })
        .catch(error => {
            console.error('An error occurred:', error);
            showNotification('An error occurred: ' + error, "error");
        });

    button_disable_by_element(button, false);
}
window.stop_Action = stop_Action;



export function getActiveTabElement() {
    return document.querySelector('.tab-content .active');
}