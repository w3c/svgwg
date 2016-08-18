// config.js
//
// Reads a publish.xml file for publication configuration.

var utils = require('./utils.js'),
    assert = require('assert'),
    maturities = require('./maturities.js'),
    definitions = require('./definitions.js'),
    namespaces = require('./namespaces.js');

function child(node, nodeName) {
  var n = node.firstChild;
  while (n && n.nodeName != nodeName) {
    n = n.nextSibling;
  }
  return n;
}

function children(node, nodeName) {
  var ns = [];
  var n = node.firstChild;
  while (n) {
    if (n.nodeName == nodeName) {
      ns.push(n);
    }
    n = n.nextSibling;
  }
  return ns;
}

function attr(node, nodeName, attrName, def) {
  var n = child(node, nodeName);
  return n && n.getAttribute(attrName) || def;
}

function text(node, nodeName, def) {
  var n = child(node, nodeName);
  return n && n.textContent || def;
}

function gatherSections(conf, page) {
  function appendToHierarchy(section) {
    var children = sectionHierarchy[sectionHierarchy.length - 1].children;
    children.push({ section: section, s: section.number + ": " + section.titleText });
  }

  function pushHierarchy() {
    var lastChild;
    if (sectionHierarchy.length) {
      var children = sectionHierarchy[sectionHierarchy.length - 1].children;
      lastChild = children[children.length - 1];
    } else {
      lastChild = { };
    }
    lastChild.children = [];
    sectionHierarchy.push(lastChild);
  }

  function popHierarchy(count) {
    while (count > 0) {
      sectionHierarchy.pop();
      count--;
    }
  }

  function gather(n) {
    if (n.nodeType == 1) {
      var id = n.getAttribute("id");
      if (/^h[2-6]$/.test(n.nodeName) &&
          n.getAttributeNS(namespaces.edit, 'toc') != 'no' &&
          id != 'pagetitle' &&
          id != 'pagesubtitle' &&
          id != 'abstract' &&
          id != 'status' &&
          id != 'toc' &&
          id != 'contents') {
        var level = n.nodeName.substring(1) - 1;
        if (section.length >= level - 1) {
          if (section.length == level - 1) {
            section.push(0);
            pushHierarchy();
          } else {
            popHierarchy(section.length - level);
          }
          section.length = level;
          section[level - 1]++;
          var sectionInfo = {
            number: section.join('.'),
            title: utils.cloneChildren(n),
            id: id
          };
          sectionInfo.titleText = sectionInfo.title.textContent;
          conf.pages[page].sections[id] = sectionInfo;
          appendToHierarchy(sectionInfo);
        }
      } else {
        n = n.firstChild;
        while (n) {
          gather(n);
          n = n.nextSibling;
        }
      }
    }
  }

  var doc = conf.getPageDocument(page);
  var section = [];
  var sectionHierarchy = [];
  conf.pages[page].sections = { };
  gather(doc.documentElement);
  conf.pages[page].sectionHierarchy = sectionHierarchy[0] || null;
}

function Config(filename) {
  var doc = utils.parseXML(filename);
  var root = doc.documentElement;
  this.title = text(root, 'title');
  this.shortTitle = text(root, 'short-title');
  this.maturity = text(root, 'maturity');

  this.usePublishDirectory = attr(root, 'output', 'use-publish-directory') == 'true';
  this.publishDirectory = attr(root, 'output', 'publish-directory');

  var pubDate = text(root, 'publication-date')
  this._publicationDate = new Date;
  if (pubDate) {
    var dateParts = pubDate.split('-');
    this._publicationDate.setUTCFullYear(dateParts[0]);
    this._publicationDate.setUTCMonth(dateParts[1] - 1, 1);
    this._publicationDate.setUTCDate(dateParts[2]);
  }

  var locs = this.locations = [];
  var vers = this.versions = { };

  var versions = child(root, 'versions');
  ['cvs', 'cvs-single', 'this', 'this-single', 'previous', 'latest', 'latestRec'].forEach(function(name) {
    var key = name.replace(/-[a-z]/, function(s) { return s.substr(1).toUpperCase(); });
    vers[key] = attr(versions, name, 'href');
    if (vers[key]) {
      var e = child(versions, name);
      locs.push([vers[key], e.ownerDocument.documentURI, e.lineNumber, e.columnNumber]);
    }
  });

  this.toc = attr(root, 'toc', 'href');
  this.elementIndex = attr(root, 'elementindex', 'href');
  this.attributeIndex = attr(root, 'attributeindex', 'href');
  this.propertyIndex = attr(root, 'propertyindex', 'href');

  this.specs = { };

  var definitionInfos = [];
  this.definitionFiles = [];
  for (var n = root.firstChild; n; n = n.nextSibling) {
    if (n.nodeName == 'definitions') {
      var specid = n.getAttribute('specid') || null;
      var base = n.getAttribute('base') || null;
      var href = n.getAttribute('href') || null;
      definitionInfos.push({
        href: href,
        base: base,
        specid: specid,
        mainspec: n.getAttribute('mainspec') || null
      });
      if (specid && base) {
        this.specs[specid] = base;
      }
      if (base) {
        locs.push([base, n.ownerDocument.documentURI, n.lineNumber, n.columnNumber]);
      }
      if (href) {
        this.definitionFiles.push(href);
      }
    }
  }
  var allDefinitions = definitions.load(definitionInfos);
  this.definitions = allDefinitions.definitions;
  this.definitionsBySpec = allDefinitions.definitionsBySpec;
  this.definitionMainSpecs = allDefinitions.mainSpecs;

  this.resources = [];
  for (var n = root.firstChild; n; n = n.nextSibling) {
    if (n.nodeName == 'resource') {
      this.resources.push(n.getAttribute('href'));
    }
  }

  this.interfacesFile = attr(root, 'interfaces', 'idl');
  this.pages = { };
  this.pageOrder = [];

  var chapter = 1, appendix = 1;
  for (var n = root.firstChild; n; n = n.nextSibling) {
    if (n.nodeType != 1) continue;
    var name = n.getAttribute('name');
    switch (n.nodeName) {
      case 'index':
        this.index = name;
        this.pages[name] = {
          type: 'index'
        };
        break;
      case 'page':
        this.pages[name] = {
          type: 'page'
        };
        if (n.getAttribute('toc') == 'true') {
          this.tocPage = name;
          this.pages[name].toc = true;
        }
        break;
      case 'chapter':
        var number = chapter++;
        this.pages[name] = {
          type: 'chapter',
          number: number,
          formattedNumber: String(number)
        };
        break;
      case 'appendix':
        var number = appendix++;
        this.pages[name] = {
          type: 'appendix',
          number: number,
          formattedNumber: String.fromCharCode(64 + number)
        };
        break;
      default:
        continue;
    }
    this.pageOrder.push(name);
  }
}

Config.prototype = {
  get shortMaturity() {
    return maturities[this.maturity].short;
  },

  get longMaturity() {
    return maturities[this.maturity].long;
  },

  get publicationYear() {
    return this._publicationDate.getUTCFullYear();
  },

  get publicationDate() {
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var d = this._publicationDate;
    return (d.getUTCDate() < 10 ? '0' : '') + d.getUTCDate() + ' ' + months[d.getUTCMonth()] + ' ' + d.getUTCFullYear();
  },

  get thisVersion() {
    return this.maturity == 'ED' ? this.versions.cvs : this.versions['this'];
  },

  get thisVersionSingle() {
    return this.maturity == 'ED' ? this.versions.cvsSingle : this.versions.thisSingle;
  },

  get outputDirectory() {
    if (!this.usePublishDirectory) {
      return '../';
    }
    if (this.publishDirectory) {
      return '../' + this.publishDirectory + '/';
    }
    return '../publish/';
  },

  get isSingleChapter() {
    return this.pageOrder.length == 1;
  },

  getPageDocument: function(page) {
    if (!this.pages[page].document) {
      var doc = utils.parseXHTML(page + '.html');
      Object.defineProperty(doc, 'head', { get: function() { return this.getElementsByTagName('head').item(0); } });
      Object.defineProperty(doc, 'body', { get: function() { return this.getElementsByTagName('body').item(0); } });
      this.pages[page].document = doc;
    }
    return this.pages[page].document;
  },

  getSectionHierarchy: function(page) {
    if (this.pages[page].sectionHierarchy === void 0) {
      gatherSections(this, page);
    }

    return this.pages[page].sectionHierarchy;
  },

  lookupElementBySpec: function(specid, elementName) {
    var element = this.definitionsBySpec[specid].elements[elementName];
    if (!element) {
      for (var id in this.definitionMainSpecs) {
        if (this.definitionMainSpecs[id] == specid) {
          element = this.definitionsBySpec[id].elements[elementName];
          if (element) {
            break;
          }
        }
      }
    }
    return element;
  },

  lookupElementAttributeBySpec: function(specid, elementName, attributeName) {
    var element = this.definitionsBySpec[specid].elements[elementName];
    if (!element || !element.attributes[attributeName]) {
      for (var id in this.definitionMainSpecs) {
        if (this.definitionMainSpecs[id] == specid) {
          element = this.definitionsBySpec[id].elements[elementName];
          if (element && element.attributes[attributeName]) {
            break;
          }
        }
      }
    }
    return element && element.attributes[attributeName];
  },

  lookupElementAttributeCategoryBySpec: function(specid, elementName, attributeCategoryName) {
    var element = this.definitionsBySpec[specid].elements[elementName];
    if (element) {
      for (var i = 0; i < element.attributeCategories.length; i++) {
        var catName = element.attributeCategories[i];
        if (catName == attributeCategoryName) {
          return this.definitionsBySpec[specid].attributeCategories[catName];
        }
      }
    }
  },
};

exports.load = function(filename) {
  return new Config(filename);
};
