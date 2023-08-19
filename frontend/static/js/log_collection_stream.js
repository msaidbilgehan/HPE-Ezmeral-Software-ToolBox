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


document.getElementById('load_logs-btn').addEventListener('click', function () {
    var contentDiv = document.getElementById('stream_content');
    var source = new EventSource('/log_collection_buffered_API'); // make sure this path matches the server's endpoint
    // console.info("log_collection_buffered_API");
    // showNotification('log_collection_buffered_API', "warning");

    source.onerror = function (error) {
        console.error("EventSource failed:", error);
        showNotification('EventSource failed: ' + error, "error");
        source.close(); // close the connection if an error occurs
    };

    source.onmessage = function (event) {
        // console.info("EventSource:", event.data);
        contentDiv.innerHTML += event.data + "<br>"; // append each new log line to the content div

        // Check if the user is at or near the bottom of the container
        var container = document.querySelector('.fakeScreen');
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - 50) { // 50px tolerance
            // Scroll to the bottom
            container.scrollTop = container.scrollHeight;
        }
    };
});

document.getElementById('run-btn').addEventListener('click', function () {
    var contentDiv = document.getElementById('stream_content');
    var source = new EventSource('/log_collection_API'); // make sure this path matches the server's endpoint

    source.onerror = function (error) {
        console.error("EventSource failed:", error);
        showNotification('EventSource failed: ' + error, "error");
        source.close(); // close the connection if an error occurs
    };

    source.onmessage = function (event) {
        // console.info("EventSource:", event.data);
        contentDiv.innerHTML += event.data + "<br>"; // append each new log line to the content div

        // Check if the user is at or near the bottom of the container
        var container = document.querySelector('.fakeScreen');
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - 50) { // 50px tolerance
            // Scroll to the bottom
            container.scrollTop = container.scrollHeight;
        }
    };
});

