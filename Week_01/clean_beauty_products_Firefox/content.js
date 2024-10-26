function findElementById(root, id) {
  if (root.id === id) return root;
  for (let child of root.children) {
    const found = findElementById(child, id);
    if (found) return found;
  }
  return null;
}

function isCleanFilterApplied() {
  const activeFiltersContainer = document.querySelector('.active-filters-container');
  if (activeFiltersContainer) {
    const cleanFilterSpan = Array.from(activeFiltersContainer.querySelectorAll('span')).find(span => 
      span.textContent.trim().toLowerCase() === "clean"
    );
    return !!cleanFilterSpan;
  }
  return false;
}

function applyCleanFilter() {
  console.log("Attempting to apply Clean filter");

  // Find the Conscious div
  const consciousDiv = document.getElementById("Conscious");
  
  if (consciousDiv) {
    // Ensure the Conscious filter is expanded
    const filterDisp = consciousDiv.querySelector('.filter-disp');
    if (filterDisp && filterDisp.classList.contains('close')) {
      const filterTitle = consciousDiv.querySelector('.filter-title');
      if (filterTitle) {
        filterTitle.click();
        console.log("Expanded Conscious filter");
      }
    }
    
    // Find the Clean option
    const cleanOption = Array.from(consciousDiv.querySelectorAll('.filter-item')).find(item => 
      item.querySelector('.filter-item-value').textContent.trim().toLowerCase() === "clean"
    );
    
    if (cleanOption) {
      const checkbox = cleanOption.querySelector('.filter-checkbox');
      if (checkbox) {
        checkbox.click();
        console.log("Clicked Clean filter checkbox");
      } else {
        console.log("Clean filter checkbox not found");
      }
    } else {
      console.log("Clean filter option not found");
    }
  } else {
    console.log("Conscious filter not found");
  }
}

function checkAndApplyCleanFilter() {
  if (!isCleanFilterApplied()) {
    applyCleanFilter();
  } else {
    console.log("Clean filter is already applied");
  }
}

function periodicCheck() {
  browser.storage.sync.get('enabled').then(data => {
    if (data.enabled) {
      checkAndApplyCleanFilter();
    }
  }).catch(error => {
    console.error("Error getting extension state:", error);
  });
}

// Run the filter check when the page loads
setTimeout(periodicCheck, 2000);

// Listen for changes in the URL (e.g., when navigating between pages)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    setTimeout(periodicCheck, 2000);
  }
}).observe(document, {subtree: true, childList: true});

// Periodically check and apply the filter every 2 seconds
setInterval(periodicCheck, 2000);
