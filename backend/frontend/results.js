const facesContainer = document.getElementById("faces-container");
const alertBox = document.getElementById("alert");

const faces = JSON.parse(localStorage.getItem("facesData") || "[]");

// Display detected faces
faces.forEach(face => {
    const div = document.createElement("div");
    div.className = "face-card";

    const img = document.createElement("img");
    img.src = face.thumb;
    img.className = "face-thumb";

    const p = document.createElement("p");
    p.textContent = `ID: ${face.track_id}`;

    const btn = document.createElement("button");
    btn.textContent = "Frontalize";
    btn.onclick = () => frontalizeFace(face.track_id);

    div.appendChild(img);
    div.appendChild(p);
    div.appendChild(btn);

    facesContainer.appendChild(div);
});


async function frontalizeFace(track_id) {
    alertBox.innerText = "⏳ Frontalizing...";

    const fd = new FormData();
    fd.append("track_id", track_id);

    let res;
    try {
        res = await fetch("http://127.0.0.1:8000/frontalize", {
            method: "POST",
            body: fd,
        });
    } catch (err) {
        alertBox.innerText = "❌ Cannot reach backend.";
        return;
    }

    let data;
    try {
        data = await res.json();
    } catch (e) {
        alertBox.innerText = "❌ Backend returned invalid JSON.";
        return;
    }

    console.log("Backend Response:", data);

    // Store results
    localStorage.setItem("matchedPerson", data.match || "Unknown");
    localStorage.setItem("frontalizedImg", data.frontalized_image || "null");

    // Send user to result page
    window.location.href = "/frontend.html";
}
