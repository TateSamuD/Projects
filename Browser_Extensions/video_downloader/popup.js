document.getElementById("download").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Searching for video...";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    // Send message to background.js to execute the script
    chrome.runtime.sendMessage(
      { action: "findM3U8", tabId: tab.id },
      (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error:", chrome.runtime.lastError);
          status.textContent = "Error: " + chrome.runtime.lastError.message;
          return;
        }
        if (response && response.url) {
          chrome.runtime.sendMessage({
            type: "download",
            m3u8URL: response.url,
            title: response.title,
          });
          status.textContent = "Downloading...";
        } else {
          status.textContent = "No video found.";
        }
      }
    );
  } catch (err) {
    console.error("Error:", err);
    status.textContent = "Error: " + err.message;
  }
});
