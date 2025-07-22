const params = new URLSearchParams(window.location.search);
const taskId = params.get("id");
let url = `https://todoapi-3kjr.onrender.com/task-detail/${taskId}`;
let detail = document.querySelector(".detail");

const getDetail = async () => {
  let token = localStorage.getItem("authToken");
  let response = await fetch(url, {
    method: "GET",
    headers: {
      "Authorization": `Token ${token}`,
      "Content-Type": "application/json",
    },
  });

  let data = await response.json();
  const status = data.completed
    ? "<span class='completed'>✅ Task has been Completed.</span>"
    : "<span class='incomplete'>❌ Task has not been completed.</span>";

  detail.innerHTML = `
    <div class="info-box">
      <h2>Title</h2>
      <p>${data.title}</p>
    </div>
    <div class="info-box">
      <h2>Description</h2>
      <p>${data.description}</p>
    </div>
    <div class="info-box">
      <h2>Status</h2>
      <p>${status}</p>
    </div>
  `;
};

getDetail();
