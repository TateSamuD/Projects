chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
	if (message.type == "download") {
		const m3u8_url = message.m3u8_url;
		try {
			const tsFiles = await fetchM3U8(m3u8_url);
			const mp4_url = await convertToMP4(tsFiles);
			chrome.downloads.download({ url: mp4_url, filename: message.title + ".mp4" });
			sendResponse({ success: true });
		} catch (error){
			console.error(error);
			sendResponse({ success: false, error: error.message});
		}}
});

async function fetchM3U8(url){
	const response = await fetch(url);
	const text = await response.text();
	return text.split("\n").filter(line => !line.startsWith('#')).map(ts => new URL(ts, url).toString());
}

async function convertToMP4(tsFiles){
	const {createFFmpeg, fetchFile} = FFmpeg;
	const ffmpeg = createFFmpeg({ log: true });
	await ffmpeg.load();
	for (let i = 0; i < tsFiles.length; i++){
		const tsFile = tsFiles[i];
		const tsData = await fetchFile(tsFile).then(res => res.arrayBuffer());
		ffmpeg.FS("writeFile", `file${i}.ts`, new Uint8Array(tsData));
	}
	await ffmpeg.run('-i', 'concat:' + tsFiles.map((_, i) => `segment${i}.ts`).join('|'), '-c', 'copy', message.title + ".mp4");
	const data = ffmpeg.FS("readFile", message.title + ".mp4");
	return URL.createObjectURL(new Blob([data.buffer], { type: "video/mp4" }));
}