chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type == "download") {
    const m3u8_url = message.m3u8URL; // Corrected the key for m3u8 URL
    try {
      const tsFiles = await fetchM3U8(m3u8_url);
      const mp4_url = await convertToMP4(tsFiles, message.title);
      chrome.downloads.download({
        url: mp4_url,
        filename: message.title + ".mp4",
      });
      sendResponse({ success: true });
    } catch (error) {
      console.error(error);
      sendResponse({ success: false, error: error.message });
    }
  }
  return true;
});

// Fetch .ts files from the .m3u8 playlist
async function fetchM3U8(url) {
  const response = await fetch(url);
  const text = await response.text();
  // Filter out non-TS file URLs and return an array of full TS file URLs
  return text
    .split("\n")
    .filter((line) => !line.startsWith("#"))
    .map((ts) => new URL(ts, url).toString());
}

// Convert the fetched .ts files to a .mp4 file using FFmpeg
async function convertToMP4(tsFiles, title) {
  const { createFFmpeg, fetchFile } = FFmpeg;
  const ffmpeg = createFFmpeg({ log: true });
  await ffmpeg.load();

  // Write the TS files to the virtual filesystem
  for (let i = 0; i < tsFiles.length; i++) {
    const tsFile = tsFiles[i];
    const tsData = await fetchFile(tsFile).then((res) => res.arrayBuffer());
    ffmpeg.FS("writeFile", `segment${i}.ts`, new Uint8Array(tsData));
  }

  // Run FFmpeg to concatenate the segments into a single MP4 file
  await ffmpeg.run(
    "-i",
    `concat:${tsFiles.map((_, i) => `segment${i}.ts`).join("|")}`,
    "-c",
    "copy",
    `${title}.mp4`
  );

  // Read the resulting MP4 file from FFmpeg's virtual filesystem
  const data = ffmpeg.FS("readFile", `${title}.mp4`);

  // Create a Blob from the data and generate a URL for downloading
  return URL.createObjectURL(new Blob([data.buffer], { type: "video/mp4" }));
}
