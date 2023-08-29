import { eventsource_source_url } from './page_specific_urls.js';



document.getElementById('ipForm').addEventListener('submit', function (event) {
    event.preventDefault();

    var ipInput = document.getElementById('input_IP_Addresses_Hostnames').value;
    var ssh_username = document.getElementById('input_SSH_Username').value;
    var ssh_password = document.getElementById('input_SSH_Password').value;

    // Split the IP addresses by a newline or comma
    var ipAddressesHostnames = ipInput.split(/\s*[,|\n]\s*/);
    console.log("ipAddressesHostnames: " + ipAddressesHostnames);

    var pageType = document.body.getAttribute('data-page-type');

    if (pageType === 'fqdn') {
        // You can further validate each IP with Hostname if needed
        ipAddressesHostnames = ipAddressesHostnames.filter(function (entry) {
            return /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[-\t\s]+\w+\b/.test(entry); 
        });
        ipAddressesHostnames = ipAddressesHostnames.map(function (entry) {
            var parts = entry.split(/[-\t\s]+/);
            return {
                ip: parts[0],
                hostname: parts[1]
            };
        });
    } else {
        // You can further validate each IP if needed
        ipAddressesHostnames = ipAddressesHostnames.map(function (entry) {
            var match = entry.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
            return match ? match[0] : null;
        }).filter(Boolean);
    }

    console.info(ipAddressesHostnames)


    // Now you have an array of IP addresses, you can send them to the server or process them as needed
    // console.log(ipAddressesHostnames);

    // Encode the IP addresses array into a JSON string
    var ipAddressesHostnamesJson = JSON.stringify(ipAddressesHostnames);
    var ssh_usernameJson = JSON.stringify(ssh_username);
    var ssh_passwordJson = JSON.stringify(ssh_password);

    // Append the IP addresses as a query parameter
    var url = eventsource_source_url
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesHostnamesJson);

    // if (!terminal_source || terminal_source.readyState === 2) {
    //     terminal_EventSource_Start(terminal_source_url);
    // }

    // Call Endpoint
    fetch(url).then(response => response.json()).then(data => {
        // console.log(data.message);
        showNotification(data.message, "info");
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
    });
});

// function updateProgressBar(percentage) {
//     var progressBar = document.querySelector('.progress-bar');
//     progressBar.style.width = percentage + '%';
//     progressBar.setAttribute('aria-valuenow', percentage);
// }