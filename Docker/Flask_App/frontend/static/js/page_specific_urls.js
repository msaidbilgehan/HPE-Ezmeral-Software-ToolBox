export var terminal_source_url = "";
export var eventsource_source_url = "";
export var eventsource_action_clear_files_url = "/clear_action_files";
export var eventsource_action_clear_logs_url = "";
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
            eventsource_action_clear_logs_url = "/clear_Log_Collection_Log_Files";
            break;
        case 'cleanup':
            terminal_source_url = '/cleanup_terminal_endpoint';
            eventsource_source_url = '/cleanup_endpoint';
            terminal_log_download_source_url = '/cleanup_download_terminal_log_endpoint';
            terminal_source_stop_url = "/cleanup_stop_endpoint";
            eventsource_action_clear_logs_url = "";
            break;
        case 'fqdn':
            terminal_source_url = '/fqdn_terminal_endpoint';
            eventsource_source_url = '/fqdn_endpoint';
            terminal_log_download_source_url = '/fqdn_download_terminal_log_endpoint';
            terminal_source_stop_url = "/fqdn_stop_endpoint";
            eventsource_action_clear_logs_url = "";
            break;
        case 'backup':
            terminal_source_url = '/backup_terminal_endpoint';
            eventsource_source_url = '/backup_endpoint';
            terminal_log_download_source_url = '/backup_download_terminal_log_endpoint';
            terminal_source_stop_url = "/backup_stop_endpoint";
            eventsource_action_clear_logs_url = "";
            break;
        default:
            terminal_source_url = '/not-found';
            eventsource_source_url = '/not-found';
            terminal_log_download_source_url = '/not-found';
            terminal_source_stop_url = "/not-found";
            eventsource_action_clear_logs_url = "";
            break;
    }
    window.terminal_source_url = terminal_source_url;
    window.eventsource_source_url = eventsource_source_url;
    window.eventsource_action_clear_url = eventsource_action_clear_files_url;
    window.terminal_log_download_source_url = terminal_log_download_source_url;
    window.terminal_source_stop_url = terminal_source_stop_url;
    
}

// Call the function on page load
pageSpecificFunction()
// document.addEventListener('DOMContentLoaded', pageSpecificFunction);

