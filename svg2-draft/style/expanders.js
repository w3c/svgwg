(function() {
  function expand(e) {
    var e1p = e.target.parentNode;
    e1p.parentNode.removeAttribute('class');
    e1p.style.display = "none";
    e1p.nextSibling.style.display = "inline";
  }
  
  var i, e0, e1, e1p, e2, l = document.querySelectorAll('span.expanding');
  for (i = 0; i != l.length; i++) {
    e0 = l[i];

    e1 = document.createElement('button');
    e1.setAttribute('class', 'expander');
    e1.addEventListener('click', expand);
    e1.textContent = 'show';

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
