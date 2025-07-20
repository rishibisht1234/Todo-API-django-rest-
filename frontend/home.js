let loginButton=document.querySelector(".loginButton");
let usernameInput=document.querySelector(".username");
let passwordInput=document.querySelector(".password");
loginButton.addEventListener("click",async (e)=>{
    e.preventDefault();
    const username = usernameInput.value.trim();
    const password = passwordInput.value;
      if (!username || !password) {
    alert("Please enter both username and password");
    return;
  }
  let url="https://todoapi-3kjr.onrender.com/login/";
let options={
    "method":"POST",
     headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ username, password })
}
try{
let res=await fetch(url,options);

    if (!res.ok) {
      const errorData = await res.json();
      alert("Login failed: " + (errorData.detail || res.status));
      return;
    }

    const data = await res.json();
    const token = data.token;
    

  localStorage.setItem("authToken", token);
  localStorage.setItem("username", data.username);


     window.location.href="list.html";
}catch (error) {
    console.error("Login error:", error);
    alert("Something went wrong. Check console.");
  }
});