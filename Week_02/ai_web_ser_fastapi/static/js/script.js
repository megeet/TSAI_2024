document.querySelectorAll('input[name="animal"]').forEach(radio => {
    radio.addEventListener('change', showAnimalImage);
});

const animalImages = {
    cat: [
        { url: "https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554_1280.jpg", credit: "Pixabay, PublicDomainPictures" },
        { url: "https://cdn.pixabay.com/photo/2015/11/16/14/43/cat-1045782_1280.jpg", credit: "Pixabay, Alexas_Fotos" },
        { url: "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg", credit: "Pixabay, suju-foto" }
    ],
    dog: [
        { url: "https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_1280.jpg", credit: "Pixabay, huoadg5888" },
        { url: "https://cdn.pixabay.com/photo/2019/08/19/07/45/dog-4415649_1280.jpg", credit: "Pixabay, Alexas_Fotos" },
        { url: "https://cdn.pixabay.com/photo/2016/02/19/15/46/labrador-retriever-1210559_1280.jpg", credit: "Pixabay, Pezibear" }
    ],
    elephant: [
        { url: "https://cdn.pixabay.com/photo/2016/11/14/04/45/elephant-1822636_1280.jpg", credit: "Pixabay, Sponchia" },
        { url: "https://cdn.pixabay.com/photo/2013/05/17/07/12/elephant-111695_1280.jpg", credit: "Pixabay, skeeze" },
        { url: "https://cdn.pixabay.com/photo/2016/11/23/01/46/elephant-1852244_1280.jpg", credit: "Pixabay, Derks24" }
    ]
};

function getRandomImage(animal) {
    const images = animalImages[animal];
    return images[Math.floor(Math.random() * images.length)];
}

function handleImageError(img, animal) {
    console.error(`Failed to load image for ${animal}. Trying fallback.`);
    img.onerror = null; // Prevent infinite loop
    img.src = `https://via.placeholder.com/400x300?text=${animal.charAt(0).toUpperCase() + animal.slice(1)}`;
    document.getElementById('image-credit').innerHTML = '<p>Image: Not Available</p>';
}

function showAnimalImage() {
    const selectedAnimal = document.querySelector('input[name="animal"]:checked').value;
    const animalImage = document.getElementById('animal-image');
    const imageCredit = document.getElementById('image-credit');
    
    const image = getRandomImage(selectedAnimal);
    animalImage.innerHTML = `<img src="${image.url}" alt="${selectedAnimal}" onerror="handleImageError(this, '${selectedAnimal}')">`;
    imageCredit.innerHTML = `<p>Image: ${image.credit}</p>`;
}

async function uploadFile(file) {
    if (!file) {
        alert('Please select a file first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        const fileInfo = document.getElementById('file-info');
        fileInfo.innerHTML = `
            <p>File Name: ${result.filename}</p>
            <p>File Size: ${result.size} bytes</p>
            <p>File Type: ${result.content_type}</p>
        `;
        fileInfo.style.display = 'block'; // Show the file info
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    }
}

document.getElementById('file-upload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        uploadFile(file);
    }
});

// Hide file info on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('file-info').style.display = 'none';
});
