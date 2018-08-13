var config = require('./config.js'),
    namespaces = require('./namespaces.js'),
    utils = require('./utils.js'),
    processing = require('./processing.js'),
    fs = require('fs'),
    DOMParser = require('xmldom').DOMParser;

var conf;

function syntax() {
  console.error('Usage: node publish.js options');
  console.error('');
  console.error('Options:');
  console.error('  --list-pages             Print the names of all pages of the specification.');
  console.error('  --list-nontoc-pages      Print the names of all non-ToC pages of the');
  console.error('                             specification.');
  console.error('  --list-toc-pages         Print the names of all ToC pages of the ');
  console.error('                             specification.');
  console.error('  --list-resources         Print the names of all resource files/directories');
  console.error('                             to be copied to the publish directory.');
  console.error('  --list-definition-files  Print the names of all referenced definition XML ');
  console.error('                             files.');
  console.error('  --list-external-links    Print all of the external links used in the ');
  console.error('                             specification.');
  console.error('  --lint                   Lints the specification and prints any problems.');
  console.error('  --build [PAGE ...]       Builds the specified pages, or all pages if');
  console.error('                             none specified.');
  console.error('  --build-single-page      Builds the single page version of the ');
  console.error('                             specification.');
  console.error('  --local-style            Link to local W3C style sheets rather than w3.org.');
  console.error('  --help                   Show this message.');
}

function parseOptions() {
  var opts = { rest: [] };
  for (var i = 2; i < process.argv.length; i++) {
    switch (process.argv[i]) {
      case '--list-pages':
        opts.listPages = true;
        opts.listPagesToC = true;
        opts.listPagesNonToC = true;
        break;
      case '--list-nontoc-pages':
        opts.listPages = true;
        opts.listPagesNonToC = true;
        break;
      case '--list-toc-pages':
        opts.listPages = true;
        opts.listPagesToC = true;
        break;
      case '--list-resources':
        opts.listResources = true;
        break;
      case '--list-definition-files':
        opts.listDefinitionFiles = true;
        break;
      case '--list-external-links':
        opts.listExternalLinks = true;
        break;
      case '--lint':
        opts.lint = true;
        break;
      case '--build':
        opts.build = true;
        break;
      case '--build-single-page':
        opts.buildSinglePage = true;
        break;
      case '--local-style':
        opts.localStyle = true;
        break;
      case '--help':
        opts.help = true;
        break;
      default:
        if (process.argv[i][0] == '-') {
          syntax();
          process.exit(1);
        }
        opts.rest.push(process.argv[i]);
    }
  }
  return opts;
}

function listPages(toc, nontoc) {
  function include(page) {
    if (page == conf.tocPage || page == conf.index) {
      return toc;
    }
    return nontoc;
  }

  console.log(conf.pageOrder.filter(include).join('\n'));
}

function listResources() {
  console.log(conf.resources.join('\n'));
}

function listDefinitionFiles() {
  console.log(conf.definitionFiles.join('\n'));
}

function gatherAllLinks() {
  var locs = conf.locations.concat(conf.definitions.locations);
  conf.pageOrder.forEach(function(page) {
    var doc = conf.getPageDocument(page);
    utils.forEachNode(doc, function(n) {
      if (n.nodeType != n.ELEMENT_NODE ||
          n.localName != 'a' ||
          !n.hasAttribute('href')) {
        return;
      }

      var href = processing.resolveSpecRelativeLink(conf, n);
      if (href) {
        locs.push([href, n.ownerDocument.documentURI, n.lineNumber, n.columnNumber]);
        return;
      }

      href = n.getAttribute('href');
      if (/^(.*):/.test(href) &&
          RegExp.$1 != 'http' &&
          RegExp.$1 != 'https') {
        return;
      }

      locs.push([href, n.ownerDocument.documentURI, n.lineNumber, n.columnNumber]);
    });
  });
  return locs.sort(function(a, b) {
      if (a[1] < b[1]) return -1;
      if (a[1] > b[1]) return 1;
      if (a[2] < b[2]) return -1;
      if (a[2] > b[2]) return 1;
      if (a[3] < b[3]) return -1;
      if (a[3] > b[3]) return 1;
      return 0;
    })
}

function listExternalLinks() {
  gatherAllLinks().forEach(function(l) {
    if (/\/\//.test(l[0])) {
      console.log([l[1], l[2], l[3], l[0]].join(':'));
    }
  });
}

function lint(pages) {
  function checkLocalLink(href, doc, n) {
    if (/^([^/]+)\.html$/.test(href)) {
      // link to a chapter
      if (conf.pageOrder.indexOf(RegExp.$1) == -1) {
        utils.info('broken link ' + href, n);
      }
    } else if (/^([^/]+)\.html#(.*)$/.test(href)) {
      // link to an anchor in a chapter
      var fragment = RegExp.$2;
      if (conf.pageOrder.indexOf(RegExp.$1) == -1) {
        utils.info('broken link ' + href, n);
      } else {
        var otherPage = conf.getPageDocument(RegExp.$1);
        if (!otherPage.getElementById(fragment)) {
          utils.info('broken link ' + href + ' (fragment not found)', n);
        }
      }
    } else if (/^#(.*)$/.test(href)) {
      if (!doc || !doc.getElementById(RegExp.$1)) {
        utils.info('broken link ' + href + ' (fragment not found)', n);
      }
    }
  }

  conf.definitions.locations.forEach(function(l) {
    checkLocalLink(l[0], conf.getPageDocument(conf.index), l.slice(1));
  });

  pages.forEach(function(page) {
    var doc = conf.getPageDocument(page);
    utils.forEachNode(doc, function(n) {
      if (n.nodeType != n.ELEMENT_NODE) {
        return;
      }

      if (/^h[2-6]$/.test(n.localName) &&
          !n.hasAttribute('id')) {
        utils.info('heading element must have an id="" attribute', n);
      }

      if (n.localName == 'a' &&
          n.hasAttribute('href')) {
        var href = n.getAttribute('href');
        checkLocalLink(href, doc, n);
      }
    });
  });
}

function checkAllPagesValid(pages) {
  for (var i = 0; i < pages.length; i++) {
    if (!conf.pages[pages[i]]) {
      var invalid = [pages[i]];
      while (++i < pages.length) {
        if (!conf.pages[pages[i]]) {
          invalid.push(pages[i]);
        }
      }
      console.error('error: unknown page' + (invalid.length > 1 ? 's' : '') + ' ' + invalid.join(' '));
      process.exit(1);
    }
  }
}

function buildPages(pages) {
  pages = pages || conf.pageOrder.concat();
  checkAllPagesValid(pages);
  lint(pages);
  pages.forEach(buildPage);
}

function buildPage(page) {
  var doc = conf.getPageDocument(page);
  var outputFilename = conf.outputDirectory + page + '.html';

  [processing.insertPageComment,
   processing.insertSpecNameInTitle,
   processing.insertStyleSheets,
   processing.insertMathJaxScript,
   processing.insertW3CScript,
   processing.addBodyClass,
   processing.addExpanderScript,
   processing.addTableOfContents,
   processing.addHeaderFooter,
   processing.processReplacements,
   processing.processLinks,
   processing.processSpecRelativeLinks,
   processing.addSectionNumbers,
   processing.addIssueIDs,
   processing.formatQuotes,
   // processing.formatIDL,
   processing.formatMarkup].forEach(function(fn) { fn(conf, page, doc); });

  fs.writeFileSync(outputFilename, doc.toString());
}

function buildSinglePage() {
  var outputFilename = conf.outputDirectory + 'single-page.html';
  var parser = new DOMParser();
  parser.recordPositions = true;

  // New document.
  var doc = parser.parseFromString('<html><head></head><body></body></html>');
  var head = doc.documentElement.firstChild;
  var body = doc.documentElement.lastChild;

  // Add HTML doctype.
  doc.insertBefore(doc.implementation.createDocumentType("html", "", ""), doc.firstChild);

  var foundMathjax = false;

  // Add the contents of each published chapter.
  for (var i = 0; i < conf.pageOrder.length; i++) {
    var page = conf.pageOrder[i];
    var pageDocument = utils.parseXHTML(conf.outputDirectory + page + '.html');
    var pageHead = utils.child(pageDocument.documentElement, 'head');
    var pageBody = utils.child(pageDocument.documentElement, 'body');
    if (i == 0) {
      // The <head> contents of the index are used for the single page document.
      head.appendChild(utils.cloneChildren(pageHead));
    } else {
      // Separate each page.
      body.appendChild(utils.parse('<hr class="chapter-divider"/>'));
    }

    utils.forEachNode(pageHead, function(n) {
      // Copy a <style> or <link data-keep=""> in any chapter's <head>
      // into the single page <head>.
      // Place before any other style sheets because we must not override
      // the W3C TR style sheets.
      if ((n.nodeName == 'style')||
          (n.nodeName == 'link' && n.hasAttribute('data-keep')) ) {
        var firstStyleSheet = head.getElementsByTagName('link')[0];
        head.insertBefore(n.cloneNode(true), firstStyleSheet);
      }
      // Note if Mathjax was used anywhere.
      if (n.nodeName == 'script' &&
          n.hasAttribute('data-script-mathjax')) {
        foundMathjax = true;
      }
    });

    // Clone the body of the chapter.
    var clonedPageBody = utils.cloneChildren(pageBody);

    // Fix up IDs so that they don't clash between chapters.
    utils.forEachNode(clonedPageBody, function(n) {
      if (n.nodeType == n.ELEMENT_NODE) {
        ['id', 'aria-describedby'].forEach(function(attr) {
          if (n.hasAttribute(attr) && !n.hasAttribute('data-never-rename')) {
            n.setAttribute(attr, page + '-' + n.getAttribute(attr));
          }
        });
        if (n.nodeName == 'a') {
          if (n.hasAttribute('name')) {
            n.setAttribute('name', page + '-' + n.getAttribute('name'));
          }
          if (n.hasAttribute('href')) {
            var href = n.getAttribute('href');
            if (href[0] == '#') {
              n.setAttribute('href', '#' + page + '-' + href.substring(1));
            } else if (href.match(/^([^\/]+)\.html#(.*)$/)) {
              n.setAttribute('href', '#' + RegExp.$1 + '-' + RegExp.$2);
            } else if (href.match(/^([^\/]+)\.html$/) && RegExp.$1 != 'single-page') {
              n.setAttribute('href', '#chapter-' + RegExp.$1);
            }
          }
        }
      }
    });

    // Copy the chapter in.
    body.appendChild(utils.parse('<div id="chapter-{{page}}" class="{{classes}}">{{pagebody}}</div>',
                                 { page: page,
                                   classes: pageBody.getAttribute('class'),
                                   pagebody: clonedPageBody }));
  }

  // Remove all references to expanders.js and fixup.js.
  utils.forEachNode(doc, function(n) {
    if (
      n.nodeName == 'script' &&
      (
        n.getAttribute('src') == 'style/expanders.js' || 
        n.getAttribute('src') == '//www.w3.org/scripts/TR/2016/fixup.js'
      )
    ) {
      n.parentNode.removeChild(n);
    }
  });

  // Add one reference at the end of the document.
  body.appendChild(utils.parse('<script src="style/expanders.js"></script>'));
  body.appendChild(utils.parse('<script src="//www.w3.org/scripts/TR/2016/fixup.js"></script>'));

  // Add reference to mathjax if we found one in any chapter.
  if (foundMathjax) {
    head.appendChild( processing.getMathJaxScript() );
  }

  fs.writeFileSync(outputFilename, doc.toString());
}

/*
// Hacky function to do some automatic reformatting of source files.
function x() {
  function isBlock(n) {
    return n.localName == "div" ||
           n.localName == "dl" ||
           n.localName == "dt" ||
           n.localName == "dd" ||
           n.localName == "p" ||
           n.localName == "ul" ||
           n.localName == "ol" ||
           n.localName == "li" ||
           n.localName == "pre";
  }

  function reformat(n, level) {
    var indent = "", indentMinusOne = "", indentMinusTwo = "", indentPlusOne = "";
    for (var i = 0; i < level - 2; i++) {
      indentMinusTwo += "  ";
    }
    for (var i = 0; i < level - 1; i++) {
      indentMinusOne += "  ";
    }
    for (var i = 0; i < level; i++) {
      indent += "  ";
    }
    for (var i = 0; i < level + 1; i++) {
      indentPlusOne += "  ";
    }

    if (n.nodeType == n.TEXT_NODE) {
      var s = n.textContent;
      s = s.replace(/\n\n\n+/g, "\n\n");
      if (!n.previousSibling && n.parentNode.getAttribute("class") != "idl-type-parenthetical") {
        s = s.replace(/^\s+/, "");
      }
      s = s.replace(/\n *(\S)/g, function() { return "\n" + indentMinusTwo + RegExp.$1; });
      if (!n.nextSibling) {
        s = s.replace(/\s+$/, "");
      }
      if (s == "") {
        n.parentNode.removeChild(n);
      } else {
        utils.replace(n, n.ownerDocument.createTextNode(s));
      }
    }

    if (n.nodeType != n.ELEMENT_NODE) {
      return;
    }

    if (n.localName == "pre") {
      return;
    }

    for (var c = n.firstChild; c; c = c.nextSibling) {
      var nextLevel;
      if (c.nodeType == c.ELEMENT_NODE &&
          (c.localName == "with" ||
           (c.localName == "div" && c.hasAttribute("class") && /ready-for/.test(c.getAttribute("class"))) ||
           !isBlock(c))) {
        nextLevel = level;
      } else {
        nextLevel = level + 1;
      }
      reformat(c, nextLevel);
    }

    if (n.localName == "with") {
      if (n.firstChild) {
        if (n.firstChild.nodeType == n.TEXT_NODE) {
          n.firstChild.data = "\n\n" + n.firstChild.data;
        } else {
          n.insertBefore(n.ownerDocument.createTextNode("\n\n"), n.firstChild);
        }
      }
      if (n.lastChild) {
        if (n.lastChild.nodeType == n.TEXT_NODE) {
          n.lastChild.data += "\n\n";
        } else {
          n.appendChild(n.ownerDocument.createTextNode("\n\n"));
        }
      }
    } else if (isBlock(n)) {
      if (n.firstChild && n.firstChild.nodeType == n.TEXT_NODE && /^\s+$/.test(n.firstChild.data)) {
        n.firstChild.data = "\n" + indent;
      } else if (n.firstChild && n.firstChild.nodeType == n.ELEMENT_NODE && isBlock(n.firstChild)) {
        n.insertBefore(n.ownerDocument.createTextNode("\n" + indent), n.firstChild);
      }
      if (n.nextSibling && n.nextSibling.nodeType == n.TEXT_NODE && /^\s+$/.test(n.nextSibling) && n.nextSibling.nextSibling && isBlock(n.nextSibling.nextSibling)) {
        n.parentNode.removeChild(n.nextSibling);
      }
      if (n.nextSibling && n.nextSibling.nodeType == n.TEXT_NODE && /^\s+$/.test(n.nextSibling) && !n.nextSibling.nextSibling) {
        n.appendChild(n.ownerDocument.createTextNode("\n" + indentMinusOne));
      }
      if (n.nextSibling && n.nextSibling.nodeType == n.ELEMENT_NODE && isBlock(n.nextSibling)) {
        n.parentNode.insertBefore(n.ownerDocument.createTextNode("\n" + indentMinusOne), n.nextSibling);
      }
      if (n.lastChild && n.lastChild.nodeType == n.ELEMENT_NODE && isBlock(n.lastChild)) {
        n.appendChild(n.ownerDocument.createTextNode("\n" + indentMinusOne));
      }
    }
    if (n.lastChild && n.lastChild.previousSibling && n.lastChild.nodeType == n.TEXT_NODE && n.lastChild.previousSibling.nodeType == n.TEXT_NODE) {
      n.lastChild.previousSibling.data += n.lastChild.data;
      n.removeChild(n.lastChild);
    }
    if (n.previousSibling && n.previousSibling.nodeType == n.TEXT_NODE) {
      n.previousSibling.data = n.previousSibling.data.replace(/\n *$/, "\n" + indentMinusOne);
    }
    if (n.lastChild && n.lastChild.nodeType == n.TEXT_NODE && /\S/.test(n.lastChild.data)) {
      n.lastChild.data = n.lastChild.data.replace(/\s+$/, "");
    }
  }

  conf.pageOrder.forEach(function(page) {
    var doc = utils.parseXHTML(page + '.html');

    // Format the document from the "DOMInterfaces" element onwards.
    var h2 = doc.getElementById("DOMInterfaces") || doc.getElementById("idl") || doc.getElementById("BasicDOMInterfaces");
    if (!h2) {
      return;
    }

    for (var n = h2.nextSibling; n; n = n.nextSibling) {
      reformat(n, 0);
    }

    fs.writeFileSync(page + ".html.new", doc.toString());
  });
}
*/

var opts = parseOptions();
if (opts.help || (!!opts.listPages + !!opts.listResources + !!opts.listDefinitionFiles + !!opts.listExternalLinks + !!opts.lint + !!opts.build + !!opts.buildSinglePage) != 1) {
  syntax();
  process.exit(opts.help ? 0 : 1);
} else {
  conf = config.load('publish.xml');
  conf.localStyleSheets = opts.localStyle;
  if (opts.listPages) {
    listPages(opts.listPagesToC, opts.listPagesNonToC);
  } else if (opts.listResources) {
    listResources();
  } else if (opts.listDefinitionFiles) {
    listDefinitionFiles();
  } else if (opts.listExternalLinks) {
    listExternalLinks();
  } else if (opts.lint) {
    lint(conf.pageOrder);
  } else if (opts.build) {
    buildPages(opts.rest);
  } else if (opts.buildSinglePage) {
    buildSinglePage();
  }
}
