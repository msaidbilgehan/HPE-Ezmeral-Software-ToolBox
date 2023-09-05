import { terminal_source_url } from './page_specific_urls.js';


function backup_cron_control() {
    var ipInput = document.getElementById('input_IP_Addresses').value;
    var ssh_username = document.getElementById('input_SSH_Username').value;
    var ssh_password = document.getElementById('input_SSH_Password').value;

    // Split the IP addresses by a newline or comma
    var ipAddresses = ipInput.split(/\s*[,|\n]\s*/);

    // You can further validate each IP if needed
    ipAddresses = ipAddresses.filter(function (ip) {
        return /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/.test(ip);
    });

    // Now you have an array of IP addresses, you can send them to the server or process them as needed
    // console.log(ipAddresses);

    // Encode the IP addresses array into a JSON string
    var ipAddressesJson = JSON.stringify(ipAddresses);
    var ssh_usernameJson = JSON.stringify(ssh_username);
    var ssh_passwordJson = JSON.stringify(ssh_password);

    // Append the IP addresses as a query parameter
    var url = '/log_collection_endpoint'
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses=' + encodeURIComponent(ipAddressesJson);

    if (!terminal_source || terminal_source.readyState === 2) {
        var pageType = document.body.getAttribute('data-page-type');
        terminal_EventSource_Start(terminal_source_url + "/" + pageType);
    }

    // Call Endpoint
    fetch(url).then(response => response.json()).then(data => {
        // console.log(data.message);
        showNotification(data.message, "info");
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
    });
};
