document.addEventListener('DOMContentLoaded', function() {
  const toggleSwitch = document.getElementById('toggleSwitch');

  // Load the current state
  browser.storage.sync.get('enabled').then(data => {
    toggleSwitch.checked = data.enabled;
  }).catch(error => {
    console.error("Error loading extension state:", error);
  });

  // Save the state when toggled
  toggleSwitch.addEventListener('change', function() {
    browser.storage.sync.set({enabled: this.checked}).then(() => {
      console.log('Extension enabled:', this.checked);
    }).catch(error => {
      console.error("Error saving extension state:", error);
    });
  });
});
