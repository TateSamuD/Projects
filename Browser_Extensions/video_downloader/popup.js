document.getElementById("download").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Searching for video...";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    if (isFirefox()) {
      // Firefox-compatible script execution (Manifest V2)
      chrome.tabs.executeScript(
        tab.id,
        { code: "(" + findM3U8.toString() + ")();" },
        (result) => {
          if (chrome.runtime.lastError) {
            console.error("Script Execution Error:", chrome.runtime.lastError);
            status.textContent = "Error executing script.";
            return;
          }
          handleScriptResult(result, status);
        }
      );
    } else {
      // Chrome/Edge-compatible script execution (Manifest V3)
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
    }
  } catch (err) {
    console.error("Error:", err);
    status.textContent = "Error: " + err.message;
  }
});

// Function to detect Firefox
function isFirefox() {
  return typeof browser !== "undefined";
}

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
