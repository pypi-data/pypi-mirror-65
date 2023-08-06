// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events',
    'notebook/js/auth0',
], function(
    $,
    Jupyter,
    events,
    auth0,
) {
    "use strict";
    // NOTE: all the functions should be idempotent, i.e on multiple load of same
    // function should have same behaviour
    
    var load = true;

    function set_logoutall() {
        var logoutall_url;
        if (window.location.origin === "https://dsin100days.refactored.ai") {
            logoutall_url = 'https://accounts.refactored.ai/logoutall?next=' + 'https://refactored.ai';
        } else if (window.location.origin === "https://stgdsin100days.refactored.ai"){
            logoutall_url = 'https://stgaccounts.refactored.ai/logoutall?next=' + 'https://stage.refactored.ai';
        }
        var hs = '<span id="logoutall_widget"><button style="color: #333; background-color: #fff; border-color: #ccc; margin-left: 10px;" class="btn btn-sm navbar-btn">Logout</button></span>'
        $('#login_widget').before(hs);
        $('#logoutall_widget').on('click', function () {
            window.location.href = logoutall_url;
        });
    }

    function load_functions() {
        if (load) {
            $('#login_widget').hide();
            set_logoutall();
            load = false;
        }
    }

    var load_extension = function() {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            load_functions();
        }
        events.on("notebook_loaded.Notebook", load_functions);
    };

    return {
        load_extension : load_extension
    };
});
