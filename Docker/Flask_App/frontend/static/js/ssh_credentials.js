// import { endpoint_action_url } from './page_specific_urls.js';
// import { get_ip_host_addresses } from './ip_hostname_table.js';


// document.getElementById('ipForm').addEventListener('submit', function (event) {
//     event.preventDefault();

//     let pageType = document.body.getAttribute('data-page-type');

//     // Encode the IP addresses array into a JSON string

//     let ipAddressesHostnamesJson;

//     if (pageType === 'fqdn') {
//         // You can further validate each IP with Hostname if needed
//         ipAddressesHostnamesJson = get_ip_host_addresses(false);

//     } else {
//         ipAddressesHostnamesJson = get_ip_host_addresses(true);
//     }
//     let credentials = get_ssh_credentials();
//     let ssh_usernameJson = credentials[0];
//     let ssh_passwordJson = credentials[1];

//     // Append the IP addresses as a query parameter
//     let url = endpoint_action_url
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
function getActiveTabInputs() {
    // Aktif tabı belirleyin (örneğin, 'active' class'ına sahip olan tab)
    let activeTab = document.querySelector('.tab-content .active');

    // Aktif tab içindeki inputları seçin
    let sshUsernameInput = activeTab.querySelector('.ssh-username-input');
    let sshPasswordInput = activeTab.querySelector('.ssh-password-input');

    return {
        username: sshUsernameInput.value,
        password: sshPasswordInput.value
    };
}

export function get_ssh_credentials(){
    let activeTab = document.querySelector('.tab-content .active');
    let sshUsernameInput = activeTab.querySelector('#input_SSH_Username');
    let sshPasswordInput = activeTab.querySelector('#input_SSH_Password');

    let ssh_username = sshUsernameInput.value;
    let ssh_password = sshPasswordInput.value;

    let ssh_usernameJson = JSON.stringify(ssh_username);
    let ssh_passwordJson = JSON.stringify(ssh_password);

    return [ssh_usernameJson, ssh_passwordJson]
}
