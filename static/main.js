"use strict";

function newTask(e) {
    // Clear the form fields
    document.querySelector("[name='title']").value = "";
    document.querySelector("[name='due']").value = "";
    document.querySelector("[name='reminder']").value = "";
    document.querySelector("[name='created']").value = "";
    document.querySelector("[name='category']").value = "Homework";
    document.querySelector("[name='priority']").value = "1";
    document.querySelector("[name='status']").value = "Unstarted";
    document.querySelector("[name='notes']").value = "";
    document.querySelector("[name='id']").value = "";
}

function newFolder(e) {
    let name = prompt("Name of new folder?");
    let userid = document.querySelector("[name='userid']").value;
    if (name.length > 0) {
        let f = new FormData();
        f.append("userid", userid);
        f.append("name", name);
        fetch("/new_folder", {
            "method": "POST",
            "body": f,
        }).then(response => response.text())
        .then(data => {
            console.log("newFolder reply: ",data)
            location.reload();
        });
    }
}

function logout(e) {
    document.location = "/logout";
}

// id="new_task_button"
document.querySelector("#new_task_button").addEventListener("click", newTask);
// id="new_folder_button"
document.querySelector("#new_folder_button").addEventListener("click", newFolder);
// id="logout_button"
document.querySelector("#logout_button").addEventListener("click", logout);
