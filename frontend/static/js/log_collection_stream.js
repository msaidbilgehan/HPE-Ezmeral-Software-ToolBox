var terminal_source;

function terminal_EventSource_Start(url) {
    clear_Log_Buffer();

    var contentDiv = document.getElementById('stream_content');
    if (terminal_source) {
        terminal_source.close();
    }
    terminal_source = new EventSource(url); // use the URL with the IP addresses
    
    terminal_source.onerror = function (error) {
        console.error("EventSource failed:", error);
        showNotification('EventSource failed: ' + error, "error");
        terminal_source.close(); // close the connection if an error occurs
    };

    terminal_source.onmessage = function (event) {
        // console.info("EventSource:", event.data);
        contentDiv.innerHTML += event.data + "<br>"; // append each new log line to the content div

        // Check if the user is at or near the bottom of the container
        var container = document.querySelector('.fakeScreen');
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - 50) { // 50px tolerance
            // Scroll to the bottom
            container.scrollTop = container.scrollHeight;
        }
    };
}

function terminal_EventSource_Stop() {
    if (terminal_source) {
        terminal_source.close();
    }
}


function clear_Log_Collection_Log_Files() {
    var contentDiv = document.getElementById('stream_content');
    contentDiv.innerHTML = ""; // clear the content div

    fetch('/clear_Log_Collection_Log_Files')
        .then(response => response.json())
        .then(data => {
            // document.getElementById('output').innerText = data.message;
            showNotification(data.message, "info");
        })
        .catch(error => {
            console.error('An error occurred:', error);
            showNotification('An error occurred: ' + error, "error");
        });
}

function clear_Log_Buffer() {
    var contentDiv = document.getElementById('stream_content');
    contentDiv.innerHTML = ""; // clear the content div

    fetch('/clear_Log_Buffer')
        .then(response => response.json())
        .then(data => {
            // document.getElementById('output').innerText = data.message;
            showNotification(data.message, "info");
        })
        .catch(error => {
            console.error('An error occurred:', error);
            showNotification('An error occurred: ' + error, "error");
        });
}


document.getElementById('listen_logs-btn').addEventListener('click', function () {
    terminal_EventSource_Start('/log_collection_log_endpoint');
});


document.getElementById('stop-btn').addEventListener('click', function () {
    fetch('/log_collection_log_stop_endpoint')
        .then(response => response.json())
        .then(data => {
            // document.getElementById('output').innerText = data.message;
            showNotification(data.message, "info");
        })
        .catch(error => {
            console.error('An error occurred:', error);
            showNotification('An error occurred: ' + error, "error");
        });
});


document.getElementById('ipForm').addEventListener('submit', function (event) {
    event.preventDefault();
    
    var ipInput = document.getElementById('input_IP_Addresses').value;
    var ssh_username = document.getElementById('input_SSH_Username').value;
    var ssh_password = document.getElementById('input_SSH_Password').value;

    // Split the IP addresses by a newline or comma
    var ipAddresses = ipInput.split(/\s*[,|\n]\s*/);

    // You can further validate each IP if needed
    ipAddresses = ipAddresses.filter(function (ip) {
        return /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/.test(ip);
    });

    // Now you have an array of IP addresses, you can send them to the server or process them as needed
    // console.log(ipAddresses);

    // Encode the IP addresses array into a JSON string
    var ipAddressesJson = JSON.stringify(ipAddresses);
    var ssh_usernameJson = JSON.stringify(ssh_username);
    var ssh_passwordJson = JSON.stringify(ssh_password);

    // Append the IP addresses as a query parameter
    var url = '/log_collection_API'
    url = url + '?ssh_username=' + encodeURIComponent(ssh_usernameJson);
    url = url + '&ssh_password=' + encodeURIComponent(ssh_passwordJson);
    url = url + '&ip_addresses=' + encodeURIComponent(ipAddressesJson);

    if (!terminal_source || terminal_source.readyState === 2) {
        terminal_EventSource_Start('/log_collection_log_endpoint');
    }

    // Call Endpoint
    fetch(url).then(response => response.json()).then(data => {
        // console.log(data.message);
        showNotification(data.message, "info");
    }).catch(error => {
        console.error(error);
        showNotification(error, "error");
    });
});


terminal_EventSource_Start('/log_collection_log_endpoint');
