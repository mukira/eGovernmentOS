// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
    chrome.tabs.create({
        url: 'src/popup.html'
    });
});
