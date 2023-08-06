/*jslint browser: true*/
/*global $*/

function add_content(req) {
    var elem = document.getElementById("content");
    elem.innerHTML += req;
}

function replace_content(id, data) {
    var elem = document.getElementById(id);
    elem.outerHTML = data;
}

function get_rows(rows) {
    var fragment = "";
    rows.forEach(function (row) {
        var css_class = "hasNoProject";
        var task = row.title;
        var context = row.context;

        if (row.uuid !== null) {
            task = `<a href='things:///show?id=${row.uuid}' target='_blank'>${row.title}</a>`;
        }
        if (row.context_uuid !== null) {
            context = `<a href='things:///show?id=${row.context_uuid}' target='_blank'>` +
            `${row.context}</a>`;
        }
        if (row.context !== null) {
            css_class = "hasProject";
        } else {
            row.context = "No Context";
        }
        if (row.due !== null) {
            css_class = "hasDeadline";
        } else {
            row.due = "";
        }

        fragment += "<div class='box'>" + task +
                    "<div class='deadline'>" + row.due + "</div>" +
                    "<div class='area " + css_class + "'>" +
                    context + "</div>" +
                    "</div>";
        });
    return fragment;
}

function setup_html_column(cssclass, header, number) {
    return "<div class='column' id='"+header+"'>" +
               "  <div class=''>" +
               "     <h2 class='" + cssclass + "'>" + header +
               "         <span class='size'>" + number + "</span>" +
               "     </h2>";
}

function add(color, title, data) {
    var rows = JSON.parse(data.response);
    var fragment = setup_html_column(color, title, rows.length);
    fragment += get_rows(rows);
    fragment += "</div></div>";
    if (document.getElementById(title) !== null) {
        replace_content(title, fragment);
    } else {
        add_content(fragment);
    }
}

var makeRequest = function (url, method) {
    var request = new XMLHttpRequest();
    return new Promise(function (resolve, reject) {
        request.onreadystatechange = function () {
            if (request.readyState !== 4) {return;}
            if (request.status >= 200 && request.status < 300) {
                resolve(request);
            } else {
                reject({
                    status: request.status,
                    statusText: request.statusText
                });
            }
        };
        request.open(method || "GET", url, true);
        request.send();
    });
};

async function refresh() {
    await makeRequest("api/backlog").then(function (data) {add("color1", "Backlog", data);})
    await makeRequest("api/upcoming").then(function (data) {add("color5", "Upcoming", data);})
    await makeRequest("api/waiting").then(function (data) {add("color3", "Waiting", data);})
    await makeRequest("api/inbox").then(function (data) {add("color4", "Inbox", data);})
    await makeRequest("api/mit").then(function (data) {add("color2", "MIT", data);})
    await makeRequest("api/today").then(function (data) {add("color6", "Today", data);})
    await makeRequest("api/next").then(function (data) {add("color7", "Next", data);})
}

window.onfocus = refresh;
window.onload = refresh;
