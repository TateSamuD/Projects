document.getElementById("download").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Searching for video...";
  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        func: findM3U8,
      },
      async (result) => {
        if (result && result[0]?.result) {
          const {url, title} = result[0].result;
          await chrome.runtime.sendMessage({ type: "download", m3u8URL: url, title });
          status.textContent = "Downloading";
        } else {
          status.textContent = "No video found";
        }
      }
    );
  } catch (err) {
    console.error(err);
    status.textContent = "Error" + err.message;
  }
});

function findM3U8() {
  const videos = Array.from(document.querySelectorAll("video, source"));
  for (const video of videos) {
    if (video.src && video.src.endsWith(".m3u8")) {
      return {url: video.src, title: document.title || "video"};
    }
  }
  return null;
}
