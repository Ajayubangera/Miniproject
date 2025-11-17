document.addEventListener("DOMContentLoaded", () => {

    const videoInput = document.getElementById("videoInput");
    const uploadBtn = document.getElementById("uploadBtn");
    const alertBox = document.getElementById("alert");

    uploadBtn.addEventListener("click", async () => {

        if (!videoInput.files.length) {
            alertBox.innerText = "❌ Please select a video!";
            return;
        }

        const formData = new FormData();
        formData.append("video", videoInput.files[0]);

        alertBox.innerText = "⏳ Uploading...";

        const res = await fetch("/upload_video", {
            method: "POST",
            body: formData,
        });

        const data = await res.json();

        if (data.error) {
            alertBox.innerText = "❌ " + data.error;
            return;
        }

        localStorage.setItem("facesData", JSON.stringify(data.faces));

        window.location.href = "/results.html";
    });
});
