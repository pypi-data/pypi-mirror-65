chrome.runtime.onInstalled.addListener(function() {
  const BACKEND_URL = "http://localhost:8086";

  chrome.storage.sync.set(
    {
      koverj_url: BACKEND_URL
    },
    () => {}
  );
});

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  chrome.storage.sync.get(["isActive", "activeBuild"], result => {
    if (result.isActive && changeInfo.status === "complete") {
        getData(tab.id, tab.url, result.activeBuild);
    }
  });
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (sender.tab && request.message != "init") {
    return;
  }

  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    const tab = tabs[0];
    getData(tab.id, tab.url, request.activeBuild);
  });

  sendResponse({ status: "loaded..." });
  return true;
});

const getData = (tabId, currentTabUrl, activeBuild) => {
  chrome.storage.sync.get(["koverj_url"], result => {
    const encodedUrl = encodeURIComponent(`${currentTabUrl}`);
    const req = new XMLHttpRequest();
    req.open(
      "GET",
      `${result.koverj_url}/locators?url=${encodedUrl}&buildId=${activeBuild}`,
      true
    );
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send();

    req.onreadystatechange = function() {
      // Call a function when the state changes.
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        saveToStorage(tabId, this.responseText);
        broadcast(tabId, { command: "init", activeBuild: activeBuild });
      }
    };
  });
};

const saveToStorage = (tabId, data) => {
  // chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  chrome.tabs.executeScript(tabId, {
    code: `localStorage.setItem("locators", ${JSON.stringify(data)});`
  });
  // });
};

const broadcast = (tabId, message) => {
  // chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
  chrome.tabs.sendMessage(tabId, message, () => {});
  // });
};
