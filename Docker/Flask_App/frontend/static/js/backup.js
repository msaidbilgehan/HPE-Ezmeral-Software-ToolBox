import { endpoint_action_2_url } from './page_specific_urls.js';
import { get_ssh_credentials } from './ssh_credentials.js';
// import { add_device, get_Devices, set_Device_Property } from './device_table.js';
import { get_Flex_Container_Devices, flex_Element_Update_Device, flex_Element_Clear_Devices, flex_Element_Add_Device } from './flex_container.js';
import { get_ip_host_addresses } from './ip_hostname_table.js';
import { showNotification } from './notification.js';
import { button_disable_by_element } from './tools.js';


function backup_cron_control(button) {
    button_disable_by_element(button, true);

    flex_Element_Clear_Devices();
    let ip_table_input = get_ip_host_addresses(true);

    // let tmp_ip_addresses = "";
    // ip_table_input.forEach(element => {
    //     if (tmp_ip_addresses === "") {
    //         tmp_ip_addresses = element["ip"];
    //     }
    //     else {
    //         tmp_ip_addresses = tmp_ip_addresses + ", " + element["ip"];
    //     }
    // });
    // ip_table_input = tmp_ip_addresses;

    // if (ip_table_input !== "") {
    //     add_device(ip_table_input);
    // }

    // let devices = get_Devices();

    // devices.forEach(device => {
    //     let deviceElement = document.getElementById(device.element.id);
    //     let propertyName = "status";
    //     let propertyValue = "waiting";
    //     set_Device_Property(deviceElement, propertyName, propertyValue);
    // })

    // let ipAddresses = devices.map((device) => {
    //     return {"ip": device.name};
    // });
    
    // let ipAddressesJson = JSON.stringify(ipAddresses);

    let device_elements = flex_Element_Add_Device(ip_table_input.map(device => device.ip));
    // get_Flex_Container_Devices();

    let ipAddressesJson = JSON.stringify(ip_table_input);

    let credentials = get_ssh_credentials();
    let ssh_usernameJson = credentials[0];
    let ssh_passwordJson = credentials[1];

    // Append the IP addresses as a query parameter
    let url = endpoint_action_2_url;
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses_hostnames=' + encodeURIComponent(ipAddressesJson);

    // Call Endpoint
    fetchTimeout()
    fetch(url).then(response => response.json()).then(data => {
        // console.log(typeof data.message[Symbol.iterator]);
        // console.log(typeof data.message instanceof Array);

        if (typeof data.message instanceof Array){
            data.message.forEach(item => {
                // let notification = "IP: " + item.ip_address + " | " + "Response: " + item.response + " | " + "Message: " + item.message;

                // devices.forEach(device => {
                //     if (device.name === item.ip_address) {

                //         let deviceElement = document.getElementById(device.element.id);
                //         let propertyName = "status";

                //         let propertyValue;
                //         if (item.check === "True") {
                //             propertyValue = "completed";
                //         } else if (item.check === "False") {
                //             propertyValue = "error";
                //         } else {
                //             console.warn(`Unexpected value for item.check: ${item.check}`);
                //         }

                //         set_Device_Property(deviceElement, propertyName, propertyValue);
                //     }
                // })

                // "IP: " + item.ip_address + " | " + "Response: " + item.response + " | " + "Message: " + item.message;

                let ip_list_connected = [];
                let ip_list_not_connected = [];

                if (item.check === "True") {

                    // TODO: Check if statuses are correct

                    ip_list_connected.push({
                        "ip": item.ip_address,
                        "connection_status": "🟢",
                        "backup_script_status": "🟢",
                        "cron_job_status": "🟢",
                        "background_class": "bg-gif-ok-green",
                    });

                } else if (item.check === "False") {

                    ip_list_not_connected.push({
                        "ip": item.ip_address,
                        "connection_status": "🔴",
                        "backup_script_status": "🔴",
                        "cron_job_status": "🔴",
                        "background_class": "bg-gif-alert-red-4",
                    });
                } else {

                    console.warn(`Unexpected value for item.check: ${item.check}`);
                    ip_list_not_connected.push({
                        "ip": item.ip_address,
                        "connection_status": "⚫",
                        "backup_script_status": "⚫",
                        "cron_job_status": "⚫",
                        "background_class": "bg-gif-noise-1",
                    });
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
                    ip_list_connected.map(item => item.ip),
                    ip_list_connected.map(item => item.connection_status),
                    ip_list_connected.map(item => item.cron_job_status),
                    ip_list_connected.map(item => item.backup_script_status),
                    ip_list_connected.map(item => item.background_class),
                );
                // Not Connected Flex Container Update
                flex_Element_Update_Device(
                    device_elements,
                    ip_list_not_connected.map(item => item.ip),
                    ip_list_not_connected.map(item => item.connection_status),
                    ip_list_not_connected.map(item => item.cron_job_status),
                    ip_list_not_connected.map(item => item.backup_script_status),
                    ip_list_not_connected.map(item => item.background_class),
                );
            });
        }
        else{
            showNotification("Server: " + data.message, "info");
        }
        

        // showNotification(notification, "info");
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
    });
    button_disable_by_element(button, false);
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