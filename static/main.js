"use strict";

function newTask(event) {
    // Clearing the form fields
    document.querySelector("[name='title']").value = "";
    document.querySelector("[name='due']").value = "";
    document.querySelector("[name='reminder']").value = "";
    document.querySelector("[name='created']").value = "";
    document.querySelector("[name='category']").value = "Homework";
    document.querySelector("[name='priority']").value = "1";
    document.querySelector("[name='status']").value = "Unstarted";
    document.querySelector("[name='notes']").value = "";
    document.querySelector("[name='id']").value = "";
    document.querySelector("[name='title']").value = "";
}

function newFolder(event) {
    let name = prompt("Name of new folder?")
    let userid = document.querySelector("[name='userid']").value;
    if (name.length > 0) {
        let f = new FormData();
        f.append("userid", userid);
        f.append("name", name);
        fetch("/new_folder", {
            "method": "POST",
            "body": f,
        }).then(response => response.text()).then(data => {
            console.log("newFolder reply: ",data);
            location.reload();
        });        
    }
}


document.querySelector("#new_task_button").addEventListener("click", newTask);
document.querySelector("#new_folder_button").addEventListener("click", newFolder);
