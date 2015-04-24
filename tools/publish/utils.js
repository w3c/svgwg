// utils.js
//
// A grab-bag of utility functions for use by the publication scripts.

var fs = require('fs'),
    DOMParser = require('xmldom').DOMParser,
    XMLSerializer = require('xmldom').XMLSerializer;

parseXML = function(filename, type) {
  var parser = new DOMParser();
  parser.recordPositions = true;
  var doc = parser.parseFromString(String(fs.readFileSync(filename)), type);
  doc.documentURI = filename;
  return doc;
};

exports.parseXML = function(filename) {
  return parseXML(filename);
};

exports.parseXHTML = function(filename) {
  return parseXML(filename, "/xhtml");
};

function fillParameter(n, parameter) {
  switch (n.nodeType) {
    case n.TEXT_NODE:
    case n.COMMENT_NODE:
      if (parameter.replacement &&
          parameter.replacement.nodeType &&
          n.nodeType == n.TEXT_NODE) {
        if (n.data.indexOf(parameter.string) != -1) {
          var frag = n.ownerDocument.createDocumentFragment();
          var parts = n.data.split(parameter.string);
          parts.forEach(function(part, i) {
            if (i) {
              frag.appendChild(parameter.replacement.cloneNode(true));
            }
            if (part != '') {
              frag.appendChild(n.ownerDocument.createTextNode(part));
            }
          });
          exports.replace(n, frag);
        }
      } else {
        var replacement = parameter.replacement;
        if (replacement === void 0) replacement = '';
        n.data = n.data.replace(parameter.re, replacement);
      }
      break;

    case n.ELEMENT_NODE:
      var replacement = parameter.replacement;
      if (replacement === void 0) replacement = '';
      for (var i = 0; i < n.attributes.length; i++) {
        var attr = n.attributes.item(i);
        attr.value = attr.value.replace(parameter.re, replacement);
      }
      break;
  }

  n = n.firstChild;
  while (n) {
    var next = n.nextSibling;
    fillParameter(n, parameter);
    n = next;
  }
};

exports.parse = function(s, parameters) {
  var doc = new DOMParser().parseFromString('<div xmlns="http://www.w3.org/1999/xhtml">' + s + '</div>', '/xhtml');

  for (var k in parameters) {
    var replacement = parameters[k];
    if (Array.isArray(replacement)) {
      replacement = exports.fragment(replacement);
    }
    fillParameter(doc, { re: new RegExp('{{' + k + '}}', 'g'),
                         string: '{{' + k + '}}',
                         replacement: replacement });
  }

  var frag = doc.createDocumentFragment();
  while (doc.documentElement.firstChild) {
    frag.appendChild(doc.documentElement.firstChild);
  }

  if (frag.firstChild == frag.lastChild) {
    return frag.firstChild;
  }

  return frag;
};

exports.set = function(a) {
  var set = { };
  for (var i = 0; i < a.length; i++) {
    set[a[i]] = true;
  }
  return set;
};

exports.encode = function(s) {
  return s.replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/'/g, "&apos;")
          .replace(/"/g, "&quot;");
};

exports.extend = function(object, properties) {
  for (var p in properties) {
    object[p] = properties[p];
  }
};

exports.resolveURL = function(base, url) {
  if (!base) return url;
  if (url[0] == '/') throw "can't handle absolute paths";
  if (url.indexOf(':') != -1) return url;
  if (url[0] == '#') {
    return base.replace(/(#.*)?$/, url);
  }
  return base.replace(/[^\/]*$/, '') + url;
};

exports.forEachChild = function(n, localName, fn) {
  n = n.firstChild;
  while (n) {
    if (n.nodeType == n.ELEMENT_NODE && n.localName == localName) {
      fn(n);
    }
    n = n.nextSibling;
  }
};

exports.cloneChildren = function(n) {
  var fragment = n.ownerDocument.createDocumentFragment();
  n = n.firstChild;
  while (n) {
    fragment.appendChild(n.cloneNode(true));
    n = n.nextSibling;
  }
  return fragment;
};

exports.child = function(n, localName) {
  n = n.firstChild;
  while (n && n.localName != localName) {
    n = n.nextSibling;
  }
  return n;
};

exports.initialuc = function(s) {
  s = String(s);
  if (s == '') return '';
  return s.substring(0, 1).toUpperCase() + s.substring(1);
};

exports.replace = function(n, replacement) {
  n.parentNode.replaceChild(replacement, n);
};

exports.replaceWithChildren = function(n) {
  var doc = n.ownerDocument;
  var frag = doc.createDocumentFragment();
  var children = exports.children(n);
  children.forEach(frag.appendChild.bind(frag));
  n.parentNode.replaceChild(frag, n);
  return children;
};

exports.children = function(n) {
  var a = [];
  for (n = n.firstChild; n; n = n.nextSibling) {
    a.push(n);
  }
  return a;
};

exports.englishList = function(items) {
  if (!items.length) {
    return undefined;
  }
  var doc = items[0].ownerDocument;
  var frag = doc.createDocumentFragment();
  for (var i = 0; i < items.length; i++) {
    if (i != 0) {
      frag.appendChild(doc.createTextNode(i == items.length - 1 ? ' and ' : ', '));
    }
    frag.appendChild(items[i]);
  }
  return frag;
};

exports.list = function(items) {
  if (!items.length) {
    return undefined;
  }
  var doc = items[0].ownerDocument;
  var frag = doc.createDocumentFragment();
  for (var i = 0; i < items.length; i++) {
    if (i != 0) {
      frag.appendChild(doc.createTextNode(', '));
    }
    frag.appendChild(items[i]);
  }
  return frag;
};

exports.splitList = function(s) {
  if (!s) {
    return [];
  }
  return s.split(/,\s*/);
};

exports.values = function(object) {
  var a = [];
  for (var k in object) {
    a.push(object[k]);
  }
  return a;
};

function fragment() {
  return exports.parse('<div></div>').ownerDocument.createDocumentFragment();
}

exports.fragment = function(a, between) {
  if (!a || !a.length) return void 0;
  var frag = fragment();
  a.forEach(function(n, i) {
    if (n !== void 0) {
      if (i && between) {
        frag.appendChild(frag.ownerDocument.createTextNode(between));
      }
      if (typeof n == 'object' && n.nodeType) {
        frag.appendChild(n);
      } else {
        frag.appendChild(frag.ownerDocument.createTextNode(String(n)));
      }
    }
  });
  return frag;
};

exports.firstIndexOfAny = function(within, searchingFor) {
  for (var i = 0; i < searchingFor.length; i++) {
    var index = within.indexOf(searchingFor[i]);
    if (index != -1) {
      return true;
    }
  }
  return false;
};

exports.compare = function(s1, s2) {
  if (s1 == s2) return 0;
  return s1 < s2 ? -1 : 1;
};

exports.forEachNode = function(n, fn, stackfn, stackval) {
  stackval = stackfn && stackfn(n) || stackval;
  var a = fn(n, stackval);
  if (Array.isArray(a)) {
    a.forEach(function(n) { exports.forEachNode(n, fn, stackfn, stackval) });
  } else {
    n = n.firstChild;
    while (n) {
      var next = n.nextSibling;
      exports.forEachNode(n, fn, stackfn, stackval);
      n = next;
    }
  }
};

exports.warn = function(message, node) {
  exports.info('warning: ' + message, node);
};

exports.info = function(message, node) {
  if (node) {
    if (node.nodeType) {
      console.warn([node.ownerDocument.documentURI, node.lineNumber, node.columnNumber, ' ' + message].join(':'));
    } else {
      console.warn(node.concat(' ' + message));
    }
  } else {
    console.warn(message);
  }
};

exports.allEqual = function(a) {
  if (a.length == 0) {
    return true;
  }
  var x = a[0];
  for (var i = 1; i < a.length; i++) {
    if (a[i] != x) {
      return false;
    }
  }
  return true;
};
