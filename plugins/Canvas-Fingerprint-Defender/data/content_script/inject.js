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
var ran = '11111111111';
function workWithBugVal(val) {
    ran = val
    if (ran == undefined){
        ran = Math.random();
        chrome.storage.sync.set({'ran': ran}, function() {
              console.log('Settings saved');
            });
}
    var inject = `function () {
  const getImageData = CanvasRenderingContext2D.prototype.getImageData;
  //
  let noisify = function (canvas, context) {
    if (context) {
        let w = ${ran};
        w = w.toString();
        const ran = w.slice(2);
        let ran1 = ran;
      const shift = {
        'r': function(){if (ran1.length<2){ran1=ran}; let n = Math.floor(parseInt(ran1.slice(0,1))); ran1 = ran1.slice(1);return n;},
        'g': function(){if (ran1.length<2){ran1=ran}; let n = Math.floor(parseInt(ran1.slice(0,1))); ran1 = ran1.slice(1);return n;},
        'b': function(){if (ran1.length<2){ran1=ran}; let n = Math.floor(parseInt(ran1.slice(0,1))); ran1 = ran1.slice(1);return n;},
        'a': function(){if (ran1.length<2){ran1=ran}; let n = Math.floor(parseInt(ran1.slice(0,1))); ran1 = ran1.slice(1);return n;},
      };
//
      const width = canvas.width;
      const height = canvas.height;
      //
      if (width && height) {
        const imageData = getImageData.apply(context, [0, 0, width, height]);
        //
        for (let i = 0; i < height; i++) {
          for (let j = 0; j < width; j++) {
            const n = ((i * (width * 4)) + (j * 4));
            imageData.data[n + 0] = imageData.data[n + 0] + shift.r();
            imageData.data[n + 1] = imageData.data[n + 1] + shift.g();
            imageData.data[n + 2] = imageData.data[n + 2] + shift.b();
            imageData.data[n + 3] = imageData.data[n + 3] + shift.a();
          }
        }
        //
        window.top.postMessage("canvas-fingerprint-defender-alert", '*');
        context.putImageData(imageData, 0, 0);
      }
    }
  };
  //
  HTMLCanvasElement.prototype.toBlob = new Proxy(HTMLCanvasElement.prototype.toBlob, {
    apply(target, self, args) {
      noisify(self, self.getContext("2d"));
      //
      return Reflect.apply(target, self, args);
    }
  });
  //
  HTMLCanvasElement.prototype.toDataURL = new Proxy(HTMLCanvasElement.prototype.toDataURL, {
    apply(target, self, args) {
      noisify(self, self.getContext("2d"));
      //
      return Reflect.apply(target, self, args);
    }
  });
  //
  CanvasRenderingContext2D.prototype.getImageData = new Proxy(CanvasRenderingContext2D.prototype.getImageData, {
    apply(target, self, args) {
      noisify(self.canvas, self);
      //
      return Reflect.apply(target, self, args);
    }
  });
  // Note: this variable is for targeting sandboxed iframes
  document.documentElement.dataset.cbscriptallow = true;
}`;
    let script_1 = document.createElement("script");
    script_1.textContent = "(" + inject + ")()";
    document.documentElement.appendChild(script_1);
    script_1.remove();
    if (document.documentElement.dataset.cbscriptallow !== "true") {
  let script_2 = document.createElement("script");
  //
  script_2.textContent = `{
    const iframes = [...window.top.document.querySelectorAll("iframe[sandbox]")];
    for (let i = 0; i < iframes.length; i++) {
      if (iframes[i].contentWindow) {
        if (iframes[i].contentWindow.CanvasRenderingContext2D) {
          iframes[i].contentWindow.CanvasRenderingContext2D.prototype.getImageData = CanvasRenderingContext2D.prototype.getImageData;
        }
        //
        if (iframes[i].contentWindow.HTMLCanvasElement) {
          iframes[i].contentWindow.HTMLCanvasElement.prototype.toBlob = HTMLCanvasElement.prototype.toBlob;
          iframes[i].contentWindow.HTMLCanvasElement.prototype.toDataURL = HTMLCanvasElement.prototype.toDataURL;
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
    chrome.storage.sync.get('ran', function (obj) {
        bugVal = obj['ran'];
        callback(bugVal);
    });
};
getBugVal(workWithBugVal);

window.addEventListener("message", function (e) {
  if (e.data && e.data === "canvas-fingerprint-defender-alert") {
    background.send("fingerprint", {
      "host": document.location.host
    });
  }
}, false);