const preview = document.getElementById("preview");
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");

if (fileInput) {
    // Add an event listener to handle file selection and drag-and-drop functionality
    fileInput.addEventListener("change", function () {
        preview.innerHTML = ""; // Clear previous preview
        const file = this.files[0];

        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.alt = "Image Preview";
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
}

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("hover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("hover");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("hover");
    const files = e.dataTransfer.files;

    if (files.length > 0) {
        fileInput.files = files;
        // Simulate a change event to trigger the file input's change handler
        // This is necessary to ensure the file input's change event is fired
        fileInput.dispatchEvent(new Event("change"));
        // Or trigger the form submission
        // This will submit the form and send the file to the server
        //document.getElementById("upload").submit();
    }
});

dropArea.addEventListener("click", () => {
    fileInput.click();
});
