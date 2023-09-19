import { getActiveTabElement } from './general_action_buttons.js';



// Add Device to Flex Container
export function flex_Element_Add_Device(ip_list = []) {
    let status_emoji = "🔵";
    let sub_div_classes = "bg-color-black-25 bg-blur-5px w-100 align-items-left";
    let sub_div_color = "text-shadow-black-0px color-white";

    let element_list = {};
    
    if (ip_list.length === 0) {
        console.error("No IP Address provided!");
        return element_list;
    }
    ip_list.forEach(ip => {
        let ip_replaced = ip.replace(/\./g, '-');
        // Container
        let sub_div = document.createElement('div');
        sub_div.setAttribute("id", "sub_div_" + ip_replaced);
        sub_div.className = "d-flex flex-sm-column mb-2 " + sub_div_classes + " " + sub_div_color;

        // IP Input Box
        let sub_div_IP = document.createElement('div');
        sub_div_IP.setAttribute("id", "sub_div_IP_" + ip_replaced);
        sub_div_IP.className = sub_div_classes + " " + sub_div_color;
        sub_div_IP.innerHTML = "IP: " + ip_replaced;

        // Append Child element to Container
        sub_div.appendChild(sub_div_IP);

        // Connection Status Information
        let sub_div_Connection = document.createElement('div');
        sub_div_Connection.setAttribute("id", "sub_div_Connection_" + ip_replaced);
        sub_div_Connection.className = sub_div_classes + " " + sub_div_color;
        sub_div_Connection.innerHTML = "Connection Status: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_Connection);

        // Cron Job Status Information
        let sub_div_Cron_Job = document.createElement('div');
        sub_div_Cron_Job.setAttribute("id", "sub_div_Cron_Job_" + ip_replaced);
        sub_div_Cron_Job.className = sub_div_classes + " " + sub_div_color;
        sub_div_Cron_Job.innerHTML = "Cron Job Status: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_Cron_Job);

        // Backup Script File Status Information
        let sub_div_backup_script = document.createElement('div');
        sub_div_backup_script.setAttribute("id", "sub_div_backup_script_" + ip_replaced);
        sub_div_backup_script.className = sub_div_classes + " " + sub_div_color;
        sub_div_backup_script.innerHTML = "Backup Script Status: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_backup_script);

        element_list[ip] = sub_div;

        flex_Container_Add_Element(
            "",
            "bg-gif-setting-2",
            [],
            [sub_div],
        )
    });

    return element_list;
}

export function flex_Element_Update_Device(element = "", ip = "", connection_status = "", cron_job_status = "", backup_script_status = "", background_class = "") {
    if (element === "" || element === null || element === undefined) {
        console.error("No element provided!");
        return;
    }

    ip = ip.replace(/\./g, '-');
    if (element.id.includes(ip)) {

        element.parentElement.setAttribute("class", "submenu submenu_handle " + background_class);

        if (connection_status !== null && connection_status !== undefined && connection_status !== "") {
            let sub_div_Connection = element.querySelector("#sub_div_Connection_" + ip);
            sub_div_Connection.innerHTML = "Connection Status: " + connection_status;
        }
        if (cron_job_status !== null && cron_job_status !== undefined && cron_job_status !== "") {
            let sub_div_Cron_Job = element.querySelector("#sub_div_Cron_Job_" + ip);
            sub_div_Cron_Job.innerHTML = "Cron Job Status: " + cron_job_status;
        }
        if (backup_script_status !== null && backup_script_status !== undefined && backup_script_status !== "") {
            let sub_div_backup_script = element.querySelector("#sub_div_backup_script_" + ip);
            sub_div_backup_script.innerHTML = "Backup Script Status: " + backup_script_status;
        }
    };
}

export function get_Flex_Container_Devices(){
    let flex_Container_Element = get_Flex_Container_Element();
    let devices = flex_Container_Element.querySelectorAll(".submenu");
    return devices;
}


// Get Flex Container Element
function get_Flex_Container_Element(is_submenu = false){
    let active_tab = getActiveTabElement();
    let flex_Container_Element;

    if (active_tab === null) {
        flex_Container_Element = document.getElementById('flex_container');
    }
    else {
        flex_Container_Element = active_tab.querySelector('#flex_container');
    }

    if (is_submenu){
        return flex_Container_Element.querySelector("#flex_container_content");
    }
    else{
        return flex_Container_Element;
    }
}


// Add element to Flex Container
export function flex_Container_Add_Element(context, classes = "", sub_contexts = "", sub_elements = []) {
    let flex_Container_Element_SubMenu = get_Flex_Container_Element(true);

    const li = document.createElement('li');
    // li.setAttribute('id', 'flex_container_content_li');

    li.className = "submenu submenu_handle " + classes;

    li.setAttribute('data-toggle', 'tooltip');
    // li.setAttribute('title', 'Drag N Drop');
    li.textContent = context;

    if (sub_contexts !== null) {
        sub_contexts.forEach(sub_context => {
            const sub_div = document.createElement('div');
            sub_div.className = "bg-secondary color-green typewriter full_width text-center";
            sub_div.textContent = sub_context;
            li.appendChild(sub_div);
        });
    }

    if (sub_elements !== null) {
        sub_elements.forEach(sub_element => {
            li.appendChild(sub_element);
        });
    }

    flex_Container_Element_SubMenu.appendChild(li);
}

export function flex_Element_Clear_Devices(){
    let flex_Container_Element_SubMenu = get_Flex_Container_Element(true);
    flex_Container_Element_SubMenu.innerHTML = "";
}
window.flex_Element_Clear_Devices = flex_Element_Clear_Devices;


// Draggable Enable
document.addEventListener('DOMContentLoaded', () => {
    let container_submenu = get_Flex_Container_Element(true);
    var sortable = new Draggable.Sortable(container_submenu, {
        draggable: ".submenu",
        handle: ".submenu_handle",
        swapAnimation: {
            duration: 200,
            easingFunction: "linear",
            horizontal: true
        },
        plugins: [Draggable.Plugins.SwapAnimation]
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});