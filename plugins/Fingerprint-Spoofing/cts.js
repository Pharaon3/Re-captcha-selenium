! function(t) {
    var e = {};

    function n(r) {
        if (e[r]) return e[r].exports;
        var o = e[r] = {
            i: r,
            l: !1,
            exports: {}
        };
        return t[r].call(o.exports, o, o.exports, n), o.l = !0, o.exports
    }
    n.m = t, n.c = e, n.d = function(t, e, r) {
        n.o(t, e) || Object.defineProperty(t, e, {
            enumerable: !0,
            get: r
        })
    }, n.r = function(t) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(t, "__esModule", {
            value: !0
        })
    }, n.t = function(t, e) {
        if (1 & e && (t = n(t)), 8 & e) return t;
        if (4 & e && "object" == typeof t && t && t.__esModule) return t;
        var r = Object.create(null);
        if (n.r(r), Object.defineProperty(r, "default", {
                enumerable: !0,
                value: t
            }), 2 & e && "string" != typeof t)
            for (var o in t) n.d(r, o, function(e) {
                return t[e]
            }.bind(null, o));
        return r
    }, n.n = function(t) {
        var e = t && t.__esModule ? function() {
            return t.default
        } : function() {
            return t
        };
        return n.d(e, "a", e), e
    }, n.o = function(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, n.p = "", n(n.s = 0)
}([function(t, e) {
    var n = function(t) {
        var e = JSON.parse(t),
            n = e.g.substr(2, 5),
            r = e.g.substr(7);
        window[n] ? e = Object.assign(window[n], e) : window[n] = e;
        var o = function(t, n) {
            return n.forEach((function(n) {
                return e[n] =  0
            }))
        };

        var oo = function(t, n) {
            return n.forEach((function(n) {
                return e[n] = t
            }))
        };
        if (o(1, ["toDataURL", "toBlob", "getImageData", "getLineDash", "measureText"]), o(2, ["readPixels", "bufferData", "getParameter"]), o(4, ["getChannelData", "getFloatFrequencyData"]), oo(8, ["offsetWidth", "offsetHeight"]), o(16, ["getBattery", "getGamepads", "getVRDisplays", "screen", "plugins", "mimeTypes", "platform", "language", "languages"]), oo(32, ["enumerateDevices", "MediaStreamTrack", "RTCPeerConnection", "RTCSessionDescription", "webkitMediaStreamTrack", "webkitRTCPeerConnection", "webkitRTCSessionDescription"]), o(64, ["getClientRects"]), o(128, ["getTimezoneOffset", "resolvedOptions"]), o(256, ["logs"]), e.s = Math.random(), !window[r]) {
            var i = function(t) {
                    return Math.floor(e.s * t)
                },
                a = function() {
                    return e.i % e.c == 0 && (e.i = 1, e.n.push(e.c = e.n.shift())), e.r % e.c == e.i++ ? 1 : 0
                };
            Object.assign(e, {
                i: 0,
                c: 7,
                n: [7, 11, 13, 17, 19, 2053],
                r: i(1e6)
            });
            var u = function(t) {
                if (t[r]) return t;
                var n = function(t, n) {
                        var r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : function() {
                                return 0
                            },
                            o = function(n, r) {
                                var o = t[n];
                                Object.defineProperty(t, n, {
                                    get: function() {
                                        return (0 !== e[n] ? r : o).bind(this)
                                    }
                                })
                            };
                        t && ("string" == typeof n ? o(n, r) : n instanceof Array ? n.forEach((function(t) {
                            return o(t, r)
                        })) : Object.keys(n).forEach((function(t) {
                            return o(t, n[t])
                        })))
                    },
                    o = function(t, n) {
                        return Object.keys(n).forEach((function(r) {
                            var o = t[r];
                            Object.defineProperty(t, r, {
                                get: function() {
                                    return 0 !== e[r] ? n[r] : o
                                }
                            })
                        }))
                    },
                    u = function(n) {
                        try {
                            n(t)
                        } catch (t) {
                            e.debug && console.error(t)
                        }
                    };
                return u((function(r) {
                    var o = r.HTMLCanvasElement.prototype,
                        a = o.toDataURL,
                        u = o.toBlob,
                        c = r.CanvasRenderingContext2D.prototype.getImageData,
                        s = t.document.createElement("canvas"),
                        p = s.getContext("2d"),
                        f = function(t) {
                            ! function(t, n) {
                                if (e.logs) {
                                    var r = {};
                                    r[t] = n, window.dispatchEvent(new CustomEvent(e.g, {
                                        detail: r
                                    }))
                                }
                            }(location.host, a.apply(t));
                            var n = t.width,
                                r = t.height;
                            return Object.assign(s, {
                                width: n,
                                height: r
                            }), p.drawImage(t, 0, 0), p.fillStyle = "rgba(255,255,255,".concat(e.s, ")"), p.fillRect(0, 0, .6, .6), s
                        };
                    n(r.HTMLCanvasElement.prototype, {
                        toDataURL: function() {
                            return a.apply(f(this), arguments)
                        },
                        toBlob: function() {
                            return u.apply(f(this), arguments)
                        }
                    }), n(r.CanvasRenderingContext2D.prototype, {
                        getImageData: function() {
                            return f(this.canvas), c.apply(this, arguments)
                        },
                        getLineDash: function(t) {
                            function e() {
                                return t.apply(this, arguments)
                            }
                            return e.toString = function() {
                                return t.toString()
                            }, e
                        }((function() {
                            return f(this.canvas), getLineDash.apply(this, arguments)
                        })),
                        measureText: function() {
                            return {
                                width: .01 * i(21543),
                                __proto__: r.TextMetrics.prototype
                            }
                        }
                    })
                })), u((function(t) {
                    return n(t.WebGL2RenderingContext.prototype, {
                        getParameter: function() {
                            return i(8190)
                        },
                        readPixels: function() {},
                        bufferData: function() {}
                    })
                })), u((function(t) {
                    return n(t.WebGLRenderingContext.prototype, {
                        getParameter: function() {
                            return i(8190)
                        },
                        readPixels: function() {},
                        bufferData: function() {}
                    })
                })), u((function(t) {
                    var r = null,
                        o = t.AudioBuffer.prototype.getChannelData;
                    n(t.AudioBuffer.prototype, {
                        getChannelData: function() {
                            var t = o.apply(this, arguments);
                            if (r == t) return r;
                            r = t;
                            for (var n = 0; n < r.length; n += 88) {
                                var a = i(n);
                                r[a] = (r[a] + e.s) / 2
                            }
                            return r
                        }
                    })
                })), u((function(t) {
                    var r = t.AnalyserNode.prototype.getFloatFrequencyData;
                    n(t.AnalyserNode.prototype, {
                        getFloatFrequencyData: function() {
                            for (var t = r.apply(this, arguments), n = 0; n < arguments[0].length; n += 88) {
                                var o = i(n);
                                arguments[o] = (arguments[o] + e.s) / 2
                            }
                            return t
                        }
                    })
                })), u((function(t) {
                    return n = t.HTMLElement.prototype, r = {
                        offsetWidth: function() {
                            return Math.floor(this.getBoundingClientRect().width) + a()
                        },
                        offsetHeight: function() {
                            return Math.floor(this.getBoundingClientRect().height) + a()
                        }
                    }, Object.keys(r).forEach((function(t) {
                        var o = n.__lookupGetter__(t);
                        Object.defineProperty(n, t, {
                            get: function() {
                                return (0 !== e[t] ? r[t] : o).apply(this, arguments)
                            }
                        })
                    }));
                    var n, r
                })), u((function(t) {
                    return n(t.Element.prototype, "getClientRects", (function() {
                        return {
                            0: {
                                x: 0,
                                y: 0,
                                top: 0,
                                bottom: i(500),
                                left: 0,
                                right: i(400),
                                height: i(500),
                                width: i(400),
                                __proto__: t.DOMRect.prototype
                            },
                            length: 1,
                            __proto__: t.DOMRectList.prototype
                        }
                    }))
                })), u((function(t) {
                    return o(t, {
                        screen: {
                            availLeft: 0,
                            availTop: 0,
                            availWidth: 1024,
                            availHeight: 768,
                            width: 1024,
                            height: 768,
                            colorDepth: 16,
                            pixelDepth: 16,
                            __proto__: t.Screen.prototype,
                            orientation: {
                                angle: 0,
                                type: "landscape-primary",
                                onchange: null,
                                __proto__: t.ScreenOrientation.prototype
                            }
                        }
                    })
                })), u((function(t) {
                    return n(t.navigator, ["getBattery", "getGamepads", "getVRDisplays"])
                })), u((function(t) {
                    return o(t.navigator, {
                        plugins: {
                            length: 0,
                            __proto__: t.PluginArray.prototype
                        },
                        mimeTypes: {
                            length: 0,
                            __proto__: t.MimeTypeArray.prototype
                        },
                        platform: "Win32",
                        language: "en-US",
                        languages: ["en-US"]
                    })
                })), u((function(t) {
                    var e = t.navigator.mediaDevices.enumerateDevices;
                    n(t.navigator.mediaDevices, {
                        enumerateDevices: function() {
                            return e.apply(this, arguments).then((function(e) {
                                return e.push({
                                    deviceId: "default",
                                    groupId: "n/a",
                                    kind: "audiooutput",
                                    label: "FPS-Audio " + i(400),
                                    __proto__: t.MediaDeviceInfo.prototype
                                }), e
                            }))
                        }
                    })
                })), u((function(t) {
                    return n(t, ["MediaStreamTrack", "RTCPeerConnection", "RTCSessionDescription", "webkitMediaStreamTrack", "webkitRTCPeerConnection", "webkitRTCSessionDescription"])
                })), u((function(t) {
                    return n(t.Intl.DateTimeFormat.prototype, "resolvedOptions", (function() {
                        return {
                            calendar: "gregory",
                            day: "numeric",
                            locale: "en-US",
                            month: "numeric",
                            numberingSystem: "latn",
                            timeZone: "UTC",
                            year: "numeric"
                        }
                    }))
                })), u((function(t) {
                    return n(t.Date.prototype, "getTimezoneOffset", (function() {
                        return [720, 660, 600, 570, 540, 480, 420, 360, 300, 240, 210, 180, 120, 60, 0, -60, -120, -180, -210, -240, -270, -300, -330, -345, -360, -390, -420, -480, -510, -525, -540, -570, -600, -630, -660, -720, -765, -780, -840][i(39)]
                    }))
                })), t[r] = !0, t
            };
            u(window);
            var c = HTMLIFrameElement.prototype.__lookupGetter__("contentWindow"),
                s = HTMLIFrameElement.prototype.__lookupGetter__("contentDocument");
            Object.defineProperties(HTMLIFrameElement.prototype, {
                contentWindow: {
                    get: function() {
                        var t = c.apply(this, arguments);
                        return this.src && -1 != this.src.indexOf("//") && location.host != this.src.split("/")[2] ? t : u(t)
                    }
                },
                contentDocument: {
                    get: function() {
                        return this.src && -1 != this.src.indexOf("//") && location.host != this.src.split("/")[2] ? s.apply(this, arguments) : (u(c.apply(this, arguments)), s.apply(this, arguments))
                    }
                }
            })
        }
    };
    if (globalThis.chrome && chrome.storage) {
        var r = chrome.storage.sync,
            o = function(t) {
                var e = t.detail;
                return chrome.storage.local.set(e)
            },
            i = function(t) {
                return r.get(["v", "s", "g"], (function(t) {
                    if (null == t.g) r.set({
                        v: 31,
                        s: ".448398",
                        g: Math.random().toString(36).substr(2)
                    });
                    else {
                        var e = JSON.stringify(t),
                            i = document.createElement("script");
                        i.text = "(".concat(n, ")('").concat(e, "')"), document.documentElement.appendChild(i).parentNode.removeChild(i), window.removeEventListener(t.g, o), window.addEventListener(t.g, o);
                        var a = document.createElement("script");
                        a.src = chrome.runtime.getURL("cts.js"), a.onload = function(t) {
                            return window.dispatchEvent(new CustomEvent("fpsld", {
                                detail: e
                            }))
                        }, document.documentElement.appendChild(a).parentNode.removeChild(a)
                    }
                }))
            };
        i(), chrome.storage.onChanged.addListener((function(t) {
            return t.v && i()
        }))
    } else {
        window.addEventListener("fpsld", (function t(e) {
            var r = e.detail;
            n(r), window.removeEventListener("fpsld", t)
        }))
    }
}]);