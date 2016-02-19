var utils = require('./utils.js'),
    namespaces = require('./namespaces.js'),
    forEachChild = utils.forEachChild;

function Element(properties) {
  if (properties) utils.extend(this, properties);
}

Element.prototype.formatLink = function(omitQuotes) {
  return utils.parse('<span class="element-name">{{lquote}}<a href="{{href}}"><span>{{name}}</span></a>{{rquote}}</span>',
                     { href: this.href,
                       name: this.name,
                       lquote: omitQuotes ? '' : '‘',
                       rquote: omitQuotes ? '' : '’' });
};

function Attribute(properties) {
  if (properties) utils.extend(this, properties);
}

Attribute.prototype.formatLink = function(omitQuotes) {
  var title;
  if (this.property) {
    title = 'Presentation attribute for property ‘' + utils.encode(this.property) + '’';
  }
  var span = utils.parse('<span class="attr-name">{{lquote}}<a href="{{href}}"><span>{{name}}</span></a>{{rquote}}</span>',
                         { href: this.href,
                           name: this.name,
                           lquote: omitQuotes ? '' : '‘',
                           rquote: omitQuotes ? '' : '’' });
  if (title) {
    span.firstChild.nextSibling.setAttribute('title', title);
  }
  return span;
};

function Property(properties) {
  if (properties) utils.extend(this, properties);
}

Property.prototype.formatLink = function(omitQuotes) {
  return utils.parse('{{lquote}}<a class="property" href="{{href}}">{{name}}</a>{{rquote}}',
                     { href: this.href,
                       name: this.name,
                       lquote: '',
                       rquote: '' });
};

function Symbol(properties) {
  if (properties) utils.extend(this, properties);
}

Symbol.prototype.formatLink = function() {
  return utils.parse('<a href="{{href}}">&lt;{{name}}&gt;</a>',
                     { href: this.href,
                       name: this.name });
};

function Term(properties) {
  if (properties) utils.extend(this, properties);
}

Term.prototype.formatLink = function() {
  return utils.parse('<a href="{{href}}">{{name}}</a>',
                     { href: this.href,
                       name: this.markup || this.name });
};

function ElementCategory(properties) {
  if (properties) utils.extend(this, properties);
}

ElementCategory.prototype.formatLink = function(capitalize) {
  return utils.parse('<a href="{{href}}">{{name}}</a>',
                     { href: this.href,
                       name: (capitalize ? utils.initialuc(this.name) : this.name) + ' element' });
};

function AttributeCategory(properties) {
  if (properties) utils.extend(this, properties);
}

AttributeCategory.prototype.formatLink = function() {
  return utils.parse('<a href="{{href}}">{{name}}</a>',
                     { href: this.href,
                       name: (capitalize ? utils.initialuc(this.name) : this.name) + ' element' });
};

function Interface(properties) {
  if (properties) utils.extend(this, properties);
}

Interface.prototype.formatLink = function() {
  return utils.parse('<a class="idlinterface" href="{{href}}">{{name}}</a>',
                     { href: this.href,
                       name: this.name });
};

function Definitions() {
  this.elements = { };
  this.elementCategories = { };
  this.attributeCategories = { };
  this.properties = { };
  this.interfaces = { };
  this.symbols = { };
  this.terms = { };
  this.commonAttributesForElements = [];
  this.commonAttributes = { };
  this.geometryProperties = [];
  this.presentationAttributes = { };
}

Definitions.prototype.formatElementLink = function(name, n, omitQuotes) {
  if (!this.elements[name]) {
    utils.warn('unknown element "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown element "{{name}}"</span>', { name: name });
  }
  return this.elements[name].formatLink(omitQuotes);
};

Definitions.prototype.formatElementAttributeLink = function(elementName, attributeName, n) {
  if (!this.elements[elementName] || !this.elements[elementName].attributes[attributeName]) {
    utils.warn('unknown attribute "' + attributeName + '" on element "' + elementName + '"', n);
    return utils.parse('<span class="xxx">@@ unknown attribute "{{attribute}}" on element "{{element}}</span>', { attribute: attributeName, element: elementName });
  }
  return this.elements[elementName].attributes[attributeName].formatLink();
};

function findAttributesInCategories(definitions, attributeName) {
  var attrs = [];
  for (var name in definitions.attributeCategories) {
    var cat = definitions.attributeCategories[name];
    for (var i = 0; i < cat.attributes.length; i++) {
      if (cat.attributes[i].name == attributeName) {
        attrs.push(cat.attributes[i]);
      }
    }
  }
  return attrs;
}

function findCommonAttributesForElements(definitions, attributeName) {
  var attrs = [];
  for (var i = 0; i < definitions.commonAttributesForElements.length; i++) {
    var attr = definitions.commonAttributesForElements[i];
    if (attr.name == attributeName) {
      attrs.push(attr);
    }
  }
  return attrs;
}

Definitions.prototype.formatAttributeLink = function(attributeName, context) {
  var elementName = context && getElementContext(this, context);
  if (elementName && this.elements[elementName] && this.elements[elementName].attributes[attributeName]) {
    return this.elements[elementName].attributes[attributeName].formatLink();
  }
  if (this.commonAttributes[attributeName]) {
    return this.commonAttributes[attributeName].formatLink();
  }
  var attrs = findAttributesInCategories(this, attributeName)
                .concat(findCommonAttributesForElements(this, attributeName));
  if (attrs.length == 1) {
    return attrs[0].formatLink();
  }
  if (attrs.length > 1) {
    utils.warn('ambiguous attribute "' + attributeName + '"', context);
    return utils.parse('<span class="xxx">@@ ambiguous attribute "{{attribute}}"</span>', { attribute: attributeName });
  }
  utils.warn('unknown attribute "' + attributeName + '"', context);
  return utils.parse('<span class="xxx">@@ unknown attribute "{{attribute}}"</span>', { attribute: attributeName });
};

Definitions.prototype.formatPropertyLink = function(name, n, omitQuotes) {
  if (!this.properties[name]) {
    utils.warn('unknown property "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown property "{{name}}"</span>', { name: name });
  }
  return this.properties[name].formatLink(omitQuotes);
};

Definitions.prototype.formatPresentationAttributeLink = function(name, n) {
  if (!this.presentationAttributes[name]) {
    utils.warn('unknown presentation attribute "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown presentation attribute "{{name}}"</span>', { name: name });
  }
  return this.presentationAttributes[name].formatLink();
};

Definitions.prototype.formatSymbolLink = function(name, n) {
  if (!this.symbols[name]) {
    utils.warn('unknown symbol "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown symbol "{{name}}"</span>', { name: name });
  }
  return this.symbols[name].formatLink();
};

function normalizeTermName(name) {
  return name.toLowerCase().replace(/\s+/g, ' ').trim();
}

function findClosestInterfaceDefinition(n) {
  while (n) {
    if (n.nodeType == n.ELEMENT_NODE &&
        /^h[2-6]$/.test(n.localName) &&
        /^Interface (\S+)$/.test(n.textContent)) {
      return RegExp.$1;
    }
    n = n.previousSibling || n.parentNode;
  }
}

Definitions.prototype.formatTermLink = function(name, n) {
  if (this.terms[name]) {
    return this.terms[name].formatLink();
  }
  if (this.terms[normalizeTermName(name)]) {
    return this.terms[normalizeTermName(name)].formatLink();
  }
  if (this.interfaces[name]) {
    return this.interfaces[name].formatLink();
  }
  var interfaceName = findClosestInterfaceDefinition(n);
  if (interfaceName && n.ownerDocument.getElementById('__svg__' + interfaceName + '__' + name)) {
    return utils.parse('<a href="#__svg__{{interface}}__{{name}}">{{prefix}}{{name}}</a>',
                       { interface: interfaceName,
                         name: name,
                         prefix: n.getAttributeNS(namespaces.edit, 'format') == 'expanded' ? interfaceName + '::' : '' });
  }
  utils.warn('unknown term "' + name + '"', n);
  return utils.parse('<span class="xxx">@@ unknown term "{{name}}"</span>', { name: name });
};

Definitions.prototype.formatElementCategoryLink = function(name, n) {
  if (!this.elementCategories[name]) {
    utils.warn('unknown element category "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown element category "{{name}}"</span>', { name: name });
  }
  return this.elementCategories[name].formatLink();
};

Definitions.prototype.formatAttributeCategoryLink = function(name, n) {
  if (!this.attributeCategories[name]) {
    utils.warn('unknown attribute category "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown attribute category "{{name}}"</span>', { name: name });
  }
  return this.attributeCategories[name].formatLink();
};

Definitions.prototype.formatInterfaceLink = function(name, n) {
  if (!this.interfaces[name]) {
    utils.warn('unknown IDL interface "' + name + '"', n);
    return utils.parse('<span class="xxx">@@ unknown interface "{{name}}"</span>', { name: name });
  }
  return this.interfaces[name].formatLink();
};

function getElementContext(definitions, context) {
  var elementName;
  while (context) {
    if (context.namespaceURI == namespaces.edit &&
        context.localName == 'with') {
      elementName = context.getAttribute('element');
      if (definitions.elements[elementName]) {
        return elementName;
      }
      utils.warn('unknown element "' + elementName + '" in edit:with', context);
    }
    context = context.parentNode;
  }
  return null;
}

Definitions.prototype.formatNameLink = function(name, context, omitQuotes) {
  var elementName = getElementContext(this, context);
  var element = this.elements[name];
  var attribute = elementName && this.elements[elementName].attributes[name] || this.commonAttributes[name];
  var property = this.properties[name];

  if (elementName && attribute) {
    // Inside an <edit:with>, assume that <a>'name'</a> links refer to an
    // attribute on the element given on the <edit:with>.  Outside an
    // <edit:with>, the name must be unambiguous.
    element = null;
    property = null;
  }

  if (!attribute && !property) {
    var attrs = findAttributesInCategories(this, name)
                  .concat(findCommonAttributesForElements(this, name));
    if (attrs.length > 1) {
      utils.warn('ambiguous name "' + name + '" matching multiple attributes', context);
      return utils.parse('<span class="xxx">@@ ambiguous name "{{name}}" (matches multiple attributes)</span>', { name: name });
    }
    attribute = attrs[0];
  }

  var types = [];
  if (element) types.push('element');
  if (attribute) types.push('attribute');
  if (property) types.push('property');

  if (types.length == 0) {
    utils.warn('unknown element, attribute or property "' + name + '"', context);
    return utils.parse('<span class="xxx">@@ unknown element, attribute or property "{{name}}"</span>', { name: name });
  }
  if (types.length > 1) {
    utils.warn('ambiguous name "' + name + '" matching ' + types.join(" and "), context);
    return utils.parse('<span class="xxx">@@ ambiguous name "{{name}}" (matches {{types}})</span>', { name: name, types: types.join(' and ') });
  }
  return (element || attribute || property).formatLink(omitQuotes);
};

function loadInto(filename, base, specid, defs) {
  var doc = utils.parseXML(filename);

  if (!defs.locations) {
    defs.locations = [];
  }

  function noteLocation(thingWithHref, node) {
    defs.locations.push([thingWithHref.href, node.ownerDocument.documentURI, node.lineNumber, node.columnNumber]);
  }

  // XXX Handle <import>.

  forEachChild(doc.documentElement, 'element', function(e) {
    var element = new Element({
      name: e.getAttribute('name'),
      href: utils.resolveURL(base, e.getAttribute('href')),
      contentModel: e.getAttribute('contentmodel'),
      elementCategories: utils.splitList(e.getAttribute('elementcategories')),
      elements: utils.splitList(e.getAttribute('elements')),
      attributeCategories: utils.splitList(e.getAttribute('attributecategories')),
      commonAttributes: utils.splitList(e.getAttribute('attributes')),
      interfaces: utils.splitList(e.getAttribute('interfaces')),
      specificAttributes: [],
      geometryProperties: utils.splitList(e.getAttribute('geometryproperties')),
      categories: { },
      specid: specid
    });
    noteLocation(element, e);

    forEachChild(e, 'attribute', function(c) {
      var attribute = new Attribute({
        name: c.getAttribute('name'),
        href: utils.resolveURL(base, c.getAttribute('href')),
        animatable: c.getAttribute('animatable') == 'yes',
        specific: true,
        specid: specid
      });
      noteLocation(attribute, c);
      element.specificAttributes.push(attribute);
    });

    forEachChild(e, 'contentmodel', function(c) {
      element.contentModelDescription = utils.cloneChildren(c);
    });

    defs.elements[element.name] = element;
  });

  forEachChild(doc.documentElement, 'elementcategory', function(ec) {
    var category = new ElementCategory({
      name: ec.getAttribute('name'),
      href: utils.resolveURL(base, ec.getAttribute('href')),
      elements: utils.splitList(ec.getAttribute('elements')),
      specid: specid
    });
    noteLocation(category, ec);

    defs.elementCategories[category.name] = category;
  });

  forEachChild(doc.documentElement, 'attribute', function(a) {
    var attribute = new Attribute({
      name: a.getAttribute('name'),
      href: utils.resolveURL(base, a.getAttribute('href')),
      animatable: a.getAttribute('animatable') == 'yes',
      common: true,
      specid: specid
    });
    noteLocation(attribute, a);
    if (a.hasAttribute('elements')) {
      attribute.elements = utils.set(utils.splitList(a.getAttribute('elements')));
      defs.commonAttributesForElements.push(attribute);
    } else {
      defs.commonAttributes[attribute.name] = attribute;
    }
  });

  forEachChild(doc.documentElement, 'attributecategory', function(ac) {
    var category = new AttributeCategory({
      name: ac.getAttribute('name'),
      href: utils.resolveURL(base, ac.getAttribute('href')),
      attributes: [],
      commonAttributes: utils.splitList(ac.getAttribute('attributes')),
      presentationAttributes: utils.splitList(ac.getAttribute('presentationattributes')),
      specid: specid
    });
    noteLocation(category, ac);

    forEachChild(ac, 'attribute', function(a) {
      var attribute = new Attribute({
        name: a.getAttribute('name'),
        href: utils.resolveURL(base, a.getAttribute('href')),
        animatable: a.getAttribute('animatable') == 'yes',
        category: category,
        specid: specid
      });
      noteLocation(attribute, a);
      category.attributes.push(attribute);
    });

    defs.attributeCategories[category.name] = category;
  });

  forEachChild(doc.documentElement, 'property', function(p) {
    var property = new Property({
      name: p.getAttribute('name'),
      href: utils.resolveURL(base, p.getAttribute('href')),
      specid: specid
    });
    noteLocation(property, p);

    defs.properties[property.name] = property;

    var presentationAttribute = new Attribute({
      name: property.name,
      href: property.href,
      property: property.name,
      specid: specid
    });
    defs.presentationAttributes[property.name] = presentationAttribute;
  });

  forEachChild(doc.documentElement, 'interface', function(i) {
    var intf = new Interface({
      name: i.getAttribute('name'),
      href: utils.resolveURL(base, i.getAttribute('href')),
      specid: specid
    });
    noteLocation(intf, i);

    defs.interfaces[intf.name] = intf;
  });

  forEachChild(doc.documentElement, 'symbol', function(s) {
    var symbol = new Symbol({
      name: s.getAttribute('name'),
      href: utils.resolveURL(base, s.getAttribute('href')),
      specid: specid
    });
    noteLocation(symbol, s);

    defs.symbols[symbol.name] = symbol;
  });

  forEachChild(doc.documentElement, 'term', function(t) {
    var term = new Term({
      name: t.getAttribute('name'),
      href: utils.resolveURL(base, t.getAttribute('href')),
      specid: specid
    });
    noteLocation(term, t);

    if (t.firstChild) {
      term.markup = utils.cloneChildren(t);
    }

    defs.terms[term.name] = term;
    if (!defs.terms[normalizeTermName(term.name)]) {
      defs.terms[normalizeTermName(term.name)] = term;
    }
  });
}

function resolve(defs, mainspecDefs) {
  for (var name in defs.elements) {
    var element = defs.elements[name];
    element.attributes = { };
    element.attributeOrder = [];
    for (var i = 0; i < element.attributeCategories.length; i++) {
      var catName = element.attributeCategories[i];
      var cat = defs.attributeCategories[catName] ||
                mainspecDefs && mainspecDefs.attributeCategories[catName];
      if (cat) {
        for (var j = 0; j < cat.attributes.length; j++) {
          element.attributes[cat.attributes[j].name] = cat.attributes[j];
          element.attributeOrder.push(cat.attributes[j].name);
        }
      }
    }
    if (mainspecDefs) {
      for (var i = 0; i < mainspecDefs.commonAttributesForElements.length; i++) {
        var attr = mainspecDefs.commonAttributesForElements[i];
        if (attr.elements[element.name]) {
          element.attributes[attr.name] = attr;
          element.attributeOrder.push(attr.name);
        }
      }
    }
    for (var i = 0; i < defs.commonAttributesForElements.length; i++) {
      var attr = defs.commonAttributesForElements[i];
      if (attr.elements[element.name]) {
        element.attributes[attr.name] = attr;
        element.attributeOrder.push(attr.name);
      }
    }
    for (var i = 0; i < element.commonAttributes.length; i++) {
      var attrName = element.commonAttributes[i];
      var commonAttribute = defs.commonAttributes[attrName] ||
                            mainspecDefs && mainspecDefs.commonAttributes[attrName];
      if (commonAttribute) {
        element.attributes[attrName] = commonAttribute;
        element.attributeOrder.push(attrName);
      }
    }
    for (var i = 0; i < element.specificAttributes.length; i++) {
      var attr = element.specificAttributes[i];
      element.attributes[attr.name] = attr;
      element.attributeOrder.push(attr.name);
    }
  }

  if (mainspecDefs) {
    for (var name in mainspecDefs.elementCategories) {
      var cat = mainspecDefs.elementCategories[name];
      for (var i = 0; i < cat.elements.length; i++) {
        var eltName = cat.elements[i];
        if (defs.elements[eltName]) {
          defs.elements[eltName].categories[name] = cat;
        }
      }
    }
  }
  for (var name in defs.elementCategories) {
    var cat = defs.elementCategories[name];
    for (var i = 0; i < cat.elements.length; i++) {
      var eltName = cat.elements[i];
      var elt = defs.elements[eltName] ||
                mainspecDefs && mainspecDefs.elements[eltName];
      if (elt) {
        elt.categories[name] = cat;
      }
    }
  }
}

exports.load = function(infos) {
  var defs = new Definitions();
  var defsBySpec = { };
  var mainSpecs = { };
  infos.reverse();
  for (var i = 0; i < infos.length; i++) {
    var href = infos[i].href;
    var base = infos[i].base;
    var specid = infos[i].specid;
    loadInto(href, base, specid, defs);
    if (specid) {
      defsBySpec[specid] = new Definitions();
      loadInto(href, base, specid, defsBySpec[specid]);
    }
  }
  for (var i = 0; i < infos.length; i++) {
    var specid = infos[i].specid;
    if (specid) {
      var mainspec = infos[i].mainspec;
      resolve(defsBySpec[specid], mainspec && defsBySpec[mainspec]);
      if (mainspec) {
        mainSpecs[specid] = mainspec;
      }
    }
  }
  resolve(defs);
  return { definitions: defs, definitionsBySpec: defsBySpec, mainSpecs: mainSpecs };
};
