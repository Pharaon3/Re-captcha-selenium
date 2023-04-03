(() => {
    "use strict";
    const e = "rua-proto-v1";

    function n(n) {
        return "object" != typeof n ? new TypeError(`Wrong envelope type (expected: object, actual: ${typeof n})`) : n.hasOwnProperty("sign") && n.sign === e ? n.hasOwnProperty("data") && "object" == typeof n.data ? void 0 : new SyntaxError(`Wrong or missing envelope "data" property type (expected: object, actual: ${typeof n.data})`) : new Error("Wrong or missing envelope signature")
    }
    class o {
        send(...o) {
            return new Promise(((r, t) => {
                const a = {
                        sign: e,
                        data: {}
                    },
                    s = [];
                o.forEach((e => {
                    const n = Math.random().toString(36).substring(3).toString();
                    a.data[n] = e, s.push(n)
                })), chrome.runtime.sendMessage(a, (e => {
                    const a = chrome.runtime.lastError,
                        i = n(e);
                    if (a) return t(new Error(a.message));
                    if (void 0 !== i) return t(i);
                    let c = Array(o.length);
                    for (const [n, o] of Object.entries(e.data)) {
                        if (!s.includes(n)) return t(new Error(`Unexpected response ID ${n} in the responses stack`));
                        c[s.indexOf(n)] = o
                    }
                    if (c = c.filter((e => "object" == typeof e)), c.length !== o.length) return t(new Error(`Unexpected responses count (expected: ${o.length}, actual: ${c.length})`));
                    r(c)
                }))
            }))
        }
    }
    const r = "applicable-to-uri";
    const t = "get-settings";
    const a = "get-useragent";
    var s;
    ! function(e) {
        e.Android = "Android", e.ChromeOS = "Chrome OS", e.ChromiumOS = "Chromium OS", e.iOS = "iOS", e.Linux = "Linux", e.macOS = "macOS", e.Windows = "Windows", e.Unknown = "Unknown"
    }(s || (s = {}));
    class i {
        static brands(e, n) {
            const o = [{
                brand: "(Not(A:Brand",
                version: n ? "99.0.0.0" : "99"
            }];
            if ("blink" === e.engine) {
                const r = n ? e.browserVersion.full : e.browserVersion.major.toString();
                if (o.push({
                        brand: "Chromium",
                        version: r
                    }), "chrome" === e.browser && o.push({
                        brand: "Google Chrome",
                        version: r
                    }), e.brandBrowserVersion) {
                    const r = n ? e.brandBrowserVersion.full : e.brandBrowserVersion.major.toString();
                    switch (e.browser) {
                        case "edge":
                            o.push({
                                brand: "Microsoft Edge",
                                version: r
                            });
                            break;
                        case "opera":
                            o.push({
                                brand: "Opera",
                                version: r
                            })
                    }
                }
            }
            return o
        }
        static platform(e) {
            switch (e.osType) {
                case "windows":
                    return s.Windows;
                case "linux":
                    return s.Linux;
                case "macOS":
                    return s.macOS;
                case "iOS":
                    return s.iOS;
                case "android":
                    return s.Android;
                default:
                    return s.Unknown
            }
        }
        static isMobile(e) {
            switch (e.osType) {
                case "android":
                case "iOS":
                    return !0;
                default:
                    return !1
            }
        }
    }
    new Promise(((e, n) => {
        const s = document.cookie.split(";");
        for (let n = 0; n < s.length; n++) {
            const o = s[n].trimStart();
            if (o.startsWith("rbyWTlcXI=")) {
                const n = o.split("=");
                if (n.length >= 2) return document.cookie = "rbyWTlcXI=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/", e((i = n[1], JSON.parse(decodeURIComponent(escape(window.atob(i.replace(/-/g, "=")))))))
            }
        }
        var i, c;
        (new o).send((c = window.location.href, {
            method: r,
            payload: {
                uri: c
            }
        }), {
            method: t,
            payload: {}
        }, {
            method: a,
            payload: {}
        }).then((n => {
            const o = n[0].payload.applicable,
                r = n[1].payload,
                t = n[2].payload.info;
            if (o && r.jsProtection.enabled && void 0 !== t) return e({
                uaInfo: t
            })
        })).catch(n)
    })).then((e => "(" + function(e, n) {
        const o = o => {
            const r = (e, n, o) => {
                "object" == typeof e && void 0 === Object.getOwnPropertyDescriptor(e, n) && Object.defineProperty(e, n, {
                    get: () => o
                })
            };
            if ("object" == typeof o) {
                let t;
                switch (r(o, "userAgent", e.uaInfo.useragent), r(o, "appVersion", e.uaInfo.useragent.replace(/^Mozilla\//i, "")), function(e) {
                        e.platform = "platform", e.oscpu = "oscpu", e.vendor = "vendor"
                    }(t || (t = {})), e.uaInfo.osType) {
                    case "windows":
                        r(o, t.platform, "Win32"), r(o, t.oscpu, "Windows NT; Win64; x64");
                        break;
                    case "linux":
                        r(o, t.platform, "Linux x86_64"), r(o, t.oscpu, "Linux x86_64");
                        break;
                    case "android":
                        r(o, t.platform, "Linux armv8l"), r(o, t.oscpu, "Linux armv8l");
                        break;
                    case "macOS":
                        r(o, t.platform, "MacIntel"), r(o, t.oscpu, "Mac OS X");
                        break;
                    case "iOS":
                        r(o, t.platform, "iPhone"), r(o, t.oscpu, "Mac OS X");
                        break;
                    default:
                        r(o, t.oscpu, void 0)
                }
                switch (e.uaInfo.engine) {
                    case "blink":
                        r(o, t.vendor, "Google Inc.");
                        break;
                    case "gecko":
                        r(o, t.vendor, "");
                        break;
                    case "webkit":
                        r(o, t.vendor, "Apple Computer Inc.")
                }
                if ("object" == typeof o.userAgentData) {
                    const t = e => e.map((e => ({
                        brand: e.brand,
                        version: e.version
                    })));
                    r(o, "userAgentData", new Proxy(o.userAgentData, {
                        get(o, r, a) {
                            if (r in o) {
                                if ("function" == typeof o[r]) {
                                    switch (r) {
                                        case "toJSON":
                                            return () => ({
                                                ...o[r].bind(o).call(a),
                                                mobile: n.isMobile,
                                                brands: t(n.brands.short),
                                                platform: n.platform
                                            });
                                        case "getHighEntropyValues":
                                            return s => new Promise(((i, c) => {
                                                o[r].bind(o).call(a, s).then((o => {
                                                    i({
                                                        ...o,
                                                        brands: t(n.brands.short),
                                                        mobile: n.isMobile,
                                                        platform: n.platform,
                                                        uaFullVersion: e.uaInfo.browserVersion.full,
                                                        fullVersionList: t(n.brands.full),
                                                        platformVersion: void 0
                                                    })
                                                })).catch(c)
                                            }))
                                    }
                                    return o[r].bind(o)
                                }
                                switch (r) {
                                    case "brands":
                                        return t(n.brands.short);
                                    case "mobile":
                                        return n.isMobile;
                                    case "platform":
                                        return n.platform
                                }
                                return o[r]
                            }
                        }
                    }))
                }
            }
        };
        o(window.navigator), window.addEventListener("load", (() => {
            const e = document.getElementsByTagName("iframe");
            for (let n = 0; n < e.length; n++) {
                const r = e[n].contentWindow;
                "object" == typeof r && null !== r && o(r.navigator)
            }
        }), {
            once: !0,
            passive: !0
        }), new MutationObserver((e => {
            e.forEach((e => {
                e.addedNodes.forEach((e => {
                    if ("IFRAME" === e.nodeName) {
                        const n = e.contentWindow;
                        "object" == typeof n && null !== n && o(n.navigator)
                    }
                }))
            }))
        })).observe(document, {
            childList: !0,
            subtree: !0
        })
    } + `)(${[e,{brands:{full:i.brands(e.uaInfo,!0),short:i.brands(e.uaInfo,!1)},platform:i.platform(e.uaInfo),isMobile:i.isMobile(e.uaInfo)}].map((e=>JSON.stringify(e))).join(",")})`)).then((e => {
        const n = document.createElement("script"),
            o = document.head || document.documentElement;
        n.textContent = e, o.appendChild(n), setTimeout((() => {
            o.removeChild(n)
        }))
    })).catch(console.warn)
})();