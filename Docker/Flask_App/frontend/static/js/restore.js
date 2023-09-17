import { endpoint_action_2_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
// import { get_Devices, set_Device_Property } from './device_table.js';
import { get_ip_host_addresses } from './ip_hostname_table.js';
import { flex_Element_Add_Device, flex_Element_Update_Device, flex_Element_Clear_Devices } from './flex_container.js';
import { showNotification } from './notification.js';



function restore_control(button = null) {
    if (button !== null || button !== undefined){
        button.disabled = true;
    }
    
    flex_Element_Clear_Devices();
    let device_ip_addresses = get_ip_host_addresses(true);
    let device_elements = flex_Element_Add_Device(device_ip_addresses.map(device => device.ip));
    
    let ipAddressesJson = JSON.stringify(
        device_ip_addresses.map(device => {
            return { "ip": device.ip }
        })
    );
    console.log(ipAddressesJson);

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
        let ip_list_connected = [];
        let ip_list_not_connected = [];

        data.message.forEach(item => {
            // "IP: " + item.ip_address + " | " + "Response: " + item.response + " | " + "Message: " + item.message;
            let flex_Element_classes = [];
            
            let connection_status = [];
            let backup_script_status = [];
            let cron_job_status = [];

            let background_class =[];

            if (item.check === "True") {
                flex_Element_classes = "bg-gif-green-circle";
                
                // TODO: Check if statuses are correct
                connection_status.push("🟢");
                backup_script_status.push("🟢");
                cron_job_status.push("🟢");

                background_class.push("bg-gif-data-center-1");

                ip_list_connected.push(item.ip_address);

            } else if (item.check === "False") {
                flex_Element_classes = "bg-gif-lost";
                
                connection_status.push("🔴");
                backup_script_status.push("🔴");
                cron_job_status.push("🔴");

                background_class.push("bg-gif-no-connection");

                ip_list_not_connected.push(item.ip_address);
            } else {
                flex_Element_classes = "bg-gif-black-hole-red";
                
                connection_status.push("⚫");
                backup_script_status.push("⚫");
                cron_job_status.push("⚫");

                background_class.push("bg-gif-no-connection");

                console.warn(`Unexpected value for item.check: ${item.check}`);
                ip_list_not_connected.push(item.ip_address);
            }

            // elements: any[] | undefined,
            // ip_list: any[] | undefined,
            // connection_status: any,
            // cron_job_status: any,
            // backup_script_status: any,
            // background_class: any

            // Connected Flex Container Update
            flex_Element_Update_Device(
                device_elements, 
                ip_list_connected, 
                connection_status,
                cron_job_status,
                backup_script_status,
                background_class,
            );
            // Not Connected Flex Container Update
            flex_Element_Update_Device(
                device_elements,
                ip_list_not_connected,
                device_elements.map(element => "⚫"),
                device_elements.map(element => "⚫"),
                device_elements.map(element => "⚫"),
                device_elements.map(element => "bg-gif-no-connection"),
            );
            // showNotification(notification, "info");
        });

        // showNotification(notification, "info");

        if (button !== null || button !== undefined) {
            button.disabled = false;
        }
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");

        if (button !== null || button !== undefined) {
            button.disabled = false;
        }
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