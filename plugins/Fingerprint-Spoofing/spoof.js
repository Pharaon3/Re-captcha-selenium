! function(e) {
    var t = {};

    function n(o) {
        if (t[o]) return t[o].exports;
        var r = t[o] = {
            i: o,
            l: !1,
            exports: {}
        };
        return e[o].call(r.exports, r, r.exports, n), r.l = !0, r.exports
    }
    n.m = e, n.c = t, n.d = function(e, t, o) {
        n.o(e, t) || Object.defineProperty(e, t, {
            enumerable: !0,
            get: o
        })
    }, n.r = function(e) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }, n.t = function(e, t) {
        if (1 & t && (e = n(e)), 8 & t) return e;
        if (4 & t && "object" == typeof e && e && e.__esModule) return e;
        var o = Object.create(null);
        if (n.r(o), Object.defineProperty(o, "default", {
                enumerable: !0,
                value: e
            }), 2 & t && "string" != typeof e)
            for (var r in e) n.d(o, r, function(t) {
                return e[t]
            }.bind(null, r));
        return o
    }, n.n = function(e) {
        var t = e && e.__esModule ? function() {
            return e.default
        } : function() {
            return e
        };
        return n.d(t, "a", t), t
    }, n.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }, n.p = "", n(n.s = 3)
}
({
    3: function(e, t) {
        var n = chrome.storage.sync,
            o = function(e) {
                return (1e-99 * new Uint8Array(e.length).map((function(t, n) {
                    return e.charCodeAt(n)
                })).reduce((function(e, t, n) {
                    return e + t * Math.pow(8, n)
                }), 0)).toExponential().slice(1, -4)
            },
            r = function() {
                return n.get(["v"], (function(e) {
                    (512 | e.v) == e.v ? localStorage[0] = localStorage.cur = "random" : "random" == localStorage.cur && n.set({
                        s: o(localStorage.cur = "default")
                    }), document.querySelector("#cur").innerText = localStorage.cur || "default", document.querySelectorAll("fieldset").forEach((function(e) {
                        var t = e.children.select;
                        t.checked = localStorage.cur == localStorage[t.value]
                    }))
                }))
            };
        window.onload = function() {
            r(), document.querySelectorAll("fieldset").forEach((function(e) {
                var t = e.children.select;
                e.onclick = function(e) {
                    return n.get(["v"], (function(e) {
                        localStorage.cur = localStorage[t.value] || "default", "0" !== t.value ? ((512 | e.v) == e.v && n.set({
                            v: 512 ^ e.v
                        }), n.set({
                            s: o(localStorage.cur)
                        })) : n.set({
                            v: 512 | e.v
                        })
                    }))
                }
            })), document.querySelectorAll(".seed").forEach((function(e) {
                e.value = localStorage[e.id] || "", e.oninput = e.onchange = function(t) {
                    return n.set({
                        s: o(localStorage.cur = localStorage[e.id] = e.value || "default")
                    })
                }
            })), btc.onmouseenter = function(e) {
                bt.style.display = "block", bt.style.top = e.clientY - 240
            }, btc.onmouseleave = function(e) {
                return bt.style.display = "none"
            }, bch.onmouseenter = function(e) {
                bc.style.display = "block", bc.style.top = e.clientY - 240
            }, bch.onmouseleave = function(e) {
                return bc.style.display = "none"
            }
        },
        chrome.storage.onChanged.addListener((function(e) {
            return r()
        })),
        document.getElementById("asad").click();
        console.log(document.getElementById("asad"))
    }
});