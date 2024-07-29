const form = document.querySelector('#upload-form');
const imageFile = document.querySelector('#image-file');
const previewDiv = document.querySelector('#preview');

form.addEventListener('submit', (event) => {
  if (!imageFile.value) {
    event.preventDefault();
    imageFile.classList.add('is-invalid');
    previewDiv.style.display = 'none';
  } else {
    imageFile.classList.remove('is-invalid');
    previewImage();
  }
});

imageFile.addEventListener('change', () => {
  previewImage();
});

function previewImage() {
  const file = imageFile.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      const img = document.createElement('img');
      img.src = event.target.result;
      previewDiv.innerHTML = '';
      previewDiv.appendChild(img);
      previewDiv.style.display = 'block';
    }
    reader.readAsDataURL(file);
  } else {
    previewDiv.style.display = 'none';
  }
}