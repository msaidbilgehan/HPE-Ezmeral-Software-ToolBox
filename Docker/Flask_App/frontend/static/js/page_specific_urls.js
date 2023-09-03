export var terminal_source_url = "";
export var eventsource_source_url = "";
export var terminal_log_download_source_url = "";
export var terminal_source_stop_url = "";

function pageSpecificFunction() {
    var pageType = document.body.getAttribute('data-page-type');
    // console.log("pageType:", pageType);
    switch (pageType) {
        case 'log_collection':
            terminal_source_url = '/log_collection_terminal_endpoint';
            eventsource_source_url = '/log_collection_endpoint';
            terminal_log_download_source_url = '/log_collection_download_terminal_log_endpoint';
            terminal_source_stop_url = "/log_collection_stop_endpoint";
            break;
        case 'cleanup':
            terminal_source_url = '/cleanup_terminal_endpoint';
            eventsource_source_url = '/cleanup_endpoint';
            terminal_log_download_source_url = '/cleanup_download_terminal_log_endpoint';
            terminal_source_stop_url = "/cleanup_stop_endpoint";
            break;
        case 'fqdn':
            terminal_source_url = '/fqdn_terminal_endpoint';
            eventsource_source_url = '/fqdn_endpoint';
            terminal_log_download_source_url = '/fqdn_download_terminal_log_endpoint';
            terminal_source_stop_url = "/fqdn_stop_endpoint";
            break;
        default:
            terminal_source_url = '/not-found';
            eventsource_source_url = '/not-found';
            terminal_log_download_source_url = '/not-found';
            terminal_source_stop_url = "/not-found";
            break;
    }
    window.terminal_source_url = terminal_source_url;
    window.eventsource_source_url = eventsource_source_url;
    window.terminal_log_download_source_url = terminal_log_download_source_url;
    window.terminal_source_stop_url = terminal_source_stop_url;
}

// Call the function on page load
pageSpecificFunction()
// document.addEventListener('DOMContentLoaded', pageSpecificFunction);

