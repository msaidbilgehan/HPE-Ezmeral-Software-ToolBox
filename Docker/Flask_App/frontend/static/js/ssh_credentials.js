// import { endpoint_action_url } from './page_specific_urls.js';
// import { get_ip_host_addresses } from './ip_hostname_table.js';


// document.getElementById('ipForm').addEventListener('submit', function (event) {
//     event.preventDefault();

//     var pageType = document.body.getAttribute('data-page-type');

//     // Encode the IP addresses array into a JSON string

//     var ipAddressesHostnamesJson;

//     if (pageType === 'fqdn') {
//         // You can further validate each IP with Hostname if needed
//         ipAddressesHostnamesJson = get_ip_host_addresses(false);

//     } else {
//         ipAddressesHostnamesJson = get_ip_host_addresses(true);
//     }
//     var credentials = get_ssh_credentials();
//     var ssh_usernameJson = credentials[0];
//     var ssh_passwordJson = credentials[1];

//     // Append the IP addresses as a query parameter
//     var url = endpoint_action_url
//     url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
//     url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
//     url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesHostnamesJson);

//     // Call Endpoint
//     fetch(url).then(response => response.json()).then(data => {
//         // console.log(data.message);
//         showNotification(data.message, "info");
//     }).catch(error => {
//         console.error(error);
//         showNotification(error, "error");
//     });
// });

export function get_ssh_credentials(){

    var ssh_username = document.getElementById('input_SSH_Username').value;
    var ssh_password = document.getElementById('input_SSH_Password').value;

    var ssh_usernameJson = JSON.stringify(ssh_username);
    var ssh_passwordJson = JSON.stringify(ssh_password);

    return [ssh_usernameJson, ssh_passwordJson]
}
