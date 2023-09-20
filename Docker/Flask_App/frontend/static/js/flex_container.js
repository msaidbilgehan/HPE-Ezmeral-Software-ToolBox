import { getActiveTabElement } from './general_action_buttons.js';



// Add Device to Flex Container
export function flex_Element_Add_Device(ip_list = []) {
    let status_emoji = "🔵";
    let sub_div_classes = "bg-color-black-25 bg-blur-5px w-100 align-items-left";
    let sub_div_color = "text-shadow-black-0px color-white";
    let sub_div_classes_latest = sub_div_classes + " " + sub_div_color;

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
        sub_div.className = "d-flex flex-sm-column mb-2 " + sub_div_classes_latest;

        // IP Information
        let sub_div_IP = document.createElement('div');
        sub_div_IP.setAttribute("id", "sub_div_IP_" + ip_replaced);
        sub_div_IP.className = sub_div_classes_latest;
        sub_div_IP.innerHTML = "IP: " + ip_replaced + " " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_IP);

        // IP Information
        let sub_div_Backup_ID = document.createElement('div');
        sub_div_Backup_ID.setAttribute("id", "sub_div_Backup_ID_" + ip_replaced);
        sub_div_Backup_ID.className = sub_div_classes_latest;
        sub_div_Backup_ID.innerHTML = "ID: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_Backup_ID);

        // Cron Job Status Information
        let sub_div_Cron_Job = document.createElement('div');
        sub_div_Cron_Job.setAttribute("id", "sub_div_Cron_Job_" + ip_replaced);
        sub_div_Cron_Job.className = sub_div_classes_latest;
        sub_div_Cron_Job.innerHTML = "Cron Job: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_Cron_Job);

        // Backup Script File Status Information
        let sub_div_backup_script = document.createElement('div');
        sub_div_backup_script.setAttribute("id", "sub_div_Backup_Script_" + ip_replaced);
        sub_div_backup_script.className = sub_div_classes_latest;
        sub_div_backup_script.innerHTML = "Backup Script: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_backup_script);

        // Restore Script File Status Information
        let sub_div_restore_script = document.createElement('div');
        sub_div_restore_script.setAttribute("id", "sub_div_Restore_Script_" + ip_replaced);
        sub_div_restore_script.className = sub_div_classes_latest;
        sub_div_restore_script.innerHTML = "Restore Script: " + status_emoji;

        // Append Child element to Container
        sub_div.appendChild(sub_div_restore_script);

        // Cron Job Status Information
        let sub_div_Backups = document.createElement('div');
        sub_div_Backups.setAttribute("id", "sub_div_Backups_" + ip_replaced);
        sub_div_Backups.className = sub_div_classes_latest;
        sub_div_Backups.innerHTML = "Backups: " + "-";

        // Append Child element to Container
        sub_div.appendChild(sub_div_Backups);

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

export function flex_Element_Update_Device(element = "", ip = "", connection_status = "", backup_id = "", cron_job_status = "", backup_script_status = "", restore_script_status = "", backups = "0", background_class = "") {
    if (element === "" || element === null || element === undefined) {
        console.error("No element provided!");
        return;
    }

    ip = ip.replace(/\./g, '-');
    if (element.id.includes(ip)) {

        element.parentElement.setAttribute("class", "submenu submenu_handle " + background_class);

        if (connection_status !== null && connection_status !== undefined && connection_status !== "") {
            let sub_div_IP = element.querySelector("#sub_div_IP_" + ip);
            sub_div_IP.innerHTML = "IP: " + ip + " " + connection_status;
        }
        if (backup_id !== null && backup_id !== undefined && backup_id !== "") {
            let sub_div_Backup_ID = element.querySelector("#sub_div_Backup_ID_" + ip);
            sub_div_Backup_ID.innerHTML = "ID: " + backup_id;
        }
        if (cron_job_status !== null && cron_job_status !== undefined && cron_job_status !== "") {
            let sub_div_Cron_Job = element.querySelector("#sub_div_Cron_Job_" + ip);
            sub_div_Cron_Job.innerHTML = "Cron Job: " + cron_job_status;
        }
        if (backup_script_status !== null && backup_script_status !== undefined && backup_script_status !== "") {
            let sub_div_backup_script = element.querySelector("#sub_div_Backup_Script_" + ip);
            sub_div_backup_script.innerHTML = "Backup Script: " + backup_script_status;
        }
        if (restore_script_status !== null && restore_script_status !== undefined && restore_script_status !== "") {
            let sub_div_restore_script = element.querySelector("#sub_div_Restore_Script_" + ip);
            sub_div_restore_script.innerHTML = "Restore Script: " + restore_script_status;
        }
        if (backups !== null && backups !== undefined && backups !== "0") {
            let sub_div_Backups = element.querySelector("#sub_div_Backups_" + ip);
            sub_div_Backups.innerHTML = "Backups: " + backups;
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
export function draggable_activate() {
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
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
draggable_activate();