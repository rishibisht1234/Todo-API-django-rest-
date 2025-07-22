// list.js

let taskList = document.querySelector(".taskList");
let formContainer = document.querySelector(".formContainer");
let createTask = document.querySelector(".createTask");
let searchInput = document.querySelector(".search");
let searchBtn = document.querySelector(".searchBtn");
let logoutBtn = document.querySelector(".logoutBtn");
let showAllBtn = document.querySelector(".showAllBtn");
showAllBtn.addEventListener("click", async () => {
    viewMode = "all";
    localStorage.setItem("viewMode", viewMode);
    await getList(); // fetch full list again
});

const url = "https://todoapi-3kjr.onrender.com/task-list/";
const urlc = "https://todoapi-3kjr.onrender.com/task-create/";
const outurl = "https://todoapi-3kjr.onrender.com/logout/";

let viewMode = localStorage.getItem("viewMode") || "all";
let cachedData = localStorage.getItem("cachedData");

const getList = async () => {
    let token = localStorage.getItem("authToken");
    let res = await fetch(url, {
        method: "GET",
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

    const data = await res.json();
    localStorage.setItem("cachedData", JSON.stringify(data));
    viewMode = "all";
    localStorage.setItem("viewMode", viewMode);
    renderTasks(data);
};

const renderTasks = (data) => {
    taskList.innerHTML = `
    <div class="task header">
        <div class="cell"><strong>Title</strong></div>
        <div class="cell"><strong>Status</strong></div>
        <div class="cell"><strong>Actions</strong></div>
    </div>`;

    data.forEach(task => {
        const taskElement = document.createElement("div");
        taskElement.classList.add("task");
        taskElement.dataset.id = String(task.id);

        const status = task.completed ? "✅ Task has been Completed." : "❌ Task has not been completed.";

        taskElement.innerHTML = `
        <div class="cell"><strong>${task.title}</strong></div>
        <div class="cell">${status}</div>
        <div class="cell">
            <button class="showDetails">Show Details</button>
            <button class="updateTask">Update Task</button>
            <button class="toggleBtn">Toggle Status</button>
            <button class="deleteBtn">Delete Task</button>
        </div>`;

        taskList.appendChild(taskElement);

        taskElement.querySelector(".showDetails").addEventListener("click", () => {
            window.location.href = `detail.html?id=${task.id}`;
        });

        taskElement.querySelector(".updateTask").addEventListener("click", () => showUpdateForm(task, taskElement));

        taskElement.querySelector(".deleteBtn").addEventListener("click", async () => {
            let token = localStorage.getItem("authToken");
            let res = await fetch(`https://todoapi-3kjr.onrender.com/task-delete/${task.id}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Token ${token}`
                }
            });
            if (res.ok) getList();
        });

        taskElement.querySelector(".toggleBtn").addEventListener("click", async () => {
            let token = localStorage.getItem("authToken");
            let res = await fetch(`https://todoapi-3kjr.onrender.com/task-toggle/${task.id}`, {
                method: "PUT",
                headers: {
                    "Authorization": `Token ${token}`,
                    "Content-Type": "application/json"
                }
            });
            if (res.ok) getList();
        });
    });
};

const showUpdateForm = (task, taskElement) => {
    viewMode = "update";
    localStorage.setItem("viewMode", viewMode);

    taskElement.innerHTML = `
    <form class="updateForm">
        <input class="editTitle" value="${task.title}" required><br>
        <textarea class="editDescription" required>${task.description}</textarea><br>
        <label><input type="checkbox" class="editCompleted" ${task.completed ? "checked" : ""}> Completed</label><br>
        <input type="datetime-local" class="editDeadline" value="${task.deadline.slice(0, 16)}" required><br>
        <button type="submit">Save Changes</button>
        <button type="button" class="cancelUpdate">Cancel</button>
    </form>`;

    taskElement.querySelector(".updateForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("authToken");

        const updatedData = {
            title: document.querySelector(".editTitle").value,
            description: document.querySelector(".editDescription").value,
            completed: document.querySelector(".editCompleted").checked,
            deadline: new Date(document.querySelector(".editDeadline").value).toISOString()
        };

        const res = await fetch(`https://todoapi-3kjr.onrender.com/task-update/${task.id}`, {
            method: "PUT",
            headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedData)
        });

        if (res.ok) {
            await getList();
        }
    });

    taskElement.querySelector(".cancelUpdate").addEventListener("click", () => {
        viewMode = "all";
        localStorage.setItem("viewMode", viewMode);
        getList();
    });
};

createTask.addEventListener("click", () => {
    viewMode = "create";
    localStorage.setItem("viewMode", viewMode);

    formContainer.innerHTML = `
        <h2>Create New Task</h2>
        <form class="taskForm">
            <input class="title" placeholder="Enter Title" required><br>
            <textarea class="description" placeholder="Enter Description" required></textarea><br>
            <input type="datetime-local" class="deadline" required><br>
            <button type="submit">Submit Task</button>
        </form>
        <button class="cancelBtn">Cancel</button>`;

    taskList.hidden = true;

    document.querySelector(".cancelBtn").addEventListener("click", () => {
        viewMode = "all";
        localStorage.setItem("viewMode", viewMode);
        formContainer.innerHTML = "";
        taskList.hidden = false;
        getList();
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

            if (res.status === 201) {
                viewMode = "all";
                localStorage.setItem("viewMode", viewMode);
                formContainer.innerHTML = "";
                taskList.hidden = false;
                await getList();
            } else {
                const error = await res.json();
                alert("Error creating task: " + JSON.stringify(error));
            }
        } catch (err) {
            alert("Network error: " + err.message);
        }
    });
});

const performSearch = async () => {
    let token = localStorage.getItem("authToken");
    let query = searchInput.value.trim();

    if (!query) return;

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
    viewMode = "search";
    localStorage.setItem("viewMode", viewMode);
    localStorage.setItem("cachedData", JSON.stringify(data));
    renderTasks(data);
};

searchBtn.addEventListener("click", performSearch);
searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        performSearch();
    }
});

logoutBtn.addEventListener("click", async () => {
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
            localStorage.removeItem("authToken");
            localStorage.removeItem("viewMode");
            localStorage.removeItem("cachedData");
            window.location.href = "index.html";
        } else {
            alert(data.detail || "Logout failed.");
        }
    } catch (error) {
        alert("Logout error: " + error.message);
    }
});

// Load based on view mode
if (viewMode !== "all" && cachedData) {
    renderTasks(JSON.parse(cachedData));
} else {
    getList();
}
