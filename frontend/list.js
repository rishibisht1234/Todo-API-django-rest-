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
taskList.innerHTML = ""; 
 const data = await res.json();
  if (data.length === 0) {
            taskList.innerHTML = "<p>No tasks available.</p>";
            return;
        }
    
    data.forEach(task => {
                  let status = task.completed
                ? "✅ Task has been Completed."
                : "❌ Task has not been completed.";
        taskList.innerHTML+=`<h2>${task.title}</h2>
        <p>${task.description}</p>
        <p>${status}</p><br>`
    });
};
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
        taskList.style.display="none";
        document.querySelector(".cancelBtn").addEventListener("click", () => {
    formContainer.innerHTML = "";
    taskList.style.display="block";
});


       document.querySelector(".taskForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    let token = localStorage.getItem("authToken");
    let title = document.querySelector(".title").value;
    let description = document.querySelector(".description").value;
    let deadlineInput = document.querySelector(".deadline").value;
    let deadline = new Date(deadlineInput).toISOString();


    try {
        let res = await fetch(urlc, {
            method: "POST",
            headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title, description, deadline })
        });

       if (res.status === 201) {
    alert("Task created successfully!");
    formContainer.innerHTML = "";
    getList(); // ✅ Refresh list after successful creation
} else {
    const errorData = await res.json();
    alert("Error creating task:\n" + JSON.stringify(errorData, null, 2)); // ✅ Show real error
}
taskList.style.display="block";

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
            window.location.href = "/Todo-API-django-rest-/frontend/index.html";
        } else {
            alert(data.detail || "Logout failed.");
        }
    } catch (error) {
        console.error("Logout error:", error);
        alert("Something went wrong during logout.");
    }
});

