let taskList=document.querySelector(".taskList")
let formContainer=document.querySelector(".formContainer");
let url="https://todoapi-3kjr.onrender.com/task-list/";
let urlc="https://todoapi-3kjr.onrender.com/task-create/";
let createTask=document.querySelector(".createTask");
let getList = async()=>{
let token = localStorage.getItem("authToken");
let res = await fetch(url, {
    method:"GET",
    headers: {
        "Authorization": `Token ${token}`,
        "Content-Type": "application/json"
    }
});
    if (res.status === 401) {
        alert("Session expired. Please log in again.");
        localStorage.removeItem("authToken");
        window.location.href = "index.html";
        return;
    }
taskList.innerHTML = ""; 
 const data = await res.json();
  if (data.length === 0) {
            taskList.innerHTML = "<p>No tasks available.</p>";
            return;
        }
    
   data.forEach(task => {
    const taskElement = document.createElement("div");
    taskElement.classList.add("task");
   taskElement.dataset.id = String(task.id);
const taskId = String(taskElement.dataset.id);
    

    const status = task.completed ? "✅ Task has been Completed." : "❌ Task has not been completed.";
    taskElement.innerHTML = `
        <h2>${task.title}</h2>
        <p>${task.description}</p>
        <p>${status}</p><br>
        <button class="deleteBtn">Delete Task</button>
    `;

    // ✅ Attach delete listener
    const deleteBtn = taskElement.querySelector(".deleteBtn");
    deleteBtn.addEventListener("click", async () => {
           console.log("Deleting ID:", taskId, typeof taskId);
        let dres = await fetch(`https://todoapi-3kjr.onrender.com/task-delete/${taskId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Token ${localStorage.getItem("authToken")}`,
            }
        });

        if (dres.ok) {
            alert("Task deleted successfully.");
            await getList();
        } else {
            alert("Failed to delete task.");
        }
    });

    taskList.appendChild(taskElement);
});
}
    createTask.addEventListener("click",async()=>{
        // if (formContainer.innerHTML.trim() !== "") return; 
        formContainer.innerHTML=`<h2>Create New Task</h2>
        <form class="taskForm">
<input class="title" placeholder="Enter Title" required><br>
<textarea class="description" placeholder="Enter Description" required></textarea><br>
<input type="datetime-local" class="deadline" required><br>
<button type="submit">Submit Task</button>
</form>
        <button class="cancelBtn">Cancel</button>`;
        
        taskList.hidden=true;
        document.querySelector(".cancelBtn").addEventListener("click", () => {
    formContainer.innerHTML = "";
    taskList.hidden=false;
});


       document.querySelector(".taskForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    let token = localStorage.getItem("authToken");
    let title = document.querySelector(".title").value;
    let description = document.querySelector(".description").value;
    let deadlineInput = document.querySelector(".deadline").value;
    let deadline = new Date(deadlineInput).toISOString();
    if (!deadlineInput) {
    alert("Please provide a valid deadline.");
    return;
}



    try {
        let res = await fetch(urlc, {
            method: "POST",
            headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title, description, deadline })
        });
            if (res.status === 401) {
        alert("Session expired. Please log in again.");
        localStorage.removeItem("authToken");
        window.location.href = "index.html";
        return;
    }

       if (res.status === 201) {
    alert("Task created successfully!");
    formContainer.innerHTML = "";
    await getList(); // ✅ Refresh list after successful creation
} else {
    const errorData = await res.json();
    alert("Error creating task:\n" + JSON.stringify(errorData, null, 2)); // ✅ Show real error
}
taskList.hidden=false;

    } catch (err) {
        alert("Network or server error:\n" + err.message);
    }
});

    });



getList();


document.querySelector(".searchBtn").addEventListener("click", async () => {
    let token = localStorage.getItem("authToken");
    let query = document.querySelector(".search").value;

    if (!query.trim()) {
        alert("Please enter a search term");
        return;
    }

    let res = await fetch(`https://todoapi-3kjr.onrender.com/task-search/?q=${encodeURIComponent(query)}`, {
        headers: {
            "Authorization": `Token ${token}`
        }
    });
    if (res.status === 401) {
    alert("Session expired. Please log in again.");
    localStorage.removeItem("authToken");
    window.location.href = "index.html";
    return;
}

    let data = await res.json();
    taskList.innerHTML = "";

    if (data.length === 0) {
        taskList.innerHTML = "<p>No tasks found.</p>";
        return;
    }

    data.forEach(task => {
        let status = task.completed ? "✅ Completed" : "❌ Not completed";
        taskList.innerHTML += `
            <h2>${task.title}</h2>
            <p>${task.description}</p>
            <p>${status}</p><br>`;
    });
});
const outurl = "https://todoapi-3kjr.onrender.com/logout/";

document.querySelector(".logoutBtn").addEventListener("click", async () => {
    const token = localStorage.getItem("authToken");

    try {
        const response = await fetch(outurl, {
            method: "POST",
            headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message || "Logged out successfully.");
            localStorage.removeItem("authToken"); // remove token from localStorage
            window.location.href = "index.html";
        } else {
            alert(data.detail || "Logout failed.");
        }
    } catch (error) {
        console.error("Logout error:", error);
        alert("Something went wrong during logout.");
    }
});

