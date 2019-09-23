var namespaces = require('./namespaces.js'),
    utils = require('./utils.js'),
    fs = require('fs');

// -- Add HTML comment at the top of the page ---------------------------------

exports.insertPageComment = function(conf, page, doc) {
  var pageTitle = doc.getElementsByTagName('title')[0].textContent;
  var pageType = utils.initialuc(conf.pages[page].type);
  var masterDirectory = conf.usePublishDirectory ? '../master/' : '../';
  var subtitle = '';
  if (pageType == 'Chapter' || pageType == 'Appendix') {
    subtitle = '\n  ' + pageType + ' ' + conf.pages[page].formattedNumber + ': ' + pageTitle;
  }

  var comment = utils.parse('\n\n<!--\n  {{title}}{{subtitle}}\n\n  Note: This document is generated from {{source}}.\n  Run "make" from the root of the repository to regenerate it.\n  -->\n\n',
                            { title: conf.title,
                              subtitle: subtitle,
                              source: masterDirectory + page + '.html' });

  doc.insertBefore(comment, doc.documentElement);
}


// -- Include the specification name in the page's <title> --------------------

exports.insertSpecNameInTitle = function(conf, page, doc) {
  if (conf.index == page) {
    return;
  }

  doc.getElementsByTagName('title')[0].textContent += ' — ' + conf.shortTitle;
};

// -- Link to the document and W3C style sheet for the document's maturity ---

exports.insertStyleSheets = function(conf, page, doc) {
  // Remove existing stylesheet links, unless marked with a data-keep attribute.
  for (var next, n = doc.head.firstChild; n; n = next) {
    next = n.nextSibling;
    if (n.nodeName == 'link' &&
        /\bstylesheet\b/.test(n.getAttribute('rel')) &&
        !n.hasAttribute('data-keep') ) {
      n.parentNode.removeChild(n);
    }
  }

  var isSVG2 = conf.shortTitle == 'SVG 2';
  // Add a link to the default style sheet.
  doc.head.appendChild(utils.parse('<link rel="stylesheet" title="Default" href="{{href}}" type="text/css" media="screen"/>',
                                   { href: conf.maturity == 'ED' && isSVG2 ? 'style/svg.css' : 'style/default_no_maturity.css' }));

  if (isSVG2) {
    // Add a link to alternate style sheet to hide background colors
    // if this is an Editor's Draft, or to show them otherwise.
    doc.head.appendChild(utils.parse('<link rel="alternate stylesheet" title="{{title}}" href="{{href}}" type="text/css" media="screen"/>',
                                     { href: conf.maturity == 'ED' ? 'style/default_no_maturity.css' : 'style/svg.css',
                                       title: conf.maturity == 'ED' ? 'Only annotations for publication' : 'All annotations' }));
  }

  // Add a link to the "no issues/annotations" style sheet.
  doc.head.appendChild(utils.parse('<link rel="alternate stylesheet" title="No issues/annotations" href="style/default_no_issues.css" type="text/css" media="screen"/>'));

  // Add a link to a local or remote W3C TR style sheet for this document's maturity.
  var href = 'W3C-' + conf.shortMaturity;
  if (conf.localStyleSheets) {
    href = 'style/' + href + '.css';
  } else {
    href = '//www.w3.org/StyleSheets/TR/2016/' + href;
    if (conf.maturity != 'ED') {
      href = 'https:' + href;
    }
  }
  doc.head.appendChild(utils.parse('<link rel="stylesheet" href="{{href}}" type="text/css" media="screen"/>',
                                   { href: href }));

  if (conf.maturity == 'ED') {
    // Add <script> to fix up protocol-relative style sheet links when viewed over file:.
    doc.head.appendChild(utils.parse('<script src="style/link-fixup.js"></script>'));
  }
};


// -- Insert link to MathJax script on pages that have math -------------------

function hasMathElements(n) {
  if (n.namespaceURI == namespaces.mathml) {
    return true;
  }

  n = n.firstChild;
  while (n) {
    if (hasMathElements(n)) {
      return true;
    }
    n = n.nextSibling;
  }

  return false;
}

exports.getMathJaxScript = function() {
  return utils.parse('<script data-script-mathjax="" async="" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"></script>')
}

exports.insertMathJaxScript = function(conf, page, doc) {
  if (hasMathElements(doc)) {
    doc.head.appendChild( exports.getMathJaxScript() );
  }
}

exports.insertW3CScript = function(conf, page, doc) {
  // Load the W3C TR script.
  if (conf.localStyleSheets) {
    doc.body.appendChild(utils.parse('<script src="style/fixup.js"></script>'));
  } else {
    doc.body.appendChild(utils.parse('<script src="//www.w3.org/scripts/TR/2016/fixup.js"></script>'));
  }
}

// -- Set class="" on <body> to indicate which chapter this is ----------------

exports.addBodyClass = function(conf, page, doc) {
  if (doc.body.hasAttribute('class')) {
    doc.body.setAttribute('class', doc.body.getAttribute('class') + ' chapter-' + page);
  } else {
    doc.body.setAttribute('class', 'chapter-' + page);
  }
}


// -- Add header and footer links to next/previous chapter, etc. --------------

exports.addHeaderFooter = function(conf, page, doc) {
  if (conf.isSingleChapter) {
    return;
  }

  var index = conf.pageOrder.indexOf(page);
  var previous = conf.pageOrder[index - 1];
  var next = conf.pageOrder[index + 1];

  var markup = '<div class="header {{side}}">';

  if (conf.toc)            markup += '<a href="Overview.html">Overview</a>';
  if (previous)            markup += ' · <a href="{{previous}}.html">Previous</a>';
  if (next)                markup += ' · <a href="{{next}}.html">Next</a>';
  if (conf.elementIndex)   markup += ' · <a href="{{elementIndex}}">Elements</a>';
  if (conf.attributeIndex) markup += ' · <a href="{{attributeIndex}}">Attributes</a>';
  if (conf.propertyIndex)  markup += ' · <a href="{{propertyIndex}}">Properties</a>';

  markup += "</div>";

  function header() {
    return utils.parse(markup, { shortTitle: conf.shortTitle,
                                 publicationDate: conf.publicationDate,
                                 index: conf.index,
                                 toc: conf.toc,
                                 elementIndex: conf.elementIndex,
                                 attributeIndex: conf.attributeIndex,
                                 propertyIndex: conf.propertyIndex,
                                 previous: previous,
                                 next: next });
  }

  function getChildNodeById(parent, id) {
    var n = parent.firstChild;
    while (n != null) {
      if (n.nodeType === n.ELEMENT_NODE && n.getAttribute('id') === id)
          return n;
      n = n.nextSibling;
    }
  }

  if (conf.pages[page].type != 'index') {
    var toc = getChildNodeById(doc.body, 'toc');
    if (toc) {
      toc.insertBefore(header(), toc.firstChild);
    }
  }
}


// -- Add script for "expand >>" links in element summary tables --------------

function hasElementSummaryTables(n) {
  if (n.nodeType == n.ELEMENT_NODE &&
      n.localName == 'elementsummary') {
    return true;
  }

  n = n.firstChild;
  while (n) {
    if (hasElementSummaryTables(n)) {
      return true;
    }
    n = n.nextSibling;
  }

  return false;
}

exports.addExpanderScript = function(conf, page, doc) {
  if (!hasElementSummaryTables(doc)) {
    return;
  }

  doc.body.appendChild(utils.parse('<script src="style/expanders.js" type="text/javascript"></script>'));
}


// -- Add chapter number to <h1> and Table of Contents below it ---------------

function generateTOC(conf, page, className) {
  function newTOCOL() {
    return utils.parse('<ol class="{{class}}"></ol>', { class: className });
  }

  function generate(ol, children) {
    for (var i = 0; i < children.length; i++) {
      var item = children[i];
      var li = utils.parse('<li><a href="{{url}}#{{id}}"></a></li>',
                           { url: conf.isSingleChapter ? '' : page + '.html',
                             id: item.section.id });
      var a = li.firstChild;
      if (conf.pages[page].type == 'chapter' || 
          conf.pages[page].type == 'appendix' ||
          conf.isSingleChapter) {
        a.appendChild(utils.parse('<span class="secno">{{number}}{{section}}.</span> ',
                                  { number: conf.isSingleChapter ? '' : conf.pages[page].formattedNumber + '.',
                                    section: item.section.number }));
      }
      a.appendChild(item.section.title.cloneNode(true));
      if (item.children) {
        var childUL = newTOCOL();
        generate(childUL, item.children);
        if (childUL.firstChild) {
          li.appendChild(childUL);
        }
      }
      ol.appendChild(li);
    }
  }

  var ol = newTOCOL();
  var sectionHierarchy = conf.getSectionHierarchy(page);
  if (sectionHierarchy && sectionHierarchy.children) {
    generate(ol, sectionHierarchy && sectionHierarchy.children);
  }
  return ol;
}

exports.addTableOfContents = function(conf, page, doc) {
  var pageType = conf.pages[page].type;
  if (pageType != 'chapter' && pageType != 'appendix') {
    return;
  }

  var h1 = doc.getElementsByTagName('h1').item(0);
  if (!h1) {
    return;
  }

  h1.insertBefore(utils.parse('{{type}} {{number}}: ',
                              { type: utils.initialuc(pageType),
                                number: conf.pages[page].formattedNumber }),
                  h1.firstChild);

  var sections = conf.getSectionHierarchy(page);
  var toc;
  if (!sections || !sections.children.length) {
    toc = utils.parse('<nav id="toc"></nav>');
  }
  else {
    var tocClass = pageType == 'appendix' ? 'toc appendix-toc' : 'toc';

    toc = utils.parse(
      '<nav id="toc">' +
        '<h2 id="Contents" class="contents">Contents</h2>' +
        '<ol class="{{class}}"><li>{{toc}}</li></ol>' +
      '</nav>', { class: tocClass, toc: generateTOC(conf, page, tocClass) });
  }

  h1.parentNode.insertBefore(toc, h1.nextSibling);
}


// -- Add section numbers to heading elements ---------------------------------

exports.addSectionNumbers = function(conf, page, doc) {
  utils.forEachNode(doc, function(n) {
    if (n.nodeType == n.ELEMENT_NODE &&
        /^h[2-6]$/.test(n.localName) &&
        n.getAttribute('toc') != 'no') {
      var id = n.getAttribute('id');
      if (id && conf.pages[page].sections && conf.pages[page].sections[id]) {
        n.insertBefore(utils.parse('{{number}}{{section}}. ',
                                   { number: conf.isSingleChapter ? '' : (conf.pages[page].formattedNumber + '.'),
                                     section: conf.pages[page].sections[id].number }),
                       n.firstChild);
        var cls = n.getAttribute('class') || '';
        if (cls != '') {
          cls += ' ';
        }
        cls += 'heading';
        n.setAttribute('class', cls);
        n.appendChild(utils.parse('<a class="self-link" href="#' + id + '"></a>'));
      }
    }
  });
}

// -- Add id="" attributes to spec issues -------------------------------------

exports.addIssueIDs = function(config, page, doc) {
  utils.forEachNode(doc, function(n) {
    if (n.nodeType == n.ELEMENT_NODE) {
      var issue = n.getAttribute("data-issue");
      if (issue) {
        var id = "issue" + issue;
        n.setAttribute("id", id);
        n.insertBefore(utils.parse('<a class="self-link" href="#' + id + '"></a>'),
                       n.firstChild);
      }
    }
  });
}

// -- Process edit:* element replacements -------------------------------------

function doMiniTOC(conf, page, n) {
  var ul = utils.parse('<ol class="toc"></ol>');

  for (var i = 0; i < conf.pageOrder.length; i++) {
    var pageName = conf.pageOrder[i];
    if (conf.index == pageName) {
      continue;
    }

    var pageType = conf.pages[pageName].type;
    var h1 = conf.getPageDocument(pageName).getElementsByTagName('h1')[0];
    var li;
    switch (pageType) {
      case 'page':
        li = utils.parse('<li class="no-num"><a href="{{name}}.html">{{title}}</a></li>',
                         { name: pageName,
                           title: h1 && h1.textContent });
        break;
      case 'chapter':
        li = utils.parse('<li><a href="{{name}}.html"><span class="secno">{{number}}.</span> {{title}}</a></li>',
                         { name: pageName,
                           number: conf.pages[pageName].formattedNumber,
                           title: h1 && h1.textContent });
        break;
      case 'appendix':
        li = utils.parse('<li><a href="{{name}}.html">Appendix {{number}}: {{title}}</a></li>',
                         { name: pageName,
                           number: conf.pages[pageName].formattedNumber,
                           title: h1 && h1.textContent });
        break;
    }
    
    if (li) {
      ul.appendChild(li);
    }
  }

  utils.replace(n, ul);
}

function doFullTOC(conf, page, n) {
  var ul;

  if (conf.isSingleChapter) {
    ul = generateTOC(conf, page, 'toc');
  } else {
    ul = utils.parse('<ol class="toc"></ol>');
    for (var i = 0; i < conf.pageOrder.length; i++) {
      var pageName = conf.pageOrder[i];
      var pageType = conf.pages[pageName].type;
      if (pageType != 'page' && pageType != 'chapter' && pageType != 'appendix' ||
          conf.pages[pageName].toc) {
        continue;
      }

      var h1 = conf.getPageDocument(pageName).getElementsByTagName('h1')[0];
      var li = utils.parse('<li><a href="{{page}}.html">{{title}}</a></li>',
                           { page: pageName,
                             title: h1 && h1.textContent });

      if (pageType == 'chapter') {
        li.insertBefore(utils.parse('<span class="secno">{{number}}.</span> ',
                                    { number: conf.pages[pageName].formattedNumber }),
                        li.firstChild);
      } else if (pageType == 'appendix') {
        li.firstChild.insertBefore(utils.parse('Appendix {{number}}: ',
                                               { number: conf.pages[pageName].formattedNumber }),
                                   li.firstChild.firstChild);
      }

      if (pageType != 'page') {
        var pageTOC = generateTOC(conf, pageName, 'toc');
        if (pageTOC.firstChild) {
          li.appendChild(pageTOC);
        }
      }

      ul.appendChild(li);
    }
  }

  utils.replace(n, ul);
}

function doCompleteIDL(conf, page, n) {
  var idl = [];
  conf.pageOrder.forEach(function(p) {
    var doc = conf.getPageDocument(p);
    utils.forEachNode(doc, function(n) {
      if (n.nodeType == n.ELEMENT_NODE &&
          n.localName == "pre" &&
          /\bidl\b/.test(n.getAttribute("class")) ) {        
        if (n.svg_excludefromidl||n.hasAttribute("edit:excludefromidl")) {
          delete n.svg_excludefromidl;
          return;
        }
        if (idl.length) {
          idl.push(n.ownerDocument.createTextNode("\n\n"));
        }
        var clone = utils.cloneChildren(n);
        utils.forEachNode(clone, function(n) {
          if (n.nodeType == n.ELEMENT_NODE) {
            if (n.localName == "b") {
              utils.replace(n, utils.parse('<a>{{name}}</a>',
                                           { name: utils.cloneChildren(n) }));
            } else if (n.localName == "a" &&
                       n.hasAttribute("href")) {
              var href = n.getAttribute("href");
              if (href[0] == "#") {
                n.setAttribute("href", p + ".html" + href);
              }
            }
          }
        });
        idl.push(clone);
      }
    });
  });
  utils.replace(n, utils.parse('<pre class="idl">{{idl}}</pre>',
                               { idl: idl }));
}

function doInterface(conf, page, n) {
  return utils.parse('<p class="issue">Description of IDL members to be generated here.</p>');
}

function doExample(conf, page, n) {
  var href = n.getAttribute('href');
  var desc = n.getAttribute('description');
  var div = utils.parse('<div class="example"><pre class="xml">{{contents}}</pre>{{figure}}{{link}}</div>',
                        { contents: String(fs.readFileSync(href)).replace(/\s+$/, ''),
                          figure: n.getAttribute('image') == 'yes' ?
                                    utils.parse('<div class="figure"><img alt="Example {{name}}{{description}}" src="{{image}}"/><p class="caption">Example {{name}}</p></div>',
                                                { name: n.getAttribute('name'),
                                                  description: desc ? ' — ' + desc : '',
                                                  image: href.replace(/\.svg$/, '.png') }) : '',
                          link: n.getAttribute('link') == 'yes' ?
                                  utils.parse('<p class="view-as-svg"><a href="{{href}}">View this example as SVG (SVG-enabled browsers only)</a></p>',
                                              { href: href }) : '' });
  utils.replace(n, div);
}

function doIncludeFile(conf, page, n) {
  utils.replace(n, utils.parse('<pre>{{contents}}</pre>',
                               { contents: String(fs.readFileSync(n.getAttribute('href'))).replace(/\s+$/, '') }));
}

function formatElementCategories(conf, element, n) {
  var categories = Object.keys(element.categories).sort().map(function(name) { return element.categories[name] });
  if (!categories.length) {
    return 'None';
  }
  return utils.fragment(categories.map(function(cat, i) { return cat.formatLink(!i) }), ', ');
}

function formatContentModel(conf, element, n) {
  if (element.contentModelDescription) {
    return element.contentModelDescription.cloneNode(true);
  }

  var intro;
  switch (element.contentModel) {
    case 'any':
      return 'Any elements or character data.';
    case 'text':
      return 'Character data.';
    default:
      return 'Empty.';
    case 'textoranyof':
      intro = 'Any number of the following elements or character data, in any order:';
      break;
    case 'anyof':
      intro = 'Any number of the following elements, in any order:';
      break;
    case 'oneormoreof':
      intro = 'One or more of the following elements, in any order:';
      break;
  }

  var content = [intro];

  var ul = utils.parse('<ul class="no-bullets"></ul>');
  element.elementCategories.concat().sort().forEach(function(name) {
    var cat = conf.definitions.elementCategories[name];
    if (!cat) {
      return utils.parse('<li><a href="data:," style="background: red; color: white">@@ unknown element category "{{name}}"</a><li>', { name: name });
    }
    var li = utils.parse('<li><a href="{{href}}">{{name}} elements</a><span class="expanding"> — {{elements}}</span></li>',
                         { href: cat.href,
                           name: cat.name,
                           elements: utils.fragment(cat.elements.map(function(name) { return conf.definitions.formatElementLink(name, n) }), ', ') });
    ul.appendChild(li);
  });
  content.push(ul);

  content.push(utils.list(element.elements.concat().sort().map(function(name) {
    var e = conf.definitions.elements[name];
    if (!e) {
      return utils.parse('<a href="data:," style="background: red; color: white">@@ unknown element "{{name}}"</a>', { name: name });
    }
    return conf.definitions.formatElementLink(name, n, true);
  })));

  return content;
}

function formatElementAttributes(conf, element, n) {
  if (!element.attributeCategories && !element.commonAttributes && !element.specificAttributes) {
    return "None";
  }

  var ul = utils.parse('<ul class="no-bullets"></ul>');
  element.attributeCategories.forEach(function(name) {
    var cat = conf.definitions.attributeCategories[name];
    if (!cat) {
      return utils.parse('<li><a href="data:," style="background: red; color: white">@@ unknown attribute category "{{name}}"</a><li>', { name: name });
    }
    var attributes = cat.commonAttributes.concat(cat.attributes.map(function(a) { return a.name }));
    // map(function(name) { return element.commonAttributes[name] }).concat(cat.attributes);
    var li = utils.parse('<li><a href="{{href}}">{{name}} attributes</a><span class="expanding"> — {{attributes}}</span></li>',
                         { href: cat.href,
                           name: cat.name,
                           attributes: utils.fragment(attributes.map(function(a) { return conf.definitions.formatElementAttributeLink(element.name, a, n) }), ', ') });
    ul.appendChild(li);
  });

  element.commonAttributes.forEach(function(name) {
    var li = utils.parse('<li>{{attribute}}</li>',
                         { attribute: conf.definitions.formatElementAttributeLink(element.name, name, n) });
    ul.appendChild(li);
  });

  element.specificAttributes.forEach(function(a) {
    var li = utils.parse('<li>{{attribute}}</li>',
                         { attribute: a.formatLink() });
    ul.appendChild(li);
  });

  return ul;
}

function formatElementGeometryProperties(conf, element, n) {
  if (!element.geometryProperties || !element.geometryProperties.length) {
    return null;
  }

  var ul = utils.parse('<ul class="no-bullets"></ul>');

  element.geometryProperties.forEach(function(pn) {
    var prop = conf.definitions.properties[pn];
    if (!prop) {
      throw "bad property name " + pn;
    }
    var li = utils.parse('<li>{{property}}</li>',
                         { property: prop.formatLink() });
    ul.appendChild(li);
  });

  return ul;
}

function formatElementInterfaces(conf, element, n) {
  var ul = utils.parse('<ul class="no-bullets"></ul>');
  element.interfaces.forEach(function(name) {
    ul.appendChild(utils.parse('<li>{{interface}}</li>',
                               { interface: conf.definitions.formatInterfaceLink(name, n) }));
  });
  return ul;
}

function doElementSummary(conf, page, n) {
  var name = n.getAttribute('name');
  var element = conf.definitions.elements[name];
  var geometry = formatElementGeometryProperties(conf, element, n) || '';
  if (geometry) {
    geometry = '<dt>Geometry properties:</dt><dd>' + geometry + '</dd>';
  }
  var e = utils.parse('<div class="element-summary"><div class="element-summary-name"><span class="element-name">‘<dfn data-dfn-type="element" data-export="" id="elementdef-{{name}}">{{name}}</dfn>’</span></div><dl>' +
                      '<dt>Categories:</dt><dd>{{categories}}</dd>' +
                      '<dt>Content model:</dt><dd>{{contentmodel}}</dd>' +
                      '<dt>Attributes:</dt><dd>{{attributes}}</dd>' +
                      geometry +
                      '<dt>DOM Interfaces:</dt><dd>{{interfaces}}</dd></dl></div>',
                      { name: name,
                        categories: formatElementCategories(conf, element, n),
                        contentmodel: formatContentModel(conf, element, n),
                        attributes: formatElementAttributes(conf, element, n) || '',
                        interfaces: formatElementInterfaces(conf, element, n) || '' });
  utils.replace(n, e);
}

function doLongMaturity(conf, page, n) {
  utils.replace(n, n.ownerDocument.createTextNode(conf.longMaturity));
}

function doDate(conf, page, n) {
  utils.replace(n, n.ownerDocument.createTextNode(conf.publicationDate));
}

function replaceWithURLLink(n, actual, visible) {
  utils.replace(n, utils.parse('<a href="{{actual}}" class="url">{{visible}}</a>',
                               { actual: actual,
                                 visible: visible || actual }));
}

function doThisVersion(conf, page, n) {
  var actualURL = n.hasAttribute('single-page') ? 'single-page.html' : conf.thisVersion;
  var visibleURL = n.hasAttribute('single-page') ? conf.thisVersionSingle : conf.thisVersion;
  replaceWithURLLink(n, actualURL, visibleURL);
}

function doLatestVersion(conf, page, n) {
  replaceWithURLLink(n, conf.versions.latest);
}

function doIncludeLatestEditorsDraft(conf, page, n) {
  if (conf.maturity == 'ED') {
    n.parentNode.removeChild(n);
    return;
  }

  utils.replace(n, utils.parse('<dt>Latest editor\'s draft:</dt><dd><a href="{{href}}" class="url">{{href}}</a></dd>',
                               { href: conf.versions.cvs }));
}

function doPreviousVersion(conf, page, n) {
  replaceWithURLLink(n, conf.maturity == 'ED' ? conf.versions.this : conf.versions.previous);
}

function doCopyright(conf, page, n) {
  utils.replace(n, utils.parse('<p class="copyright"><a href="http://www.w3.org/Consortium/Legal/ipr-notice#Copyright">Copyright</a> © {{year}} <a href="http://www.w3.org/"><abbr title="World Wide Web Consortium">W3C</abbr></a><sup>®</sup> (<a href="http://www.csail.mit.edu/"><abbr title="Massachusetts Institute of Technology">MIT</abbr></a>, <a href="http://www.ercim.eu/"><abbr title="European Research Consortium for Informatics and Mathematics">ERCIM</abbr></a>, <a href="http://www.keio.ac.jp/">Keio</a>, <a href="http://ev.buaa.edu.cn/">Beihang</a>). W3C <a href="http://www.w3.org/Consortium/Legal/ipr-notice#Legal_Disclaimer">liability</a>, <a href="http://www.w3.org/Consortium/Legal/ipr-notice#W3C_Trademarks">trademark</a> and <a href="http://www.w3.org/Consortium/Legal/copyright-documents">document use</a> rules apply.</p>',
                               { year: conf.publicationYear }));
}

function doLocalLink(conf, page, n) {
  var href = utils.resolveURL(conf.thisVersion, n.getAttribute('href'));
  utils.replace(n, utils.parse('<a href="{{href}}">{{content}}</a>',
                               { href: href,
                                 content: n.firstChild ? utils.cloneChildren(n) : href }));
}

function doAttributeTable(conf, page, n) {
  var table = utils.parse('<table class="proptable attrtable"><thead><tr><th>Attribute</th><th>Elements on which the attribute may be specified</th><th title="Animatable"><a>Anim.</a></th></tr></thead><tbody></tbody></table>');
  var attributes = [];
  utils.values(conf.definitions.elements).forEach(function(e) {
    e.specificAttributes.forEach(function(a) {
      attributes.push([[a.name, e.name].toString(), a.formatLink(true), [e.formatLink(true)], a.animatable]);
    });
  });
  utils.values(conf.definitions.attributeCategories).forEach(function(cat) {
    var elements =
      utils.values(conf.definitions.elements)
        .filter(function(e) { return e.attributeCategories.indexOf(cat.name) != -1 })
        .sort(function(a, b) { return utils.compare(a.name, b.name) });
    var elementNames = elements.map(function(e) { return e.name });
    var elementLinks = elements.map(function(e) { return e.formatLink(true) });
    cat.attributes.forEach(function(a) {
      attributes.push([[a.name, elementNames].toString(), a.formatLink(true), elementLinks, a.animatable]);
    });
  });
  conf.definitions.commonAttributesForElements.forEach(function(a) {
    var elementNames = Object.keys(a.elements).sort();
    var elementLinks = elementNames.map(function(name) { return conf.definitions.elements[name].formatLink(true) });
    attributes.push([[a.name, elementNames].toString(), a.formatLink(true), elementLinks, a.animatable]);
  });
  utils.values(conf.definitions.commonAttributes).forEach(function(a) {
    var categoriesWithAttribute =
      utils.values(conf.definitions.attributeCategories)
        .filter(function(cat) { return cat.commonAttributes.indexOf(a) != -1 })
        .map(function(cat) { return cat.name });
    var elements =
      utils.values(conf.definitions.elements)
        .filter(function(e) { return e.commonAttributes.indexOf(a.name) != -1 ||
                                     utils.firstIndexOfAny(e.attributeCategories, categoriesWithAttribute) })
        .sort(function(a, b) { return utils.compare(a.name, b.name) });
    var elementNames = elements.map(function(e) { return e.name });
    var elementLinks = elements.map(function(e) { return e.formatLink(true) });
    attributes.push([[a.name, elementNames].toString(), a.formatLink(true), elementLinks, a.animatable]);
  });
  attributes.sort(function(a, b) { return utils.compare(a[0], b[0]) });
  attributes.forEach(function(a) {
    table.lastChild.appendChild(utils.parse('<tr><th>{{attribute}}</th><td>{{elements}}</td><td>{{animatable}}</td></tr>',
                                            { attribute: a[1],
                                              elements: utils.fragment(a[2], ', '),
                                              animatable: a[3] ? '✓' : '' }));
  });
  utils.replace(n, table);
}

function doElementIndex(conf, page, n) {
  var elements = Object.keys(conf.definitions.elements).sort().map(function(name) { return conf.definitions.formatElementLink(name) });
  var index = utils.parse('<ul class="element-index">{{elements}}</ul>',
                          { elements: elements.map(function(e) { return utils.parse('<li>{{link}}</li>', { link: e }) }) });
  utils.replace(n, index);
}

function doIDLIndex(conf, page, n) {
  var interfaces = Object.keys(conf.definitions.interfaces)
                     .filter(function(name) { return conf.definitions.interfaces[name].href.indexOf(':') == -1 })
                     .sort().map(function(name) { return conf.definitions.formatInterfaceLink(name) });
  var index = utils.parse('<ul>{{interfaces}}</ul>',
                          { interfaces: interfaces.map(function(e) { return utils.parse('<li>{{link}}</li>', { link: e }) }) });
  utils.replace(n, index);
}

function doElementCategory(conf, page, n) {
  var cat = conf.definitions.elementCategories[n.getAttribute('name')];
  var elts = cat.elements.concat().sort();
  utils.replace(n, utils.englishList(elts.map(function(e) { return conf.definitions.formatElementLink(e) })));
}

function doAttributeCategory(conf, page, n) {
  function lookupPresentationAttribute(name) {
    if (!conf.definitions.presentationAttributes[name]) {
      utils.warn('unknown presentation attribute "' + name + '" while processing edit:attributecategory', n);
    }
    return [name, conf.definitions.presentationAttributes[name]];
  }

  function lookupCommonAttribute(name) {
    if (!conf.definitions.commonAttributes[name]) {
      utils.warn('unknown attribute "' + name + '" while processing edit:attributecategory', n);
    }
    return [name, conf.definitions.commonAttributes[name]] ;
  }

  var cat = conf.definitions.attributeCategories[n.getAttribute('name')];
  var omitQuotes = n.getAttribute('omitquotes') == 'yes';
  var attributes =
    cat.presentationAttributes.map(lookupPresentationAttribute)
       .concat(cat.commonAttributes.map(lookupCommonAttribute))
       .concat(cat.attributes.map(function(attr) { return [attr.name, attr] }))
       .sort(function(a, b) { return a[0] - b[0] })
       .map(function(a) { return a[1].formatLink(omitQuotes) });
  utils.replace(n, utils.englishList(attributes));
}

function doElementsWithAttributeCategory(conf, page, n) {
  var category = n.getAttribute('name');
  var omitQuotes = n.getAttribute('omitquotes') == 'yes';
  var elements = 
    utils.values(conf.definitions.elements)
      .filter(function(e) { return e.attributeCategories.indexOf(category) != -1 })
      .sort(function(a, b) { return utils.compare(a.name, b.name) })
      .map(function(e) { return e.formatLink(omitQuotes) });
  utils.replace(n, utils.englishList(elements));
}

function doWhenPublished(conf, page, n) {
  if (conf.maturity != 'ED') {
    return utils.replaceWithChildren(n);
  }
}

function doShortTitle(conf, page, n) {
  return utils.replace(n, n.ownerDocument.createTextNode(conf.shortTitle));
}

function doScript(conf, page, n) {
  with ({ processing: exports,
          utils: utils,
          namespaces: namespaces }) {
    eval(n.textContent);
  }
}

var replacementFunctions = {
  minitoc: doMiniTOC,
  fulltoc: doFullTOC,
  completeidl: doCompleteIDL,
  interface: doInterface,
  example: doExample,
  includefile: doIncludeFile,
  elementsummary: doElementSummary,
  maturity: doLongMaturity,
  date: doDate,
  thisversion: doThisVersion,
  latestversion: doLatestVersion,
  includelatesteditorsdraft: doIncludeLatestEditorsDraft,
  previousversion: doPreviousVersion,
  copyright: doCopyright,
  locallink: doLocalLink,
  attributetable: doAttributeTable,
  elementindex: doElementIndex,
  idlindex: doIDLIndex,
  elementcategory: doElementCategory,
  attributecategory: doAttributeCategory,
  elementswithattributecategory: doElementsWithAttributeCategory,
  whenpublished: doWhenPublished,
  shorttitle: doShortTitle,
  script: doScript
};

exports.defineReplacement = function(elementName, fn) {
  if (replacementFunctions[elementName]) {
    throw 'replacement function for <edit:' + elementName + '> already defined';
  }
  replacementFunctions[elementName] = fn;
};

exports.processReplacements = function(conf, page, doc) {
  utils.forEachNode(doc, function(n) {
    if (n.nodeType == n.ELEMENT_NODE &&
        n.namespaceURI == namespaces.edit &&
        n.localName != 'with') {
      if (!replacementFunctions[n.localName]) {
        utils.warn('unknown element "edit:' + n.localName + '"', n);
      } else {
        return replacementFunctions[n.localName](conf, page, n);
      }
    }
  });
};


// -- Format the DOM so that it serializes nicely -----------------------------

exports.formatMarkup = function(conf, page, doc) {

  // Replace all CDATA section nodes with text nodes.
  utils.forEachNode(doc, function(n) {
    if (n.nodeType == n.CDATA_SECTION_NODE) {
      utils.replace(n, doc.createTextNode(n.data));
    }
  });

  // Remove any remaining edit:* elements or attributes.
  utils.forEachNode(doc, function(n) {
    if (n.nodeType == n.ELEMENT_NODE) {
      if (n.namespaceURI == namespaces.edit) {
        if (n.localName == 'with') {
          var a = [];
          while (n.firstChild) {
            a.push(n.firstChild);
            n.removeChild(n.firstChild);
          }
          for (var i = 0; i < a.length; i++) {
            n.parentNode.insertBefore(a[i], n);
          }
          n.parentNode.removeChild(n);
          return a;
        } else {
          n.parentNode.removeChild(n);
        }
      }
      n.removeAttribute("edit:toc");
      if (n.hasAttribute("edit:excludefromidl")) {
        n.svg_excludefromidl = true;
        n.setAttribute("class", n.getAttribute("class")+" extract");
        //`extract` class is used by Reffy when building IDL indexes
        n.removeAttribute("edit:excludefromidl");
      }
    }
  });

  // Remove the XML declaration "processing instruction".
  if (doc.firstChild.nodeType == doc.PROCESSING_INSTRUCTION_NODE) {
    doc.removeChild(doc.firstChild);
  }

  // Remove any unnecessary xmlns="" attributes.
  utils.forEachNode(doc.documentElement, function(n) {
    if (n.nodeType == n.ELEMENT_NODE) {
      if (n.parentNode.nodeType == n.ELEMENT_NODE &&
          n.parentNode.namespaceURI == n.getAttribute("xmlns")) {
        n.removeAttribute("xmlns");
      }
      n.removeAttribute("xmlns:edit");
    }
  });

  // Replace any HTML4-style <meta http-equiv="Content-Type"> element with
  // an HTML5-style <meta charset>.
  var head = utils.child(doc.documentElement, 'head');
  var meta = utils.child(head, 'meta');
  if (meta) {
    head.removeChild(meta);
  }
  head.insertBefore(utils.parse('<meta charset="UTF-8"/>'), head.firstChild);

  // Remove the existing DOCTYPE node.
  if (doc.firstChild.nodeType == doc.DOCUMENT_TYPE_NODE) {
    doc.removeChild(doc.firstChild);
  }

  // Add an HTML5 DOCTYPE.
  doc.insertBefore(doc.implementation.createDocumentType("html", "", ""), doc.firstChild);
};


// -- Handle automatic linking with <a>. --------------------------------------

function resolveSpecRelativeLink(conf, n) {
  if (n.nodeType != n.ELEMENT_NODE ||
      n.localName != 'a' ||
      !n.hasAttribute('href')) {
    return;
  }

  var href = n.getAttribute('href');
  if (!/^\[(\S+)\]([^#]*)(#.*)?/.test(href)) {
    return;
  }

  var specid = RegExp.$1;
  var path = RegExp.$2;
  var ref = RegExp.$3 || '';
  if (!conf.specs[specid]) {
    throw 'unknown spec [' + specid + ']';
  }
  var base = conf.specs[specid];
  if (/\/$/.test(base) && /^\//.test(path)) {
    path = path.substr(1);
  } else if (!/\/$/.test(base) && path != '' && !/^\//.test(path)) {
    path = '/' + path;
  }
  return base + path + ref;
}

exports.resolveSpecRelativeLink = resolveSpecRelativeLink;

exports.processSpecRelativeLinks = function(conf, page, doc) {
  utils.forEachNode(doc, function(n) {
    var href = resolveSpecRelativeLink(conf, n);
    if (href) {
      n.setAttribute('href', href);
    }
  });
};

exports.processLinks = function(conf, page, doc) {
  function shouldOmitQuotes(n) {
    if (n.parentNode.localName != 'th') {
      return false;
    }

    while (n.localName != 'table') {
      n = n.parentNode;
    }

    return n.getAttribute("class") == 'proptable';
  }

  utils.forEachNode(doc, function(n, speclinks) {
    if (n.nodeType != n.ELEMENT_NODE ||
        n.localName != 'a' ||
        n.hasAttribute('href') ||
        !n.firstChild) {
      return;
    }

    var text = n.textContent;

    var definitions = speclinks ? conf.definitionsBySpec[speclinks] : conf.definitions;

    if (/^'(\S+)\s+element'$/.test(text)) {
      utils.replace(n, definitions.formatElementLink(RegExp.$1, n));
    } else if (/^'(\S+)\s+attribute'$/.test(text)) {
      utils.replace(n, definitions.formatAttributeLink(RegExp.$1, n));
    } else if (/^'(\S+)\s+property'$/.test(text)) {
      utils.replace(n, definitions.formatPropertyLink(RegExp.$1, n, shouldOmitQuotes(n)));
    } else if (/^'(\S+)\s+presentationattribute'$/.test(text)) {
      utils.replace(n, definitions.formatPresentationAttributeLink(RegExp.$1, n));
    } else if (/^'([^\/]+)\/([^\/]+)'$/.test(text)) {
      utils.replace(n, definitions.formatElementAttributeLink(RegExp.$1, RegExp.$2, n));
    } else if (/^'(\S+)'$/.test(text)) {
      utils.replace(n, definitions.formatNameLink(RegExp.$1, n, shouldOmitQuotes(n)));
    } else if (/^([^:]+)::([^:]+)$/.test(text)) {
      var interfaceName = RegExp.$1;
      var memberName = RegExp.$2;
      if (/^(.*)#/.test(definitions.interfaces[interfaceName].href)) {
        var beforeHash = RegExp.$1;
        utils.replace(n, utils.parse('<a href="{{base}}#__svg__{{interface}}__{{member}}">{{prefix}}{{member}}</a>',
                                     { base: beforeHash,
                                       interface: interfaceName,
                                       prefix: n.getAttributeNS(namespaces.edit, 'format') == "expanded" ? interfaceName + '::' : '',
                                       member: memberName }));
      } else {
        utils.warn('unknown interface name "' + interfaceName + '"', n);
      }
    } else if (/^<(.*)>$/.test(text)) {
      utils.replace(n, definitions.formatSymbolLink(RegExp.$1, n));
    } else {
      utils.replace(n, definitions.formatTermLink(text, n));
    }
  }, function(n) {
    return n.nodeType == 1 && n.getAttributeNS(namespaces.edit, 'speclinks');
  });
};


// -- Use rounded quotes around element, attribute and property names. --------

exports.formatQuotes = function(conf, page, doc) {
  utils.forEachNode(doc, function(n) {
    if (n.nodeType == n.ELEMENT_NODE && n.localName != 'a') {
      var text = n.textContent;
      if (text[0] == "'" && text[text.length - 1] == "'") {
        var className = n.getAttribute('class');
        if (/property/.test(className)) {
          n.textContent = text.substr(1, text.length - 2);
          n.parentNode.insertBefore(doc.createTextNode('‘'), n);
          n.parentNode.insertBefore(doc.createTextNode('’'), n.nextSibling);
        } else if (/(element|attr)-name/.test(className)) {
          n.textContent = '‘' + text.substr(1, text.length - 2) + '’';
        }
      }
    }
  });
};
