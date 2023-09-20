

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

export function checkResponses_restore(responses) {
    let allTrue = true;
    let allFalse = true;

    for (let key in responses) {
        if (responses[key].connection === false) {
            allTrue = false;
        } else {
            allFalse = false;
        }
    }

    if (allTrue) {
        return [true, "🟢"];
    } else if (allFalse) {
        return [false, "🔴"];
    } else {
        return [null, "🟡"];
    }
}
