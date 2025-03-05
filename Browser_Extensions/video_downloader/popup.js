document.getElementById("download").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Searching for video...";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    if (typeof chrome.scripting !== "undefined") {
      // Chrome (Manifest V3)
      chrome.scripting
        .executeScript({
          target: { tabId: tab.id },
          func: findM3U8,
        })
        .then((injectionResults) => {
          if (
            !injectionResults ||
            !injectionResults[0] ||
            !injectionResults[0].result
          ) {
            status.textContent = "No video found.";
            return;
          }
          handleScriptResult([injectionResults[0].result], status);
        })
        .catch((error) => {
          console.error("Error executing script:", error);
          status.textContent = "Error: " + error.message;
        });
    } else {
      // If `chrome.scripting` is undefined, show error
      console.error("chrome.scripting API is not available.");
      status.textContent = "Error: chrome.scripting API not supported.";
    }
  } catch (err) {
    console.error("Error:", err);
    status.textContent = "Error: " + err.message;
  }
});

// Function to process results
function handleScriptResult(result, status) {
  if (result && result[0]) {
    const { url, title } = result[0];
    if (!url) {
      status.textContent = "No video found.";
      return;
    }
    chrome.runtime.sendMessage({ type: "download", m3u8URL: url, title });
    status.textContent = "Downloading...";
  } else {
    status.textContent = "No video found.";
  }
}

// Function to find m3u8 videos
function findM3U8() {
  const videos = Array.from(document.querySelectorAll("video, source"));
  for (const video of videos) {
    if (video.src && video.src.endsWith(".m3u8")) {
      return { url: video.src, title: document.title || "video" };
    }
  }
  return { url: null, title: null };
}
