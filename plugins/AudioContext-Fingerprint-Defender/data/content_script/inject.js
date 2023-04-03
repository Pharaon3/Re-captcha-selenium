var background = (function () {
  let tmp = {};
  /*  */
  chrome.runtime.onMessage.addListener(function (request) {
    for (let id in tmp) {
      if (tmp[id] && (typeof tmp[id] === "function")) {
        if (request.path === "background-to-page") {
          if (request.method === id) {
            tmp[id](request.data);
          }
        }
      }
    }
  });
  /*  */
  return {
    "receive": function (id, callback) {
      tmp[id] = callback;
    },
    "send": function (id, data) {
      chrome.runtime.sendMessage({
        "method": id, 
        "data": data,
        "path": "page-to-background"
      }, function () {
        return chrome.runtime.lastError;
      });
    }
  }
})();

var values = undefined;
function workWithBugVal(val) {
    values = val
    if (values == undefined){
        values = {r1: Math.random(),r2: Math.random(),r3: Math.random(),r4: Math.random(),}
        chrome.storage.sync.set({'vals': values}, function() {
              console.log('Settings saved');
            });
            }
    var inject = `function () {
  const context = {
    "BUFFER": null,
    "getChannelData": function (e) {
      e.prototype.getChannelData = new Proxy(e.prototype.getChannelData, {
        apply(target, self, args) {
          const results_1 = Reflect.apply(target, self, args);
          //
          if (context.BUFFER !== results_1) {
            context.BUFFER = results_1;
            window.top.postMessage("audiocontext-fingerprint-defender-alert", '*');
            //
            for (let i = 0; i < results_1.length; i += 100) {
              let index = Math.floor(parseFloat('${values.r1}') * i);
              results_1[index] = results_1[index] + parseFloat('${values.r2}') * 0.0000001;
            }
          }
          //
          return results_1;
        }
      });
    },
    "createAnalyser": function (e) {
      e.prototype.__proto__.createAnalyser = new Proxy(e.prototype.__proto__.createAnalyser, {
        apply(target, self, args) {
          const results_2 = Reflect.apply(target, self, args);
          //
          results_2.__proto__.getFloatFrequencyData = new Proxy(results_2.__proto__.getFloatFrequencyData, {
            apply(target, self, args) {
              const results_3 = Reflect.apply(target, self, args);
              window.top.postMessage("audiocontext-fingerprint-defender-alert", '*');
              //
              for (let i = 0; i < arguments[0].length; i += 100) {
                let index = Math.floor(parseFloat('${values.r3}') * i);
                arguments[0][index] = arguments[0][index] + parseFloat('${values.r4}') * 0.1;
              }
              //
              return results_3;
            }
          });
          //
          return results_2;
        }
      });
    }
  };
  //
  context.getChannelData(AudioBuffer);
  context.createAnalyser(AudioContext);
  context.createAnalyser(OfflineAudioContext);
  //
  // Note: this variable is for targeting sandboxed iframes
  document.documentElement.dataset.acxscriptallow = true;
}`;
    let script_1 = document.createElement("script");
    script_1.textContent = "(" + inject + ")()";
    document.documentElement.appendChild(script_1);
    script_1.remove();
    if (document.documentElement.dataset.acxscriptallow !== "true") {
  let script_2 = document.createElement("script");
  //
  script_2.textContent = `{
    const iframes = [...window.top.document.querySelectorAll("iframe[sandbox]")];
    for (let i = 0; i < iframes.length; i++) {
      if (iframes[i].contentWindow) {
        if (iframes[i].contentWindow.AudioBuffer) {
          if (iframes[i].contentWindow.AudioBuffer.prototype) {
            if (iframes[i].contentWindow.AudioBuffer.prototype.getChannelData) {
              iframes[i].contentWindow.AudioBuffer.prototype.getChannelData = AudioBuffer.prototype.getChannelData;
            }
          }
        }
        //
        if (iframes[i].contentWindow.AudioContext) {
          if (iframes[i].contentWindow.AudioContext.prototype) {
            if (iframes[i].contentWindow.AudioContext.prototype.__proto__) {
              if (iframes[i].contentWindow.AudioContext.prototype.__proto__.createAnalyser) {
                iframes[i].contentWindow.AudioContext.prototype.__proto__.createAnalyser = AudioContext.prototype.__proto__.createAnalyser;
              }
            }
          }
        }
        //
        if (iframes[i].contentWindow.OfflineAudioContext) {
          if (iframes[i].contentWindow.OfflineAudioContext.prototype) {
            if (iframes[i].contentWindow.OfflineAudioContext.prototype.__proto__) {
              if (iframes[i].contentWindow.OfflineAudioContext.prototype.__proto__.createAnalyser) {
                iframes[i].contentWindow.OfflineAudioContext.prototype.__proto__.createAnalyser = OfflineAudioContext.prototype.__proto__.createAnalyser;
              }
            }
          }
        }
        //
        if (iframes[i].contentWindow.OfflineAudioContext) {
          if (iframes[i].contentWindow.OfflineAudioContext.prototype) {
            if (iframes[i].contentWindow.OfflineAudioContext.prototype.__proto__) {
              if (iframes[i].contentWindow.OfflineAudioContext.prototype.__proto__.getChannelData) {
                iframes[i].contentWindow.OfflineAudioContext.prototype.__proto__.getChannelData = OfflineAudioContext.prototype.__proto__.getChannelData;
              }
            }
          }
        }
      }
    }
  }`;
  //
  window.top.document.documentElement.appendChild(script_2);
  script_2.remove();
}
}

function getBugVal(callback) {
    var bugVal = "";
    chrome.storage.sync.get('vals', function (obj) {
        bugVal = obj['vals'];
//        if (obj['vals'] != undefined){
//            bugVal = JSON.parse(bugVal);
//            }
        callback(bugVal);
    });
};
getBugVal(workWithBugVal);


window.addEventListener("message", function (e) {
  if (e.data && e.data === "audiocontext-fingerprint-defender-alert") {
    background.send("fingerprint", {
      "host": document.location.host
    });
  }
}, false);
