const onStart = () => {
  document.getElementById("loadData").addEventListener(
    "click",
    () => {
      var e = document.getElementById("buildIdSelect");
      var value = e.options[e.selectedIndex].value;

      if (value.includes("Build..")) {
        return;
      }

      chrome.runtime.sendMessage(
        { message: "init", activeBuild: value },
        response => {
          chrome.storage.sync.set({ isActive: true, activeBuild: value });
        }
      );
    },
    false
  );
};

const onDisable = () => {
  document.getElementById("disable").addEventListener(
    "click",
    () => {
      chrome.storage.sync.set({ isActive: false });
    },
    false
  );
};

const onOptions = () => {
  document
    .querySelector("#go-to-options")
    .addEventListener("click", function() {
      // if (chrome.runtime.openOptionsPage) {
      //   chrome.runtime.openOptionsPage();
      // } else {
      //   window.open(chrome.runtime.getURL("options.html"));
      // }
      chrome.tabs.create({'url': chrome.extension.getURL('graph.html')}, function(tab) {
        // Tab opened.
      });
    });
};

const onLoad = () => {
  const selectList = document.getElementById("buildIdSelect");

  chrome.storage.sync.get(["koverj_url", "activeBuild"], result => {
    const req = new XMLHttpRequest();
    req.open("GET", `${result.koverj_url}/builds`, true);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send();

    req.onreadystatechange = function() {
      // Call a function when the state changes.
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        for (let [k, v] of Object.entries(JSON.parse(this.responseText))) {
          var option = document.createElement("option");
          option.value = v.id;
          option.text = v.id;
          selectList.appendChild(option);
        }
      }
      console.log(result);
      selectList.selectedIndex = result.activeBuild;
    };
  });
};



document.addEventListener("DOMContentLoaded", onLoad, false);
document.addEventListener("DOMContentLoaded", onStart, false);
document.addEventListener("DOMContentLoaded", onDisable, false);
document.addEventListener("DOMContentLoaded", onOptions, false);
