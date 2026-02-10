document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('nav a');
  const current = (window.location.pathname.split('/').pop() || 'index.html');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === current || (href === 'index.html' && current === '')) {
      link.classList.add('active');
    }
  });

  const uploadForm = document.getElementById('uploadForm');
  if (!uploadForm) return;

  const fileInput = document.getElementById('fileInput');
  const uploadedImageContainer = document.getElementById('uploaded-image-container');
  const predictionResult = document.getElementById('prediction-result');

  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!fileInput || fileInput.files.length === 0) {
      predictionResult.textContent = 'Please select an image file.';
      predictionResult.classList.add('error');
      return;
    }

    const file = fileInput.files[0];
    const imageUrl = URL.createObjectURL(file);
    uploadedImageContainer.innerHTML = `<img src="${imageUrl}" alt="Uploaded Nail Image" style="max-width: 300px; max-height: 300px;">`;

    const formData = new FormData();
    formData.append('file', file);

    predictionResult.textContent = 'Predicting...';
    predictionResult.classList.remove('error');

    try {
      const response = await fetch('/predict', { method: 'POST', body: formData });
      const data = await response.json();

      if (data.error) {
        predictionResult.textContent = `Error: ${data.error}`;
        predictionResult.classList.add('error');
      } else {
        predictionResult.textContent = `Predicted Disease: ${data.disease_name} (Confidence: ${data.confidence}%)`;
        predictionResult.classList.remove('error');
      }
    } catch (err) {
      predictionResult.textContent = 'Failed to connect to the server.';
      predictionResult.classList.add('error');
    }
  });
});