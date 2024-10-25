console.log("Background script loaded");

chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
  chrome.storage.sync.set({ enabled: true, muted: true }, () => {
    console.log("Initial state set");
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Message received:", request);
  if (request.action === "getState") {
    chrome.storage.sync.get(["enabled", "muted"], (result) => {
      console.log("Sending state:", result);
      sendResponse(result);
    });
    return true; // Indicates an asynchronous response
  }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && tab.url.includes('youtube.com')) {
    console.log("YouTube tab updated, sending init message");
    chrome.tabs.sendMessage(tabId, { action: "init" }).catch(error => {
      console.log("Error sending init message:", error);
    });
  }
});

// Handle extension updates
chrome.runtime.onUpdateAvailable.addListener(() => {
  console.log("Update available, cleaning up tabs");
  chrome.tabs.query({url: "*://*.youtube.com/*"}, (tabs) => {
    tabs.forEach((tab) => {
      try {
        const port = chrome.tabs.connect(tab.id, {name: "cleanup"});
        port.disconnect();
      } catch (error) {
        console.log("Error during cleanup:", error);
      }
    });
  });
  chrome.runtime.reload();
});
