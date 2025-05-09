(() => {
  "use strict";
  var e = { m: {}, u: (e) => e + ".ffmpeg.bundle.js" };
  (e.g = (function () {
    if ("object" == typeof globalThis) return globalThis;
    try {
      return this || new Function("return this")();
    } catch (e) {
      if ("object" == typeof window) return window;
    }
  })()),
    (e.o = (e, r) => Object.prototype.hasOwnProperty.call(e, r)),
    (e.r = (e) => {
      "undefined" != typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(e, "__esModule", { value: !0 });
    }),
    (() => {
      var r;
      e.g.importScripts && (r = e.g.location + "");
      var t = e.g.document;
      if (
        !r &&
        t &&
        (t.currentScript &&
          "SCRIPT" === t.currentScript.tagName.toUpperCase() &&
          (r = t.currentScript.src),
        !r)
      ) {
        var E = t.getElementsByTagName("script");
        if (E.length)
          for (var o = E.length - 1; o > -1 && (!r || !/^http(s?):/.test(r)); )
            r = E[o--].src;
      }
      if (!r)
        throw new Error(
          "Automatic publicPath is not supported in this browser"
        );
      (r = r
        .replace(/^blob:/, "")
        .replace(/#.*$/, "")
        .replace(/\?.*$/, "")
        .replace(/\/[^\/]+$/, "/")),
        (e.p = r);
    })(),
    (e.b = document.baseURI || self.location.href);
  var r,
    t,
    E,
    o = {};
  e.r(o),
    ((t = r || (r = {})).LOAD = "LOAD"),
    (t.EXEC = "EXEC"),
    (t.FFPROBE = "FFPROBE"),
    (t.WRITE_FILE = "WRITE_FILE"),
    (t.READ_FILE = "READ_FILE"),
    (t.DELETE_FILE = "DELETE_FILE"),
    (t.RENAME = "RENAME"),
    (t.CREATE_DIR = "CREATE_DIR"),
    (t.LIST_DIR = "LIST_DIR"),
    (t.DELETE_DIR = "DELETE_DIR"),
    (t.ERROR = "ERROR"),
    (t.DOWNLOAD = "DOWNLOAD"),
    (t.PROGRESS = "PROGRESS"),
    (t.LOG = "LOG"),
    (t.MOUNT = "MOUNT"),
    (t.UNMOUNT = "UNMOUNT"),
    new Error("unknown message type"),
    new Error("ffmpeg is not loaded, call `await ffmpeg.load()` first"),
    new Error("called FFmpeg.terminate()"),
    new Error("failed to import ffmpeg-core.js"),
    (function (e) {
      (e.MEMFS = "MEMFS"),
        (e.NODEFS = "NODEFS"),
        (e.NODERAWFS = "NODERAWFS"),
        (e.IDBFS = "IDBFS"),
        (e.WORKERFS = "WORKERFS"),
        (e.PROXYFS = "PROXYFS");
    })(E || (E = {})),
    (0, o.createFFmpeg)({ log: !0 });
})();
