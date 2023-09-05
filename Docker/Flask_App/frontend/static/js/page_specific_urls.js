// Specific Endpoints
export var eventsource_source_url = "";
export var eventsource_action_clear_logs_url = "";

// General Endpoints
export var terminal_log_download_source_url = "/download_terminal_log";
window.terminal_log_download_source_url = terminal_log_download_source_url;

export var terminal_source_url = "/terminal_endpoint";
export var endpoint_stop_url = "/endpoint_stop";
export var eventsource_action_clear_files_url = "/clear_action_files";
export var download_action_files_url = "/file_table_download";
export var action_folder_info_url = "/folder_info";



// Specific Endpoint Sets
function pageSpecificFunction() {
    var pageType = document.body.getAttribute('data-page-type');
    // console.log("pageType:", pageType);
    switch (pageType) {
        case 'log_collection':
            eventsource_source_url = '/log_collection_endpoint';
            eventsource_action_clear_logs_url = "/clear_Log_Collection_Log_Files";
            break;
        case 'cleanup':
            eventsource_source_url = '/cleanup_endpoint';
            eventsource_action_clear_logs_url = "";
            break;
        case 'fqdn':
            eventsource_source_url = '/fqdn_endpoint';
            eventsource_action_clear_logs_url = "";
            break;
        case 'backup':
            eventsource_source_url = '/backup_endpoint';
            eventsource_action_clear_logs_url = "";
            break;
        default:
            terminal_source_url = '/not-found';
            eventsource_source_url = '/not-found';
            terminal_log_download_source_url = '/not-found';
            eventsource_action_clear_logs_url = "";
            endpoint_stop_url = "/not-found";
            break;
    }
}

pageSpecificFunction()
// document.addEventListener('DOMContentLoaded', pageSpecificFunction);

