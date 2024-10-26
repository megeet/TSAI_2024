document.addEventListener('DOMContentLoaded', function() {
    const animalSelector = document.querySelector('.animal-selector');
    const animalImage = document.getElementById('animal-image');
    const fileUpload = document.getElementById('file-upload');
    const fileInfo = document.getElementById('file-info');

    animalSelector.addEventListener('change', function(event) {
        const selectedAnimal = event.target.value;
        if (selectedAnimal) {
            fetch(`/api/animal/${selectedAnimal}`)
                .then(response => response.json())
                .then(data => {
                    if (data.image_url) {
                        animalImage.innerHTML = `<img src="${data.image_url}" alt="${selectedAnimal}" class="animal-fade-in">`;
                        // Trigger reflow to restart animation
                        void animalImage.offsetWidth;
                        animalImage.querySelector('img').classList.add('animal-fade-in');
                    } else {
                        animalImage.innerHTML = '<p>Error loading image</p>';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    animalImage.innerHTML = '<p>Error loading image</p>';
                });
        }
    });

    fileUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/api/file-info', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const sizeInKB = (data.size / 1024).toFixed(2);
                fileInfo.innerHTML = `
                    <p>File Name: ${data.name}</p>
                    <p>File Size: ${sizeInKB} KB</p>
                    <p>File Type: ${data.type}</p>
                `;
                fileInfo.classList.remove('hidden');
            })
            .catch(error => {
                console.error('Error:', error);
                fileInfo.innerHTML = '<p>Error processing file</p>';
                fileInfo.classList.remove('hidden');
            });
        } else {
            fileInfo.innerHTML = '';
            fileInfo.classList.add('hidden');
        }
    });
});
