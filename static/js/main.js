document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (event) => {
    const targetId = anchor.getAttribute('href');
    if (targetId === '#') return;

    const target = document.querySelector(targetId);
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Billedgalleri på single-page: thumbnail-skift + fuldskærms-lightbox
const gallery = document.querySelector('[data-gallery]');
if (gallery) {
  const images = JSON.parse(gallery.dataset.images || '[]');
  const mainImage = gallery.querySelector('[data-gallery-main]');
  const thumbs = gallery.querySelectorAll('[data-gallery-thumb]');
  const lightbox = document.querySelector('[data-lightbox]');
  const lightboxImage = lightbox.querySelector('[data-lightbox-image]');
  let currentIndex = 0;

  const setActiveThumb = (index) => {
    thumbs.forEach((thumb) => {
      thumb.classList.toggle('gallery__thumb--active', Number(thumb.dataset.index) === index);
    });
  };

  const showImage = (index) => {
    currentIndex = (index + images.length) % images.length;
    mainImage.src = images[currentIndex];
    setActiveThumb(currentIndex);
  };

  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', () => showImage(Number(thumb.dataset.index)));
  });

  const openLightbox = () => {
    lightboxImage.src = images[currentIndex];
    lightbox.hidden = false;
  };

  const closeLightbox = () => {
    lightbox.hidden = true;
  };

  const showLightboxImage = (index) => {
    showImage(index);
    lightboxImage.src = images[currentIndex];
  };

  gallery.querySelector('[data-gallery-open]').addEventListener('click', openLightbox);
  lightbox.querySelector('[data-lightbox-close]').addEventListener('click', closeLightbox);
  lightbox.querySelector('[data-lightbox-prev]').addEventListener('click', () => showLightboxImage(currentIndex - 1));
  lightbox.querySelector('[data-lightbox-next]').addEventListener('click', () => showLightboxImage(currentIndex + 1));

  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });

  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') showLightboxImage(currentIndex - 1);
    if (event.key === 'ArrowRight') showLightboxImage(currentIndex + 1);
  });
}
