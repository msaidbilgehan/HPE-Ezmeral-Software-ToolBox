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
    fetch(url).then(response => response.json()).then(data => {
        // console.log(typeof data.message[Symbol.iterator]);
        // console.log(typeof data.message instanceof Array);
        // console.log(Array.isArray(data.message));

        if (Array.isArray(data.message)){
            data.message.forEach(item => {
                // data.message = "IP: " + item.ip_address + " | " + "Response: " + item.response + " | " + "Message: " + item.message;

                // flex_Element_Update_Device:
                // element: str,
                // ip: str,
                // connection_status: str,
                // cron_job_status: str,
                // backup_script_status: str,
                // background_class: str

                if (item.check === "True") {

                    // TODO: Check if statuses are correct

                    // Connected Flex Container Update
                    flex_Element_Update_Device(
                        device_elements[item.ip_address],
                        item.ip_address,
                        "🟢",
                        "🟢",
                        "🟢",
                        "-",
                        "bg-gif-ok-green",
                    );

                } else if (item.check === "False") {
                    
                    // Connected Flex Container Update
                    flex_Element_Update_Device(
                        device_elements[item.ip_address],
                        item.ip_address,
                        "🔴",
                        "🔴",
                        "🔴",
                        "-",
                        "bg-gif-alert-red-4",
                    );
                } else {

                    console.warn(`Unexpected value for item.check: ${item.check}`);

                    // Connected Flex Container Update
                    flex_Element_Update_Device(
                        device_elements[item.ip_address],
                        item.ip_address,
                        "⚫",
                        "⚫",
                        "⚫",
                        "-",
                        "bg-gif-noise-1",
                    );
                }
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