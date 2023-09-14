// Specific Endpoints
export var endpoint_action_url = "";
export var endpoint_action_clear_logs_url = "";
export var endpoint_action_2_url = "";

// General Endpoints
export var terminal_log_download_source_url = "/download_terminal_log";
window.terminal_log_download_source_url = terminal_log_download_source_url;

export var notification_source_url = "/notification_endpoint";
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
            endpoint_action_url = '/log_collection_endpoint';
            endpoint_action_clear_logs_url = "/clear_Log_Collection_Log_Files";
            endpoint_action_2_url = "";
            break;
        case 'cleanup':
            endpoint_action_url = '/cleanup_endpoint';
            endpoint_action_clear_logs_url = "";
            endpoint_action_2_url = "";
            break;
        case 'fqdn':
            endpoint_action_url = '/fqdn_endpoint';
            endpoint_action_clear_logs_url = "";
            endpoint_action_2_url = "";
            break;
        case 'backup':
            endpoint_action_url = '/backup_endpoint';
            endpoint_action_clear_logs_url = "";
            endpoint_action_2_url = "/backup_control_endpoint";
            break;
        case 'restore':
            endpoint_action_url = '/restore_endpoint';
            endpoint_action_clear_logs_url = "";
            endpoint_action_2_url = "/restore_control_endpoint";
            break;
        default:
            terminal_source_url = '/not-found';
            endpoint_action_url = '/not-found';
            terminal_log_download_source_url = '/not-found';
            endpoint_action_clear_logs_url = "";
            endpoint_stop_url = "/not-found";
            endpoint_action_2_url = "/not-found";
            break;
    }
}

pageSpecificFunction()
// document.addEventListener('DOMContentLoaded', pageSpecificFunction);

