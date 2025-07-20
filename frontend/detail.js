const params = new URLSearchParams(window.location.search);
const taskId = params.get("id");
let url=`https://todoapi-3kjr.onrender.com/task-detail/${taskId}`;
let detail=document.querySelector(".detail");
const getDetail= async()=>{
    let token=localStorage.getItem("authToken");
    let response=await fetch(url,{
        method:"GET",
        headers:{
            "Authorization":`Token ${token}`,
            "Content-Type":"application/json"
        }
    });
    let data=await response.json();
    const status = data.completed ? "✅ Task has been Completed." : "❌ Task has not been completed.";
    detail.innerHTML=`<h1>${data.title}</h1>
    <p>${data.description}</p>
    <p>${status}</p>`
}
getDetail();