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
        .then((result) => {
          handleScriptResult(result, status);
        })
        .catch((error) => {
          console.error("Error executing script:", error);
          status.textContent = "Error: " + error.message;
        });
    }
  } catch (err) {
    console.error(err);
    status.textContent = "Error" + err.message;
  }
});

function isFirefox() {
  return navigator.userAgent.includes("Firefox");
}

function handleScriptResult(result, status) {
	if (result && result[0]) {
	  const { url, title } = result[0];
	  chrome.runtime.sendMessage({ type: "download", m3u8URL: url, title });
	  status.textContent = "Downloading...";
	} else {
	  status.textContent = "No video found.";
	}
 }

function findM3U8() {
  const videos = Array.from(document.querySelectorAll("video, source"));
  for (const video of videos) {
    if (video.src && video.src.endsWith(".m3u8")) {
      return { url: video.src, title: document.title || "video" };
    }
  }
  return null;
}
