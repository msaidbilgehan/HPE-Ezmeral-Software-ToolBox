
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
