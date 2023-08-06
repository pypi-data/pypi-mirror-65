// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events',
    'base/js/utils',
], function(
    $,
    Jupyter,
    events, utils
) {
    "use strict";

    var rfanaltytics_domain = "log.refactored.ai";

    function send_event(eurl, params, name) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 201) {
                console.log('sent event: ' + name);
            }
        };
        xhttp.open("POST", eurl, true);
        xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhttp.send(params);
    }


    function notebook_visit(tid, username, url, path) {
        var url = encodeURIComponent(url);
        var path = encodeURIComponent(path);
        if (tid) {
            var params = "tid=" + tid + "&username=" + username + "&url=" + url + "&path=" + path;
        } else {
            var params = "username=" + username + "&url=" + url + "&path=" + path;
        }
        var eurl = "https://" + rfanaltytics_domain + "/log/notebook/event/notebookvisit";
        send_event(eurl, params, "notebookvisit");
    }

    function notebook_load(tid, username, url, path, load_time) {
        var url = encodeURIComponent(url);
        var path = encodeURIComponent(path);
        if (tid) {
            var params = "tid=" + tid + "&username=" + username + "&url=" + url + "&path=" + path + "&load_time=" + load_time;
        } else {
            var params = "username=" + username + "&url=" + url + "&path=" + path + "&load_time=" + load_time;
        }
        var eurl = "https://" + rfanaltytics_domain + "/log/notebook/event/notebookload";
        send_event(eurl, params, "notebookload");
    }

    function notebook_error(tid, username, url, path, error) {
        var url = encodeURIComponent(url);
        var path = encodeURIComponent(path);
        if (tid) {
            var params = "tid=" + tid + "&username=" + username + "&url=" + url + "&path=" + path + "&error=" + error;
        } else {
            var params = "username=" + username + "&url=" + url + "&path=" + path + "&error=" + error;
        }
        var eurl = "https://" + rfanaltytics_domain + "/log/notebook/event/notebookerror";
        send_event(eurl, params, "notebookerror");
    }

    function cell_execution(tid, username, url, path, cell_id) {
        var url = encodeURIComponent(url);
        var path = encodeURIComponent(path);
        if (tid) {
            var params = "tid=" + tid + "&username=" + username + "&url=" + url + "&path=" + path + "&cell_id=" + cell_id;
        } else {
            var params = "username=" + username + "&url=" + url + "&path=" + path + "&cell_id=" + cell_id;
        }
        var eurl = "https://" + rfanaltytics_domain + "/log/notebook/event/cellexecution";
        send_event(eurl, params, "cellexecution");
    }

    function cell_execution_result(tid, username, url, path, cell_id, result, is_error) {
        var url = encodeURIComponent(url);
        var path = encodeURIComponent(path);
        if (tid) {
            var params = "tid=" + tid + "&username=" + username + "&url=" + url + "&path=" + path +
                "&cell_id=" + cell_id + "&result=" + result + "&is_error=" + is_error;
        } else {
            var params = "username=" + username + "&url=" + url + "&path=" + path +
                "&cell_id=" + cell_id + "&result=" + result + "&is_error=" + is_error;
        }
        var eurl = "https://" + rfanaltytics_domain + "/log/notebook/event/cellexecutionresult";
        send_event(eurl, params, "cellexecutionresult");
    }

    function cell_paste(tid, username, url, path, cell_id, content) {
        var url = encodeURIComponent(url);
        var path = encodeURIComponent(path);
        if (tid) {
            var params = "tid=" + tid + "&username=" + username + "&url=" + url + "&path=" + path +
                "&cell_id=" + cell_id + "&content=" + content;
        } else {
            var params = "username=" + username + "&url=" + url + "&path=" + path +
                "&cell_id=" + cell_id + "&content=" + content;
        }
        var eurl = "https://" + rfanaltytics_domain + "/log/notebook/event/cellpaste";
        send_event(eurl, params, "cellpaste");
    }

    var track_events = function() {
        var tid = localStorage.getItem("tid");
        var username = /user\/([^/]+)/.exec(Jupyter.notebook.base_url)[1];
        var url = location.href;
        var path = Jupyter.notebook.notebook_path;


        // to track total time spent on notebook
        function send_ping() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    console.log('sent event: ping');
                }
            };
            var eurl = "https://" + rfanaltytics_domain + "/log/ping";
            if (tid) {
                eurl = eurl + "?tid=" + tid + "&username=" + username + "&url=" + url;
            } else {
                eurl = eurl + "?username=" + username + "&url=" + url;
            }
            xhttp.open("GET", eurl, true);
            xhttp.send();
        }
        send_ping();
        // every 10mins
        setInterval(send_ping, 600000);

        // notebook visit event
        notebook_visit(tid, username, url, path);

        // load time event
        var load_time = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
        notebook_load(tid, username, url, path, load_time);

        // notebook error event
        window.onerror = function(error, url, line) {
            var error = line + "\n" + error;
            notebook_error(tid, username, url, path, error);
        }

        // to track how many executions happened
        events.on('execute.CodeCell', function (e, d) {
            var i = Jupyter.notebook.find_cell_index(d.cell);
            var cell_id = d.cell['metadata']['cell_id']
            cell_execution(tid, username, url, path, cell_id);
        });

        // to track execution result
        events.on('finished_execute.CodeCell', function (e, d) {
            var cell_id = d.cell['metadata']['cell_id']
            var i = Jupyter.notebook.find_cell_index(d.cell);
            var is_error = '';
            var outputs = d.cell['output_area']['outputs'];
            if (outputs.length) {
                if (outputs[0]['output_type'] == 'error') {
                    is_error = true;
                } else {
                    is_error = false;
                }
            }
            // TODO: convert object into string and send
            var result = outputs.toString();
            cell_execution_result(tid, username, url, path, cell_id, result, is_error);
        });

        // to track paste event
        function paste_event() {
            var i = Jupyter.notebook.get_selected_index();
            var c = Jupyter.notebook.get_cell(i);
            var cell_id = c['metadata']['cell_id']
            // TODO get content
            var content = '';
            cell_execution_paste(tid, username, url, path, cell_id, content);
        }

        // set uuid and add paste event on cell elements.
        var cells = Jupyter.notebook.get_cells();
        for(var i=0; i<cells.length; i++) {
            cells[i].element.on("paste", paste_event);
        }
        events.on('create.Cell', function(e, d){
            var i = Jupyter.notebook.find_cell_index(d.cell);
            var cell = Jupyter.notebook.get_cell(i);
            cell.metadata['cell_id'] = utils.uuid();
            d.cell.element.on("paste", paste_event);
        });
    }

    var load_ipython_extension = function() {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            track_events();
        }
        events.on("notebook_loaded.Notebook", track_events);
    };

    return {
        load_ipython_extension : load_ipython_extension
    };
});
