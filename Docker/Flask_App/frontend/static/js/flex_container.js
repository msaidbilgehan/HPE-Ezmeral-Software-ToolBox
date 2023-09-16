import { getActiveTabElement } from './general_action_buttons.js';


function get_Flex_Container_Element(){
    let active_tab = getActiveTabElement();
    let flex_Container_Element;

    if (active_tab === null) {
        flex_Container_Element = document.getElementById('flex_container');
    }
    else {
        flex_Container_Element = active_tab.querySelector('#flex_container');
    }
    return flex_Container_Element;
}


export function add_Element_to_Flex_Container(context) {
    let flex_Container_Element = get_Flex_Container_Element();
    let flex_Container_Element_SubMenu = flex_Container_Element.querySelector("#flex_container_content");

    const li = document.createElement('li');
    
    li.className = "submenu submenu_handle bg-info";

    li.setAttribute('data-toggle', 'tooltip');
    // li.setAttribute('title', 'Drag N Drop');
    
    console.log(context);
    li.textContent = context;

    flex_Container_Element_SubMenu.appendChild(li);
}


document.addEventListener('DOMContentLoaded', () => {
    let container = get_Flex_Container_Element();
    var sortable = new Draggable.Sortable(container.querySelectorAll("#flex_container_content"), {
        draggable: ".submenu",
        handle: ".submenu_handle",
        swapAnimation: {
            duration: 200,
            easingFunction: "ease-in-out",
            vertical: true
        },
        plugins: [Draggable.Plugins.SwapAnimation]
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});