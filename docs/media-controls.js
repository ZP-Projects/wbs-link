/* Explicit playback uses a user gesture; no muted autoplay or hidden volume control. */
document.querySelectorAll('.sound-play').forEach(button => {
  const section = button.closest('section');
  const video = section.querySelector('video');
  const status = section.querySelector('.playback-note');
  button.addEventListener('click', async () => {
    video.muted = false;
    // Honor an existing audible player volume on resume; explicit Play restores zero volume.
    if (video.volume === 0) video.volume = 1;
    try {
      await video.play();
      status.textContent = 'Playing with sound. Use the player to pause, adjust volume or enable captions.';
    } catch {
      status.textContent = 'Playback did not start. Use the player controls to try again.';
    }
  });
});
