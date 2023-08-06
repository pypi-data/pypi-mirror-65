const BACKEND_URL = "http://localhost:8086";

function save_options() {
  let url = document.getElementById("backend_url").value;

  if (!url) {
    url = BACKEND_URL;
  }

  chrome.storage.sync.set(
    {
      koverj_url: url
    },
    () => {
      // Update status to let user know options were saved.
      var status = document.getElementById("status");
      status.textContent = "Options saved.";
      setTimeout(function() {
        status.textContent = "";
      }, 750);
    }
  );
}

function restore_options() {
  chrome.storage.sync.get(["koverj_url"], items => {
    document.getElementById("backend_url").value = items.koverj_url;
  });
}
document.addEventListener("DOMContentLoaded", restore_options);

document.getElementById("save").addEventListener("click", save_options);
