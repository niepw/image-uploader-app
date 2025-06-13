const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("fileInput");

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("hover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("hover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("hover");
    const files = e.dataTransfer.files;

    if (files.length > 0) {
        fileInput.files = files;
        document.getElementById("upload-form").submit();
    }
});

dropZone.addEventListener("click", () => {
    fileInput.click();
});
