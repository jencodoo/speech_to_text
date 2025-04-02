async function uploadAudio() {
    let fileInput = document.getElementById("audioFile");
    if (fileInput.files.length === 0) {
        alert("Hãy chọn một file âm thanh!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        let data = await response.json();
        if (data.text) {
            document.getElementById("result").innerText = data.text;
        } else {
            alert("Có lỗi xảy ra!");
        }
    } catch (error) {
        console.error("Error during fetch:", error);
        alert("Đã xảy ra lỗi khi tải lên file âm thanh!");
    }
}
