

export function button_disable_by_id(button_id = "", disable = true) {
    let button = document.getElementById(button_id);
    if (button !== null || button !== undefined) {
        button.disabled = disable;
    }
}

export function button_disable_by_element(button, disable = true) {
    if (button !== null || button !== undefined) {
        button.disabled = disable;
    }
}