from __future__ import annotations

import abc
import html
import json
import logging
import os
import os.path
import random
import re
import shutil
import tempfile
import time
import traceback
import webbrowser
from dataclasses import dataclass
from functools import reduce

import requests
import undetected_chromedriver as uc  # undetected
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys
from selenium_stealth import stealth
#if sys.platform == 'win32':
#    from user_agent import get_random_user_agent
#
#else:
#    from crawler.user_agent import get_random_user_agent
#

def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def preg_repace(**kwargs):
    pattern = kwargs.get("patt")
    replacement = kwargs.get("repl")
    subject = kwargs.get("subj")
    output = ""
    try:
        output = re.compile(pattern, re.IGNORECASE)
        output = output.sub(replacement, str(subject)).strip()
    except:
        logging.error(traceback.format_exc())
    return output


def open_in_browser(str1):
    fd, fname = tempfile.mkstemp(".html")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(str(str1))
    os.close(fd)
    return webbrowser.open(f"file://{fname}")


def get_title_page(html1):
    title = ""
    try:
        title = parse_field("//title", html1).lower().strip()
    except:
        """"""
    return title


def parse_field(selector, html1):
    value = ""
    try:
        value = html1.xpath(f"normalize-space({selector})").get()
        if value == "I have other vehicles to add":
            value = ""
    except:
        """"""
    return value


def exit():
    os._exit(1)

class ChromeWithPrefs(uc.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")
            self._handle_local(options, user_data_dir)
            self._handle_prefs(options, user_data_dir)
            time.sleep(15)
        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options, user_data_dir):
        prefs = options.experimental_options.get("prefs")
        if prefs:
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create an user_data_dir and add its path to the options
            # user_data_dir = os.path.normpath(tempfile.mkdtemp())
            # options.add_argument(f"--user-data-dir={user_data_dir}")
            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]

    @staticmethod
    def _handle_local(options, user_data_dir):
        prefs = options.experimental_options.get("localState")
        if prefs:
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create the preferences json file in its default directory
            prefs_file = os.path.join(user_data_dir, "Local State")

            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            with open(prefs_file, encoding="latin1", mode="r") as f:
                print(json.load(f))

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["localState"]

class fctselenuim:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")  # mobile, chrome
        self.proxy_list = kwargs.get("proxy")
        self.use_proxy = kwargs.get("use_proxy")
        self.use_ua = kwargs.get("use_userAgent", True)
        self.use_canvas = kwargs.get("use_canvas", True)
        self.use_webgl = kwargs.get("use_webgl", True)
        self.use_audio = kwargs.get("use_audio", True)
        self.use_webrtc = kwargs.get("use_webrtc", True)
        self.use_webrtc_1 = kwargs.get("use_webrtc_1", False)
        self.use_privacy_badger = kwargs.get("use_privacy_badger", True)
        self.driver = None
        self.proxyDict = None

    def initialize(self):
        options_chrome = None
        try:
            options_chrome = webdriver.ChromeOptions()  # undetected
            options_chrome.add_argument("--start-maximized")
            options_chrome.add_argument("--disable-notifications")
            options_chrome.add_argument("--disable-popup-blocking")
            local_state = {
                "dns_over_https.mode": "off"
            }
            options_chrome.add_experimental_option('localState', local_state)
            options_chrome.add_argument(
                "--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints"
            )
            # options_chrome.headless = True
            options_chrome.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 0})
            options_chrome.add_argument("--disk-cache-dir=/app/cache/")
            # options_chrome.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 11.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5376.148 Safari/537.36")

            # Load tracker blockers
            # options_chrome.add_argument(
            #    "--load-extension=./crawler/pkehgijcmpdhfbdbbnkijodmdjhbjlgp,./crawler/gighmmpiobklfepjocnamgkkbiglidom"
            # )
            path_proxy = ""
            if self.use_proxy:
                path_proxy = self.create_plugin_proxy()
            canvas_path, webgl_path, audiocontext_path, fingerprint_path, webrtc_path, useragent_path, \
            privacy_badger_path = self.get_plugins()

            args_string = '--load-extension='
            if self.use_proxy:
                if os.path.exists(path_proxy):
                    args_string += f"{path_proxy},"
            if self.use_ua:
                args_string += f"{useragent_path},"
            if self.use_webgl:
                args_string += f"{webgl_path},"
            if self.use_webrtc:
                args_string += f"{fingerprint_path},"
            if self.use_webrtc_1:
                args_string += f"{webrtc_path},"
            if self.use_canvas:
                args_string += f"{canvas_path},"
            if self.use_audio:
                args_string += f"{audiocontext_path},"
            if self.use_privacy_badger:
                args_string += f"{privacy_badger_path},"

            options_chrome.add_argument(args_string[:-1])
        except:
            logging.error(traceback.format_exc())

        return options_chrome

    def send(self, cmd, params={}):
        resource = (
                "/session/%s/chromium/send_command_and_get_result" % self.driver.session_id
        )
        url = self.driver.command_executor._url + resource
        body = json.dumps({"cmd": cmd, "params": params})
        response = self.driver.command_executor._request("POST", url, body)
        return response.get("value")

    def navigator_memory(self):
        memory = random.choices([1, 2, 4, 8, 12, 16, 32, ])
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'deviceMemory', {
                      get: () => %s
                    })
                  """ % (str(memory[0]))
        })

    def navigator_hardwareConcurrency(self):
        memory = random.choices([1, 2, 6, 8, 12, 14, 16, 18])
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                            Object.defineProperty(navigator, 'hardwareConcurrency', {
                              get: () => %s
                            })
                          """ % (str(memory[0]))
        })

    def open(self):
        options_chrome = self.initialize()
        try:
            self.driver = ChromeWithPrefs(
                options=options_chrome, suppress_welcome=True
            )  # undetected
        except Exception as e:
            print(e)


        # self.send(
        #     "Network.setBlockedURLs",
        #     {
        #         "urls": [
        #             "agkn.com",
        #             "brilliantcollector.com",
        #             "browser-intake-datadoghq.com",
        #             "cloudflare.com",
        #             "demdex.net",
        #             "doubleclick.net",
        #             "eum-appdynamics.com",
        #             "glia.com",
        #             "go-mpulse.net",
        #             "googletagmanager.com",
        #             "gstatic.com",
        #             "monetate.net",
        #             "optimizely.com",
        #             "salemove.com",
        #             "tealiumiq.com",
        #             "tiqcdn.com",
        #             "zeronaught.com",
        #             "creativevirtual16.com",
        #             "evidon.com"
        #         ]
        #     },
        # )
        # self.send("Network.enable", {})
        # stealth(self.driver,
        #         # user_agent=get_random_user_agent(),
        #         languages=["en-US", "en"],
        #         platform="Win32",
        #         webgl_vendor="Intel Inc.",
        #         renderer="Intel Iris OpenGL Engine",
        #         fix_hairline=True
        #         )
        # time.sleep(3)
        # self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
        #     Object.defineProperty(Navigator.prototype, 'webdriver', {
        #         set: false,
        #         enumerable: true,
        #         configurable: true,
        #         get: new Proxy(
        #             Object.getOwnPropertyDescriptor(Navigator.prototype, 'webdriver').get,
        #             { apply: (target, thisArg, args) => {
        #                 // emulate getter call validation
        #                 Reflect.apply(target, thisArg, args);
        #                 return false;
        #             }}
        #         )
        #     });
        # """})

        # self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
        #     () => {
        #               /**
        #                * A set of shared utility functions specifically for the purpose of modifying native browser APIs without leaving traces.
        #                *
        #                * Meant to be passed down in puppeteer and used in the context of the page (everything in here runs in NodeJS as well as a browser).
        #                *
        #                * Note: If for whatever reason you need to use this outside of `puppeteer-extra`:
        #                * Just remove the `module.exports` statement at the very bottom, the rest can be copy pasted into any browser context.
        #                *
        #                * Alternatively take a look at the `extract-stealth-evasions` package to create a finished bundle which includes these utilities.
        #                *
        #                */
        #               utils = {}
        #
        #               /**
        #                * Wraps a JS Proxy Handler and strips it's presence from error stacks, in case the traps throw.
        #                *
        #                * The presence of a JS Proxy can be revealed as it shows up in error stack traces.
        #                *
        #                * @param {object} handler - The JS Proxy handler to wrap
        #                */
        #               utils.stripProxyFromErrors = (handler = {}) => {
        #                 const newHandler = {}
        #                 // We wrap each trap in the handler in a try/catch and modify the error stack if they throw
        #                 const traps = Object.getOwnPropertyNames(handler)
        #                 traps.forEach(trap => {
        #                   newHandler[trap] = function () {
        #                     try {
        #                       // Forward the call to the defined proxy handler
        #                       return handler[trap].apply(this, arguments || [])
        #                     } catch (err) {
        #                       // Stack traces differ per browser, we only support chromium based ones currently
        #                       if (!err || !err.stack || !err.stack.includes(`at `)) {
        #                         throw err
        #                       }
        #
        #                       // When something throws within one of our traps the Proxy will show up in error stacks
        #                       // An earlier implementation of this code would simply strip lines with a blacklist,
        #                       // but it makes sense to be more surgical here and only remove lines related to our Proxy.
        #                       // We try to use a known "anchor" line for that and strip it with everything above it.
        #                       // If the anchor line cannot be found for some reason we fall back to our blacklist approach.
        #
        #                       const stripWithBlacklist = stack => {
        #                         const blacklist = [
        #                           `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply
        #                           `at Object.${trap} `, // e.g. Object.get or Object.apply
        #                           `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)
        #                         ]
        #                         return (
        #                           err.stack
        #                             .split('\n')
        #                             // Always remove the first (file) line in the stack (guaranteed to be our proxy)
        #                             .filter((line, index) => index !== 1)
        #                             // Check if the line starts with one of our blacklisted strings
        #                             .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))
        #                             .join('\n')
        #                         )
        #                       }
        #
        #                       const stripWithAnchor = stack => {
        #                         const stackArr = stack.split('\n')
        #                         const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium
        #                         const anchorIndex = stackArr.findIndex(line =>
        #                           line.trim().startsWith(anchor)
        #                         )
        #                         if (anchorIndex === -1) {
        #                           return false // 404, anchor not found
        #                         }
        #                         // Strip everything from the top until we reach the anchor line
        #                         // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)
        #                         stackArr.splice(1, anchorIndex)
        #                         return stackArr.join('\n')
        #                       }
        #
        #                       // Try using the anchor method, fallback to blacklist if necessary
        #                       err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)
        #
        #                       throw err // Re-throw our now sanitized error
        #                     }
        #                   }
        #                 })
        #                 return newHandler
        #               }
        #
        #               /**
        #                * Strip error lines from stack traces until (and including) a known line the stack.
        #                *
        #                * @param {object} err - The error to sanitize
        #                * @param {string} anchor - The string the anchor line starts with
        #                */
        #               utils.stripErrorWithAnchor = (err, anchor) => {
        #                 const stackArr = err.stack.split('\n')
        #                 const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))
        #                 if (anchorIndex === -1) {
        #                   return err // 404, anchor not found
        #                 }
        #                 // Strip everything from the top until we reach the anchor line (remove anchor line as well)
        #                 // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)
        #                 stackArr.splice(1, anchorIndex)
        #                 err.stack = stackArr.join('\n')
        #                 return err
        #               }
        #
        #               /**
        #                * Replace the property of an object in a stealthy way.
        #                *
        #                * Note: You also want to work on the prototype of an object most often,
        #                * as you'd otherwise leave traces (e.g. showing up in Object.getOwnPropertyNames(obj)).
        #                *
        #                * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty
        #                *
        #                * @example
        #                * replaceProperty(WebGLRenderingContext.prototype, 'getParameter', { value: "alice" })
        #                * // or
        #                * replaceProperty(Object.getPrototypeOf(navigator), 'languages', { get: () => ['en-US', 'en'] })
        #                *
        #                * @param {object} obj - The object which has the property to replace
        #                * @param {string} propName - The property name to replace
        #                * @param {object} descriptorOverrides - e.g. { value: "alice" }
        #                */
        #               utils.replaceProperty = (obj, propName, descriptorOverrides = {}) => {
        #                 return Object.defineProperty(obj, propName, {
        #                   // Copy over the existing descriptors (writable, enumerable, configurable, etc)
        #                   ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),
        #                   // Add our overrides (e.g. value, get())
        #                   ...descriptorOverrides
        #                 })
        #               }
        #
        #               /**
        #                * Preload a cache of function copies and data.
        #                *
        #                * For a determined enough observer it would be possible to overwrite and sniff usage of functions
        #                * we use in our internal Proxies, to combat that we use a cached copy of those functions.
        #                *
        #                * This is evaluated once per execution context (e.g. window)
        #                */
        #               utils.preloadCache = () => {
        #                 if (utils.cache) {
        #                   return
        #                 }
        #                 utils.cache = {
        #                   // Used in our proxies
        #                   Reflect: {
        #                     get: Reflect.get.bind(Reflect),
        #                     apply: Reflect.apply.bind(Reflect)
        #                   },
        #                   // Used in `makeNativeString`
        #                   nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`
        #                 }
        #               }
        #
        #               /**
        #                * Utility function to generate a cross-browser `toString` result representing native code.
        #                *
        #                * There's small differences: Chromium uses a single line, whereas FF & Webkit uses multiline strings.
        #                * To future-proof this we use an existing native toString result as the basis.
        #                *
        #                * The only advantage we have over the other team is that our JS runs first, hence we cache the result
        #                * of the native toString result once, so they cannot spoof it afterwards and reveal that we're using it.
        #                *
        #                * Note: Whenever we add a `Function.prototype.toString` proxy we should preload the cache before,
        #                * by executing `utils.preloadCache()` before the proxy is applied (so we don't cause recursive lookups).
        #                *
        #                * @example
        #                * makeNativeString('foobar') // => `function foobar() { [native code] }`
        #                *
        #                * @param {string} [name] - Optional function name
        #                */
        #               utils.makeNativeString = (name = '') => {
        #                 // Cache (per-window) the original native toString or use that if available
        #                 utils.preloadCache()
        #                 return utils.cache.nativeToStringStr.replace('toString', name || '')
        #               }
        #
        #               /**
        #                * Helper function to modify the `toString()` result of the provided object.
        #                *
        #                * Note: Use `utils.redirectToString` instead when possible.
        #                *
        #                * There's a quirk in JS Proxies that will cause the `toString()` result to differ from the vanilla Object.
        #                * If no string is provided we will generate a `[native code]` thing based on the name of the property object.
        #                *
        #                * @example
        #                * patchToString(WebGLRenderingContext.prototype.getParameter, 'function getParameter() { [native code] }')
        #                *
        #                * @param {object} obj - The object for which to modify the `toString()` representation
        #                * @param {string} str - Optional string used as a return value
        #                */
        #               utils.patchToString = (obj, str = '') => {
        #                 utils.preloadCache()
        #
        #                 const toStringProxy = new Proxy(Function.prototype.toString, {
        #                   apply: function (target, ctx) {
        #                     // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + ""`
        #                     if (ctx === Function.prototype.toString) {
        #                       return utils.makeNativeString('toString')
        #                     }
        #                     // `toString` targeted at our proxied Object detected
        #                     if (ctx === obj) {
        #                       // We either return the optional string verbatim or derive the most desired result automatically
        #                       return str || utils.makeNativeString(obj.name)
        #                     }
        #                     // Check if the toString protype of the context is the same as the global prototype,
        #                     // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case
        #                     const hasSameProto = Object.getPrototypeOf(
        #                       Function.prototype.toString
        #                     ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins
        #                     if (!hasSameProto) {
        #                       // Pass the call on to the local Function.prototype.toString instead
        #                       return ctx.toString()
        #                     }
        #                     return target.call(ctx)
        #                   }
        #                 })
        #                 utils.replaceProperty(Function.prototype, 'toString', {
        #                   value: toStringProxy
        #                 })
        #               }
        #
        #               /**
        #                * Make all nested functions of an object native.
        #                *
        #                * @param {object} obj
        #                */
        #               utils.patchToStringNested = (obj = {}) => {
        #                 return utils.execRecursively(obj, ['function'], utils.patchToString)
        #               }
        #
        #               /**
        #                * Redirect toString requests from one object to another.
        #                *
        #                * @param {object} proxyObj - The object that toString will be called on
        #                * @param {object} originalObj - The object which toString result we wan to return
        #                */
        #               utils.redirectToString = (proxyObj, originalObj) => {
        #                 utils.preloadCache()
        #
        #                 const toStringProxy = new Proxy(Function.prototype.toString, {
        #                   apply: function (target, ctx) {
        #                     // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + ""`
        #                     if (ctx === Function.prototype.toString) {
        #                       return utils.makeNativeString('toString')
        #                     }
        #
        #                     // `toString` targeted at our proxied Object detected
        #                     if (ctx === proxyObj) {
        #                       const fallback = () =>
        #                         originalObj && originalObj.name
        #                           ? utils.makeNativeString(originalObj.name)
        #                           : utils.makeNativeString(proxyObj.name)
        #
        #                       // Return the toString representation of our original object if possible
        #                       return originalObj + '' || fallback()
        #                     }
        #
        #                     // Check if the toString protype of the context is the same as the global prototype,
        #                     // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case
        #                     const hasSameProto = Object.getPrototypeOf(
        #                       Function.prototype.toString
        #                     ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins
        #                     if (!hasSameProto) {
        #                       // Pass the call on to the local Function.prototype.toString instead
        #                       return ctx.toString()
        #                     }
        #
        #                     return target.call(ctx)
        #                   }
        #                 })
        #                 utils.replaceProperty(Function.prototype, 'toString', {
        #                   value: toStringProxy
        #                 })
        #               }
        #
        #               /**
        #                * All-in-one method to replace a property with a JS Proxy using the provided Proxy handler with traps.
        #                *
        #                * Will stealthify these aspects (strip error stack traces, redirect toString, etc).
        #                * Note: This is meant to modify native Browser APIs and works best with prototype objects.
        #                *
        #                * @example
        #                * replaceWithProxy(WebGLRenderingContext.prototype, 'getParameter', proxyHandler)
        #                *
        #                * @param {object} obj - The object which has the property to replace
        #                * @param {string} propName - The name of the property to replace
        #                * @param {object} handler - The JS Proxy handler to use
        #                */
        #               utils.replaceWithProxy = (obj, propName, handler) => {
        #                 utils.preloadCache()
        #                 const originalObj = obj[propName]
        #                 const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))
        #
        #                 utils.replaceProperty(obj, propName, { value: proxyObj })
        #                 utils.redirectToString(proxyObj, originalObj)
        #
        #                 return true
        #               }
        #
        #               /**
        #                * All-in-one method to mock a non-existing property with a JS Proxy using the provided Proxy handler with traps.
        #                *
        #                * Will stealthify these aspects (strip error stack traces, redirect toString, etc).
        #                *
        #                * @example
        #                * mockWithProxy(chrome.runtime, 'sendMessage', function sendMessage() {}, proxyHandler)
        #                *
        #                * @param {object} obj - The object which has the property to replace
        #                * @param {string} propName - The name of the property to replace or create
        #                * @param {object} pseudoTarget - The JS Proxy target to use as a basis
        #                * @param {object} handler - The JS Proxy handler to use
        #                */
        #               utils.mockWithProxy = (obj, propName, pseudoTarget, handler) => {
        #                 utils.preloadCache()
        #                 const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))
        #
        #                 utils.replaceProperty(obj, propName, { value: proxyObj })
        #                 utils.patchToString(proxyObj)
        #
        #                 return true
        #               }
        #
        #               /**
        #                * All-in-one method to create a new JS Proxy with stealth tweaks.
        #                *
        #                * This is meant to be used whenever we need a JS Proxy but don't want to replace or mock an existing known property.
        #                *
        #                * Will stealthify certain aspects of the Proxy (strip error stack traces, redirect toString, etc).
        #                *
        #                * @example
        #                * createProxy(navigator.mimeTypes.__proto__.namedItem, proxyHandler) // => Proxy
        #                *
        #                * @param {object} pseudoTarget - The JS Proxy target to use as a basis
        #                * @param {object} handler - The JS Proxy handler to use
        #                */
        #               utils.createProxy = (pseudoTarget, handler) => {
        #                 utils.preloadCache()
        #                 const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))
        #                 utils.patchToString(proxyObj)
        #
        #                 return proxyObj
        #               }
        #
        #               /**
        #                * Helper function to split a full path to an Object into the first part and property.
        #                *
        #                * @example
        #                * splitObjPath(`HTMLMediaElement.prototype.canPlayType`)
        #                * // => {objName: "HTMLMediaElement.prototype", propName: "canPlayType"}
        #                *
        #                * @param {string} objPath - The full path to an object as dot notation string
        #                */
        #               utils.splitObjPath = objPath => ({
        #                 // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`
        #                 objName: objPath
        #                   .split('.')
        #                   .slice(0, -1)
        #                   .join('.'),
        #                 // Extract last dot entry ==> `canPlayType`
        #                 propName: objPath.split('.').slice(-1)[0]
        #               })
        #
        #               /**
        #                * Convenience method to replace a property with a JS Proxy using the provided objPath.
        #                *
        #                * Supports a full path (dot notation) to the object as string here, in case that makes it easier.
        #                *
        #                * @example
        #                * replaceObjPathWithProxy('WebGLRenderingContext.prototype.getParameter', proxyHandler)
        #                *
        #                * @param {string} objPath - The full path to an object (dot notation string) to replace
        #                * @param {object} handler - The JS Proxy handler to use
        #                */
        #               utils.replaceObjPathWithProxy = (objPath, handler) => {
        #                 const { objName, propName } = utils.splitObjPath(objPath)
        #                 const obj = eval(objName) // eslint-disable-line no-eval
        #                 return utils.replaceWithProxy(obj, propName, handler)
        #               }
        #
        #               /**
        #                * Traverse nested properties of an object recursively and apply the given function on a whitelist of value types.
        #                *
        #                * @param {object} obj
        #                * @param {array} typeFilter - e.g. `['function']`
        #                * @param {Function} fn - e.g. `utils.patchToString`
        #                */
        #               utils.execRecursively = (obj = {}, typeFilter = [], fn) => {
        #                 function recurse(obj) {
        #                   for (const key in obj) {
        #                     if (obj[key] === undefined) {
        #                       continue
        #                     }
        #                     if (obj[key] && typeof obj[key] === 'object') {
        #                       recurse(obj[key])
        #                     } else {
        #                       if (obj[key] && typeFilter.includes(typeof obj[key])) {
        #                         fn.call(this, obj[key])
        #                       }
        #                     }
        #                   }
        #                 }
        #                 recurse(obj)
        #                 return obj
        #               }
        #
        #               /**
        #                * Everything we run through e.g. `page.evaluate` runs in the browser context, not the NodeJS one.
        #                * That means we cannot just use reference variables and functions from outside code, we need to pass everything as a parameter.
        #                *
        #                * Unfortunately the data we can pass is only allowed to be of primitive types, regular functions don't survive the built-in serialization process.
        #                * This utility function will take an object with functions and stringify them, so we can pass them down unharmed as strings.
        #                *
        #                * We use this to pass down our utility functions as well as any other functions (to be able to split up code better).
        #                *
        #                * @see utils.materializeFns
        #                *
        #                * @param {object} fnObj - An object containing functions as properties
        #                */
        #               utils.stringifyFns = (fnObj = { hello: () => 'world' }) => {
        #                 // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine
        #                 // https://github.com/feross/fromentries
        #                 function fromEntries(iterable) {
        #                   return [...iterable].reduce((obj, [key, val]) => {
        #                     obj[key] = val
        #                     return obj
        #                   }, {})
        #                 }
        #                 return (Object.fromEntries || fromEntries)(
        #                   Object.entries(fnObj)
        #                     .filter(([key, value]) => typeof value === 'function')
        #                     .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval
        #                 )
        #               }
        #
        #               /**
        #                * Utility function to reverse the process of `utils.stringifyFns`.
        #                * Will materialize an object with stringified functions (supports classic and fat arrow functions).
        #                *
        #                * @param {object} fnStrObj - An object containing stringified functions as properties
        #                */
        #               utils.materializeFns = (fnStrObj = { hello: "() => 'world'" }) => {
        #                 return Object.fromEntries(
        #                   Object.entries(fnStrObj).map(([key, value]) => {
        #                     if (value.startsWith('function')) {
        #                       // some trickery is needed to make oldschool functions work :-)
        #                       return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval
        #                     } else {
        #                       // arrow functions just work
        #                       return [key, eval(value)] // eslint-disable-line no-eval
        #                     }
        #                   })
        #                 )
        #               }
        #
        #               utils.preloadCache()
        #             }
        # """})
        # self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
        #     () => {
        #           const handler = {
        #             apply: function (target, ctx, args) {
        #               const param = (args || [])[0]
        #
        #               if (param && param.name && param.name === 'notifications') {
        #                 const result = { state: Notification.permission }
        #                 Object.setPrototypeOf(result, PermissionStatus.prototype)
        #                 return Promise.resolve(result)
        #               }
        #
        #               return utils.cache.Reflect.apply(...arguments)
        #             }
        #           }
        #
        #           utils.replaceWithProxy(
        #             window.navigator.permissions.__proto__, // eslint-disable-line no-proto
        #             'query',
        #             handler
        #           )
        #         }
        # """})
        # self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
        #     () => {
        #           const fns = {};
        #           fns.generatePluginArray = (utils, fns) => pluginsData => {
        #             return fns.generateMagicArray(utils, fns)(
        #               pluginsData,
        #               PluginArray.prototype,
        #               Plugin.prototype,
        #               'name'
        #             )
        #           }
        #           fns.generateFunctionMocks = utils => (
        #             proto,
        #             itemMainProp,
        #             dataArray
        #           ) => ({
        #             /** Returns the MimeType object with the specified index. */
        #             item: utils.createProxy(proto.item, {
        #               apply(target, ctx, args) {
        #                 if (!args.length) {
        #                   throw new TypeError(
        #                     `Failed to execute 'item' on '${proto[Symbol.toStringTag]
        #                     }': 1 argument required, but only 0 present.`
        #                   )
        #                 }
        #                 // Special behavior alert:
        #                 // - Vanilla tries to cast strings to Numbers (only integers!) and use them as property index lookup
        #                 // - If anything else than an integer (including as string) is provided it will return the first entry
        #                 const isInteger = args[0] && Number.isInteger(Number(args[0])) // Cast potential string to number first, then check for integer
        #                 // Note: Vanilla never returns `undefined`
        #                 return (isInteger ? dataArray[Number(args[0])] : dataArray[0]) || null
        #               }
        #             }),
        #             /** Returns the MimeType object with the specified name. */
        #             namedItem: utils.createProxy(proto.namedItem, {
        #               apply(target, ctx, args) {
        #                 if (!args.length) {
        #                   throw new TypeError(
        #                     `Failed to execute 'namedItem' on '${proto[Symbol.toStringTag]
        #                     }': 1 argument required, but only 0 present.`
        #                   )
        #                 }
        #                 return dataArray.find(mt => mt[itemMainProp] === args[0]) || null // Not `undefined`!
        #               }
        #             }),
        #             /** Does nothing and shall return nothing */
        #             refresh: proto.refresh
        #               ? utils.createProxy(proto.refresh, {
        #                 apply(target, ctx, args) {
        #                   return undefined
        #                 }
        #               })
        #               : undefined
        #           })
        #           fns.generateMagicArray = (utils, fns) =>
        #             function (
        #               dataArray = [],
        #               proto = MimeTypeArray.prototype,
        #               itemProto = MimeType.prototype,
        #               itemMainProp = 'type'
        #             ) {
        #               // Quick helper to set props with the same descriptors vanilla is using
        #               const defineProp = (obj, prop, value) =>
        #                 Object.defineProperty(obj, prop, {
        #                   value,
        #                   writable: false,
        #                   enumerable: false, // Important for mimeTypes & plugins: `JSON.stringify(navigator.mimeTypes)`
        #                   configurable: false
        #                 })
        #
        #               // Loop over our fake data and construct items
        #               const makeItem = data => {
        #                 const item = {}
        #                 for (const prop of Object.keys(data)) {
        #                   if (prop.startsWith('__')) {
        #                     continue
        #                   }
        #                   defineProp(item, prop, data[prop])
        #                 }
        #                 // We need to spoof a specific `MimeType` or `Plugin` object
        #                 return Object.create(itemProto, Object.getOwnPropertyDescriptors(item))
        #               }
        #
        #               const magicArray = []
        #
        #               // Loop through our fake data and use that to create convincing entities
        #               dataArray.forEach(data => {
        #                 magicArray.push(makeItem(data))
        #               })
        #
        #               // Add direct property access  based on types (e.g. `obj['application/pdf']`) afterwards
        #               magicArray.forEach(entry => {
        #                 defineProp(magicArray, entry[itemMainProp], entry)
        #               })
        #
        #               // This is the best way to fake the type to make sure this is false: `Array.isArray(navigator.mimeTypes)`
        #               const magicArrayObj = Object.create(proto, {
        #                 ...Object.getOwnPropertyDescriptors(magicArray),
        #
        #                 // There's one ugly quirk we unfortunately need to take care of:
        #                 // The `MimeTypeArray` prototype has an enumerable `length` property,
        #                 // but headful Chrome will still skip it when running `Object.getOwnPropertyNames(navigator.mimeTypes)`.
        #                 // To strip it we need to make it first `configurable` and can then overlay a Proxy with an `ownKeys` trap.
        #                 length: {
        #                   value: magicArray.length,
        #                   writable: false,
        #                   enumerable: false,
        #                   configurable: true // Important to be able to use the ownKeys trap in a Proxy to strip `length`
        #                 }
        #               })
        #
        #               // Generate our functional function mocks :-)
        #               const functionMocks = fns.generateFunctionMocks(utils)(
        #                 proto,
        #                 itemMainProp,
        #                 magicArray
        #               )
        #
        #               // We need to overlay our custom object with a JS Proxy
        #               const magicArrayObjProxy = new Proxy(magicArrayObj, {
        #                 get(target, key = '') {
        #                   // Redirect function calls to our custom proxied versions mocking the vanilla behavior
        #                   if (key === 'item') {
        #                     return functionMocks.item
        #                   }
        #                   if (key === 'namedItem') {
        #                     return functionMocks.namedItem
        #                   }
        #                   if (proto === PluginArray.prototype && key === 'refresh') {
        #                     return functionMocks.refresh
        #                   }
        #                   // Everything else can pass through as normal
        #                   return utils.cache.Reflect.get(...arguments)
        #                 },
        #                 ownKeys(target) {
        #                   // There are a couple of quirks where the original property demonstrates "magical" behavior that makes no sense
        #                   // This can be witnessed when calling `Object.getOwnPropertyNames(navigator.mimeTypes)` and the absense of `length`
        #                   // My guess is that it has to do with the recent change of not allowing data enumeration and this being implemented weirdly
        #                   // For that reason we just completely fake the available property names based on our data to match what regular Chrome is doing
        #                   // Specific issues when not patching this: `length` property is available, direct `types` props (e.g. `obj['application/pdf']`) are missing
        #                   const keys = []
        #                   const typeProps = magicArray.map(mt => mt[itemMainProp])
        #                   typeProps.forEach((_, i) => keys.push(`${i}`))
        #                   typeProps.forEach(propName => keys.push(propName))
        #                   return keys
        #                 }
        #               })
        #
        #               return magicArrayObjProxy
        #             }
        #           fns.generateMimeTypeArray = (utils, fns) => mimeTypesData => {
        #             return fns.generateMagicArray(utils, fns)(
        #               mimeTypesData,
        #               MimeTypeArray.prototype,
        #               MimeType.prototype,
        #               'type'
        #             )
        #           }
        #
        #           const data = {
        #             "mimeTypes": [
        #               {
        #                 "type": "application/pdf",
        #                 "suffixes": "pdf",
        #                 "description": "",
        #                 "__pluginName": "Chrome PDF Viewer"
        #               },
        #               {
        #                 "type": "application/x-google-chrome-pdf",
        #                 "suffixes": "pdf",
        #                 "description": "Portable Document Format",
        #                 "__pluginName": "Chrome PDF Plugin"
        #               },
        #               {
        #                 "type": "application/x-nacl",
        #                 "suffixes": "",
        #                 "description": "Native Client Executable",
        #                 "__pluginName": "Native Client"
        #               },
        #               {
        #                 "type": "application/x-pnacl",
        #                 "suffixes": "",
        #                 "description": "Portable Native Client Executable",
        #                 "__pluginName": "Native Client"
        #               }
        #             ],
        #             "plugins": [
        #               {
        #                 "name": "Chrome PDF Plugin",
        #                 "filename": "internal-pdf-viewer",
        #                 "description": "Portable Document Format",
        #                 "__mimeTypes": ["application/x-google-chrome-pdf"]
        #               },
        #               {
        #                 "name": "Chrome PDF Viewer",
        #                 "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai",
        #                 "description": "",
        #                 "__mimeTypes": ["application/pdf"]
        #               },
        #               {
        #                 "name": "Native Client",
        #                 "filename": "internal-nacl-plugin",
        #                 "description": "",
        #                 "__mimeTypes": ["application/x-nacl", "application/x-pnacl"]
        #               }
        #             ]
        #           };
        #
        #           // That means we're running headful
        #           const hasPlugins = 'plugins' in navigator && navigator.plugins.length
        #           if (hasPlugins) {
        #             return // nothing to do here
        #           }
        #
        #           const mimeTypes = fns.generateMimeTypeArray(utils, fns)(data.mimeTypes)
        #           const plugins = fns.generatePluginArray(utils, fns)(data.plugins)
        #
        #           // Plugin and MimeType cross-reference each other, let's do that now
        #           // Note: We're looping through `data.plugins` here, not the generated `plugins`
        #           for (const pluginData of data.plugins) {
        #             pluginData.__mimeTypes.forEach((type, index) => {
        #               plugins[pluginData.name][index] = mimeTypes[type]
        #               plugins[type] = mimeTypes[type]
        #               Object.defineProperty(mimeTypes[type], 'enabledPlugins', {
        #                 value: JSON.parse(JSON.stringify(plugins[pluginData.name])),
        #                 writable: false,
        #                 enumerable: false, // Important: `JSON.stringify(navigator.plugins)`
        #                 configurable: false
        #               })
        #             })
        #           }
        #
        #           const patchNavigator = (name, value) =>
        #             utils.replaceProperty(Object.getPrototypeOf(navigator), name, {
        #               get() {
        #                 return value
        #               }
        #             })
        #
        #           patchNavigator('mimeTypes', mimeTypes)
        #           patchNavigator('plugins', plugins)
        #
        #           // All done
        #         }
        # """})
        self.change_geolocation_and_timezone()
        self.navigator_memory()
        self.navigator_hardwareConcurrency()
        # self.change_screen_resolution()


    def change_geolocation_and_timezone(self):
        self.driver.get('https://api.ipify.org?format=json')
        s = self.driver.find_element(By.CSS_SELECTOR, 'body').text
        ip = json.loads(s)['ip']
        print(ip)
        api = f'https://api.ipgeolocation.io/ipgeo?apiKey=8743eb92f00d4fbaa1532cfd4f106dc9&ip={ip}'
        response = requests.get(api)
        if response.status_code == 200:
            data = response.json()
            latitude = data['latitude']
            longitude = data['longitude']
            tz = data['time_zone']['name']
        else:
            print('ipgeolocation request failed...')
            return

        geo_params = {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "accuracy": 100
        }
        tz_params = {'timezoneId': tz}
        self.driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
        self.driver.execute_cdp_cmd("Page.setGeolocationOverride", geo_params)

    def change_screen_resolution(self):
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
            Object.defineProperty(window, 'screen', {
                value: {
                    availHeight: 1080,
                    availLeft: 0,
                    availTop: 0,
                    availWidth: 1920,
                    colorDepth: 24,
                    height: 1080,
                    pixelDepth: 24,
                    width: 1920
                }
            });"""})

    def close(self):
        self.driver.close()
        self.driver.quit()

    def get_plugins(self):
        absolute_path = os.path.abspath(os.path.dirname(__file__))
        canvas_path = os.path.join(absolute_path, "plugins/Canvas-Fingerprint-Defender")
        webgl_path = os.path.join(absolute_path, "plugins/WebGL-Fingerprint-Defender")
        audiocontext_path = os.path.join(absolute_path, "plugins/AudioContext-Fingerprint-Defender")
        fingerprint_path = os.path.join(absolute_path, "plugins/WebRTC-Control")
        webrtc_path = os.path.join(absolute_path, "plugins/Fingerprint-Spoofing")
        useragent_path = os.path.join(absolute_path, "plugins/Random-User-Agent")
        privacy_badger_path = os.path.join(absolute_path, "plugins/Privacy-Badger")

        return canvas_path, webgl_path, audiocontext_path, fingerprint_path, webrtc_path, useragent_path, privacy_badger_path

    def create_plugin_proxy(self):

        path_proxy = ""
        ip_proxy = port_proxy = user_proxy = pass_proxy = ""

        try:
            http_proxy = self.proxy_list[random.randint(0, len(self.proxy_list) - 1)]

            self.proxyDict = {
                "http": http_proxy,
                "https": http_proxy,
                "ftp": http_proxy,
            }

            http_proxy = preg_repace(patt="https?://", repl="", subj=http_proxy).strip()
            if "@" not in http_proxy:
                ip_proxy = http_proxy.split("@")[0].split(":")[0].strip()
                port_proxy = http_proxy.split("@")[0].split(":")[1].strip()
            else:
                ip_proxy = http_proxy.split("@")[1].split(":")[0].strip()
                port_proxy = http_proxy.split("@")[1].split(":")[1].strip()
                user_proxy = http_proxy.split("@")[0].split(":")[0].strip()
                pass_proxy = http_proxy.split("@")[0].split(":")[1].strip()
        except:
            logging.error(traceback.format_exc())

        try:
            manifest_json = """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                        "scripts": ["background.js"]
                    },
                    "minimum_chrome_version":"22.0.0"
                }
                """

            background_js = """
                var config = {
                        mode: "fixed_servers",
                        rules: {
                        singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                        },
                        bypassList: ["localhost"]
                        }
                    };

                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }

                chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                );
                """ % (
                ip_proxy,
                port_proxy,
                user_proxy,
                pass_proxy,
            )

            absolute_path = os.path.abspath(os.path.dirname(__file__))
            path_proxy = os.path.join(absolute_path, "plugins/proxy")
            if os.path.exists(path_proxy):
                shutil.rmtree(path_proxy)
                os.makedirs(path_proxy)
            else:
                os.makedirs(path_proxy)

            with open(
                    os.path.join(".", path_proxy, "manifest.json"), "w", encoding="utf-8"
            ) as f:
                f.write(manifest_json)

            with open(
                    os.path.join(".", path_proxy, "background.js"), "w", encoding="utf-8"
            ) as f:
                f.write(background_js)

        except:
            logging.error(traceback.format_exc())

        return path_proxy

    def get(self, url, delay=3):
        str1 = ""
        try:
            self.driver.get(url)
            time.sleep(delay)
            str1 = self.driver.execute_script(
                "return document.getElementsByTagName('html')[0].innerHTML"
            )
            str1 = html.unescape(str1)
        except:
            logging.error(traceback.format_exc())

        return str1

@dataclass
class ParseResult:
    has_car: bool | None = None
    is_customer: bool | None = None
    cars: list[str] | None = None
    valid: bool = False


class Parser(abc.ABC):
    @abc.abstractmethod
    def parse_site(
            self,
            firstname: str,
            lastname: str,
            address: str,
            city: str,
            state: str,
            zip: str,
            dob: str,
    ) -> ParseResult | None:
        pass


def get_parser(provider: str, proxy_list: list[str]) -> Parser:
    from crawler import libertymutual, statefarm

    if provider == "statefarm":
        return statefarm.StateFarmParser(use_proxy=True, proxy_list=proxy_list)

    if provider == "libertymutual":
        return libertymutual.LibertyMutualParser(use_proxy=True, proxy_list=proxy_list)
