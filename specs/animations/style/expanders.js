function expand(e) {
  e = e.parentNode;
  e.parentNode.removeAttribute('class');
  e.style.display = "none";
  e.nextSibling.style.display = "inline";
}

(function() {
  var i, a = [], e0, e1p, e1, e2, l = document.getElementsByTagName('span');
  for (i = 0; i != l.length; i++) {
    e0 = l[i];
    if (e0.getAttribute('class') == 'expanding') {
      a.push(e0);
    }
  }
  for (i = 0; i != a.length; i++) {
    e0 = a[i];
    e1 = document.createElement('span');
    e1.setAttribute('class', 'expander');
    e1.setAttribute('onclick', 'expand(event.target)');
    e1p = document.createElement('span');
    e1p.textContent = ' ';
    e1p.appendChild(e1);
    e2 = document.createElement('span');
    e2.style.display = 'none';
    while (e0.firstChild) {
      e2.appendChild(e0.firstChild);
    }
    e0.appendChild(e1p);
    e0.appendChild(e2);
  }
})();
