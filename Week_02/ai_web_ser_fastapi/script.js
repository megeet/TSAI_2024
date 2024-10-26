document.querySelectorAll('input[name="animal"]').forEach(radio => {
    radio.addEventListener('change', showAnimalImage);
});

function showAnimalImage() {
    const selectedAnimal = document.querySelector('input[name="animal"]:checked').value;
    const animalImage = document.getElementById('animal-image');
    animalImage.innerHTML = `<img src="${selectedAnimal}.jpg" alt="${selectedAnimal}">`;
}

async function uploadFile() {
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('file-info').innerHTML = `
            <p>File Name: ${result.filename}</p>
            <p>File Size: ${result.size} bytes</p>
            <p>File Type: ${result.content_type}</p>
        `;
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    }
}

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    uploadFile();
});
