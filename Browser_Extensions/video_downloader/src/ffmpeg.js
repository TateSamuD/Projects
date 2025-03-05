import { createFFmpeg, fetchFile } from "@ffmpeg/ffmpeg";

export const ffmpeg = createFFmpeg({ log: true });

export async function loadFFmpeg() {
  await ffmpeg.load();
}

export async function convertToMP4(tsFiles, title) {
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
