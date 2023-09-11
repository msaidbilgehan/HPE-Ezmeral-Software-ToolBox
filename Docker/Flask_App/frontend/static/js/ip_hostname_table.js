
import { getActiveTabElement } from './general_action_buttons.js';


export function get_ip_host_addresses(only_ip) {
    let active_tab = getActiveTabElement();
    let input_ipAddressesHostnames;

    if (active_tab === null) {
        input_ipAddressesHostnames = document.getElementById('input_IP_Addresses_Hostnames').value;
    }
    else{
        input_ipAddressesHostnames = active_tab.querySelector('#input_IP_Addresses_Hostnames').value;
    }
    

    // Split the IP addresses by a newline or comma
    let ipAddressesHostnames = input_ipAddressesHostnames.split(/\s*[,|\n]\s*/);

    if (only_ip) {
        // You can further validate each IP if needed
        ipAddressesHostnames = ipAddressesHostnames.map(function (entry) {
            let match = entry.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
            return match ? match[0] : null;
        }).filter(Boolean);
    }
    else {
        // You can further validate each IP with Hostname if needed
        ipAddressesHostnames = ipAddressesHostnames.filter(function (entry) {
            return /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[-\t\s]+\w+\b/.test(entry);
        });
        ipAddressesHostnames = ipAddressesHostnames.map(function (entry) {
            let parts = entry.split(/[-\t\s]+/);
            return {
                ip: parts[0],
                hostname: parts[1]
            };
        });
    }

    return ipAddressesHostnames
}