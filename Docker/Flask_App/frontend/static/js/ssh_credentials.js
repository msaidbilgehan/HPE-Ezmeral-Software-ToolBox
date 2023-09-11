import { getActiveTabElement } from './general_action_buttons.js';


export function get_ssh_credentials(){
    let activeTab = getActiveTabElement();

    let sshUsernameInput;
    let sshPasswordInput;

    if (activeTab !== null) {
        sshUsernameInput = activeTab.querySelector('.ssh-username-input');
        sshPasswordInput = activeTab.querySelector('.ssh-password-input');
    } else {
        sshUsernameInput = document.querySelector('#input_SSH_Username');
        sshPasswordInput = document.querySelector('#input_SSH_Password');
    }
    

    let ssh_username = sshUsernameInput.value;
    let ssh_password = sshPasswordInput.value;

    let ssh_usernameJson = JSON.stringify(ssh_username);
    let ssh_passwordJson = JSON.stringify(ssh_password);

    return [ssh_usernameJson, ssh_passwordJson]
}
