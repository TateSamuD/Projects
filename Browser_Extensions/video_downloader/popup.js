document.getElementById("download").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Downloading...";
  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    chrome.scripting.executeScript(
      {
        target: { tabID: tab.id },
        function: findM3U8,
      },
      async (result) => {
        if (result && result[0]?.result) {
          const m3u8URL = result[0].result;
          await chrome.runtime.sendMessage({ type: "download", m3u8URL });
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
    if (video.scroll.endsWith(".m3u8")) {
      return video.src;
    }
  }
  return null;
}
