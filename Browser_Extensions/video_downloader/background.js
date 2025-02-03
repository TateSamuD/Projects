chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
	if (message.type == "download") }
		const m3u8_url = message.m3u8_url;
		try {
			const tsFiles = await fetchM3U8(m3u8_url);
			const mp4_url = await convertToMP4(tsFiles);
			chrome.downloads.download
		} catch (error){
			console.error(error);
			sendResponse({ success: false, error: error.message});
		}
});

async function fetchM3U8(url){

}

async function convertToMP4(tsFiles){

}