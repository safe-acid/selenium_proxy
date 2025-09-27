chrome.webRequest.onAuthRequired.addListener(
  function (details) {
    return {
      authCredentials: {
        username: "YzAsZc",
        password: "bUGAtU"
      }
    };
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
