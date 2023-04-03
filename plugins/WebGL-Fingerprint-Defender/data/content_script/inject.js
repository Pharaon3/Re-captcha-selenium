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
    var random = {
      "value": function () {
        return Math.random();
      },
      "item": function (e) {
        let rand = e.length * random.value();
        return e[Math.floor(rand)];
      },
      "number": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          tmp.push(Math.pow(2, power[i]));
        }
        /*  */
        return random.item(tmp);
      },
      "int": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          let n = Math.pow(2, power[i]);
          tmp.push(new Int32Array([n, n]));
        }
        /*  */
        return random.item(tmp);
      },
      "float": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          let n = Math.pow(2, power[i]);
          tmp.push(new Float32Array([1, n]));
        }
        /*  */
        return random.item(tmp);
      }
    }
    values = val
    if (values == undefined){
        values = {  r1:random.value(), r2:random.value(), r3:random.number([14, 15]), r4:random.number([12, 13]),
                r5:random.number([14, 15]), r6:random.number([14, 15]), r7:random.int([13, 14, 15]),
                r8:random.number([1, 2, 3, 4]),r9:random.number([1, 2, 3, 4]),r10:random.number([1, 2, 3, 4]),
                r11:random.number([1, 2, 3, 4]),r12:random.number([1, 2, 3, 4]),r13:random.number([1, 2, 3, 4]),
                r14:random.number([1, 2, 3, 4]),r15:random.number([1, 2, 3, 4]),r16:random.number([4, 5, 6, 7, 8]),
                r17:random.number([10, 11, 12, 13]), r18:random.float([0, 10, 11, 12, 13]),r19:random.float([0, 10, 11, 12, 13]),
                r20:random.item(["Graphics", "HD Graphics", "Intel(R) HD Graphics"]), r21:random.item(["WebGL 1.0", "WebGL 1.0 (OpenGL)", "WebGL 1.0 (OpenGL Chromium)"]),
                r22:random.item(["WebGL", "WebGL GLSL", "WebGL GLSL ES", "WebGL GLSL ES (OpenGL Chromium"])}
        chrome.storage.sync.set({'vals': JSON.stringify(values)}, function() {
              console.log('Settings saved');
            });
            }
    var inject = `function () {
  let config = {
    "random": {
      "value": function () {
        return Math.random();
      },
      "item": function (e) {
        let rand = e.length * config.random.value();
        return e[Math.floor(rand)];
      },
      "number": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          tmp.push(Math.pow(2, power[i]));
        }
        /*  */
        return config.random.item(tmp);
      },
      "int": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          let n = Math.pow(2, power[i]);
          tmp.push(new Int32Array([n, n]));
        }
        /*  */
        return config.random.item(tmp);
      },
      "float": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          let n = Math.pow(2, power[i]);
          tmp.push(new Float32Array([1, n]));
        }
        /*  */
        return config.random.item(tmp);
      }
    },
    "spoof": {
      "webgl": {
        "buffer": function (target) {
          let proto = target.prototype ? target.prototype : target.__proto__;
          //
          proto.bufferData = new Proxy(proto.bufferData, {
            apply(target, self, args) {
              let index = Math.floor(parseFloat('${values.r1}') * args[1].length);
              let noise = args[1][index] !== undefined ? 0.1 * parseFloat('${values.r2}') * args[1][index] : 0;
              //
              args[1][index] = args[1][index] + noise;
              window.top.postMessage("webgl-fingerprint-defender-alert", '*');
              //
              return Reflect.apply(target, self, args);
            }
          });
        },
        "parameter": function (target) {
          let proto = target.prototype ? target.prototype : target.__proto__;
          //
          proto.getParameter = new Proxy(proto.getParameter, {
            apply(target, self, args) {
              window.top.postMessage("webgl-fingerprint-defender-alert", '*');
              //
              if (args[0] === 3415) return 0;
              else if (args[0] === 3414) return 24;
              else if (args[0] === 36348) return 30;
              else if (args[0] === 7936) return "WebKit";
              else if (args[0] === 37445) return "Google Inc. (Intel)";
              else if (args[0] === 7937) return "WebKit WebGL";
              else if (args[0] === 3379) return parseInt('${values.r3}');
              else if (args[0] === 36347) return parseInt('${values.r4}');
              else if (args[0] === 34076) return parseInt('${values.r5}');
              else if (args[0] === 34024) return parseInt('${values.r6}');
              else if (args[0] === 3386) {let a = '${values.r7}'.split(',');return new Int32Array([parseInt(a[0]), parseInt(a[1])]);}
              else if (args[0] === 3413) return parseInt('${values.r8}');
              else if (args[0] === 3412) return parseInt('${values.r9}');
              else if (args[0] === 3411) return parseInt('${values.r10}');
              else if (args[0] === 3410) return parseInt('${values.r11}');
              else if (args[0] === 34047) return parseInt('${values.r12}');
              else if (args[0] === 34930) return parseInt('${values.r13}');
              else if (args[0] === 34921) return parseInt('${values.r14}');
              else if (args[0] === 35660) return parseInt('${values.r15}');
              else if (args[0] === 35661) return parseInt('${values.r16}');
              else if (args[0] === 36349) return parseInt('${values.r17}');
              else if (args[0] === 33902) {let a = '${values.r7}'.split(',');return new Float32Array([parseInt(a[0]), parseInt(a[1])]);}
              else if (args[0] === 33901) {let a = '${values.r7}'.split(',');return new Float32Array([parseInt(a[0]), parseInt(a[1])]);}
              else if (args[0] === 37446) return "${values.r20}";
              else if (args[0] === 7938) return "${values.r21}";
              else if (args[0] === 35724) return "${values.r22}";
              //
              return Reflect.apply(target, self, args);
            }
          });
        }
      }
    }
  };
  //
  config.spoof.webgl.buffer(WebGLRenderingContext);
  config.spoof.webgl.buffer(WebGL2RenderingContext);
  config.spoof.webgl.parameter(WebGLRenderingContext);
  config.spoof.webgl.parameter(WebGL2RenderingContext);
  //
  // Note: this variable is for targeting sandboxed iframes
  document.documentElement.dataset.wgscriptallow = true;
}`;
    let script_1 = document.createElement("script");
    script_1.textContent = "(" + inject + ")()";
    document.documentElement.appendChild(script_1);
    script_1.remove();
    if (document.documentElement.dataset.wgscriptallow !== "true") {
  let script_2 = document.createElement("script");
  //
  script_2.textContent = `{
    const iframes = [...window.top.document.querySelectorAll("iframe[sandbox]")];
    for (let i = 0; i < iframes.length; i++) {
      if (iframes[i].contentWindow) {
        if (iframes[i].contentWindow.WebGLRenderingContext) {
          iframes[i].contentWindow.WebGLRenderingContext.prototype.bufferData = WebGLRenderingContext.prototype.bufferData;
          iframes[i].contentWindow.WebGLRenderingContext.prototype.getParameter = WebGLRenderingContext.prototype.getParameter;
        }
        //
        if (iframes[i].contentWindow.WebGL2RenderingContext) {
          iframes[i].contentWindow.WebGL2RenderingContext.prototype.bufferData = WebGL2RenderingContext.prototype.bufferData;
          iframes[i].contentWindow.WebGL2RenderingContext.prototype.getParameter = WebGL2RenderingContext.prototype.getParameter;
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
        if (obj['vals'] != undefined){
            bugVal = JSON.parse(bugVal);
            bugVal.r18 = bugVal.r18[0] +', ' + bugVal.r18[1];
            bugVal.r19 = bugVal.r19[0] +', ' + bugVal.r19[1];
            bugVal.r7 = bugVal.r7[0] +', ' + bugVal.r7[1];
            }
        callback(bugVal);
    });
};
getBugVal(workWithBugVal);


window.addEventListener("message", function (e) {
  if (e.data && e.data === "webgl-fingerprint-defender-alert") {
    background.send("fingerprint", {
      "host": document.location.host
    });
  }
}, false);
