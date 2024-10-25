console.log("Ad Muter loaded");

function adMuter() {
  let isMuted = false;
  let adCount = 0;
  let lastAdState = false;
  let lastAdElementCount = 0;
  let consecutiveNoAdChecks = 0;
  const MAX_NO_AD_CHECKS = 30; // 30 seconds

  function isAdPlaying() {
    const adElements = document.querySelectorAll('.ad-showing, .ytp-ad-player-overlay, .video-ads');
    console.log("Ad elements found:", adElements.length);
    return adElements.length;
  }

  function muteVideo(mute) {
    const video = document.querySelector('video');
    if (video) {
      video.muted = mute;
      isMuted = mute;
      console.log(`Video ${mute ? 'muted' : 'unmuted'}`);
    }
  }

  function checkAndMuteAd() {
    const adElementCount = isAdPlaying();
    const adPlaying = adElementCount > 0;

    if (adPlaying && (!lastAdState || adElementCount !== lastAdElementCount)) {
      adCount++;
      consecutiveNoAdChecks = 0;
      console.log("New ad detected. Total ads seen:", adCount);
      muteVideo(true);
    } else if (!adPlaying) {
      if (lastAdState) {
        console.log("Ad ended. Unmuting content.");
        muteVideo(false);
      }
      consecutiveNoAdChecks++;
      if (consecutiveNoAdChecks === MAX_NO_AD_CHECKS) {
        console.log("No ads detected for 30 seconds. Ads might be blocked.");
        // Check for ad blockers
        const adBlockers = document.querySelectorAll('div[id^="ad-block"], div[id^="adblock"]');
        if (adBlockers.length > 0) {
          console.log("Potential ad blocker detected:", adBlockers);
        }
      }
    }

    lastAdState = adPlaying;
    lastAdElementCount = adElementCount;
  }

  setInterval(checkAndMuteAd, 1000);
}

// Check if we're on a YouTube page before executing the main code
if (window.location.hostname.includes('youtube.com')) {
  console.log("On YouTube, initializing ad muter");
  adMuter();
}
