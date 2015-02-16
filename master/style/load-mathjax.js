// If there were an "MML_SVG" config we should use that, to avoid the overhead of looking for TeX-style math.
var n = document.createElement("script");
n.src = (local ? "https:" : location.protocol) + "//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_SVG";
document.head.appendChild(n);
