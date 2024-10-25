document.addEventListener('DOMContentLoaded', () => {
  const toggleEnabledBtn = document.getElementById('toggleEnabled');
  const toggleMuteBtn = document.getElementById('toggleMute');

  chrome.storage.sync.get(['enabled', 'muted'], (result) => {
    toggleEnabledBtn.textContent = result.enabled ? 'Disable' : 'Enable';
    toggleMuteBtn.textContent = result.muted ? 'Unmute Ads' : 'Mute Ads';
  });

  toggleEnabledBtn.addEventListener('click', () => {
    chrome.storage.sync.get('enabled', (result) => {
      const newEnabled = !result.enabled;
      chrome.storage.sync.set({ enabled: newEnabled });
      toggleEnabledBtn.textContent = newEnabled ? 'Disable' : 'Enable';
    });
  });

  toggleMuteBtn.addEventListener('click', () => {
    chrome.storage.sync.get('muted', (result) => {
      const newMuted = !result.muted;
      chrome.storage.sync.set({ muted: newMuted });
      toggleMuteBtn.textContent = newMuted ? 'Unmute Ads' : 'Mute Ads';
    });
  });
});
