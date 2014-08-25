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
  console.error('  --list-pages            Print the names of all pages of the specification.');
  console.error('  --list-resources        Print the names of all resource files/directories');
  console.error('                            to be copied to the publish directory.');
  console.error('  --build [PAGE ...]      Builds the specified pages, or all pages if');
  console.error('                            none specified.');
  console.error('  --build-single-page     Builds the single page version of the specification.');
  console.error('  --local-style           Link to local W3C style sheets rather than w3.org.');
  console.error('  --help                  Show this message.');
}

function parseOptions() {
  var opts = { rest: [] };
  for (var i = 2; i < process.argv.length; i++) {
    switch (process.argv[i]) {
      case '--list-pages':
        opts.listPages = true;
        break;
      case '--list-resources':
        opts.listResources = true;
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

function listPages() {
  console.log(conf.pageOrder.join('\n'));
}

function listResources() {
  console.log(conf.resources.join('\n'));
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
  pages.forEach(buildPage);
}

function buildPage(page) {
  var doc = conf.getPageDocument(page);
  var outputFilename = conf.outputDirectory + page + '.html';

  [processing.insertPageComment,
   processing.insertSpecNameInTitle,
   processing.insertStyleSheets,
   processing.insertMathJaxScript,
   processing.addBodyClass,
   processing.addHeaderFooter,
   processing.addExpanderScript,
   processing.addTableOfContents,
   processing.processReplacements,
   processing.processLinks,
   processing.addSectionNumbers,
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
      // Copy a <style> in any chapter's <head> into the single page <head>.
      if (n.nodeName == 'style') {
        head.appendChild(n.cloneNode(true));
      }
      // Note if Mathjax was used anywhere.
      if (n.nodeName == 'script' &&
          n.getAttribute('src') == 'style/load-mathjax.js') {
        foundMathjax = true;
      }
    });

    // Clone the body of the chapter.
    var clonedPageBody = utils.cloneChildren(pageBody);

    // Fix up IDs so that they don't clash between chapters.
    utils.forEachNode(clonedPageBody, function(n) {
      if (n.nodeType == n.ELEMENT_NODE) {
        ['id', 'aria-describedby'].forEach(function(attr) {
          if (n.hasAttribute(attr)) {
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

  // Remove all references to expanders.js.
  utils.forEachNode(doc, function(n) {
    if (n.nodeName == 'script' &&
        n.getAttribute('src') == 'style/expanders.js') {
      n.parentNode.removeChild(n);
    }
  });

  // Add one reference to expanders.js at the end of the document.
  body.appendChild(utils.parse('<script src="style/expanders.js"></script>'));

  // Add reference to load-mathjax.js if we found one in any chapter.
  if (foundMathjax) {
    head.appendChild(utils.parse('<script src="style/load-mathjax.js"></script>'));
  }

  fs.writeFileSync(outputFilename, doc.toString());
}

var opts = parseOptions();
if (opts.help || (!!opts.listPages + !!opts.listResources + !!opts.build + !!opts.buildSinglePage) != 1) {
  syntax();
  process.exit(opts.help ? 0 : 1);
} else {
  conf = config.load('publish.xml');
  conf.localStyleSheets = opts.localStyle;
  if (opts.listPages) {
    listPages();
  } else if (opts.listResources) {
    listResources();
  } else if (opts.build) {
    buildPages(opts.rest);
  } else if (opts.buildSinglePage) {
    buildSinglePage();
  }
}
