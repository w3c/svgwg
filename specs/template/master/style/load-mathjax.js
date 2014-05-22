// If there were an "MML_SVG" config we should use that, to avoid the overhead of looking for TeX-style math.
var n = document.createElement("script");
n.src = (local ? "https:" : location.protocol) + "//d3eoax9i5htok0.cloudfront.net/mathjax/2.0-latest/MathJax.js?config=TeX-AMS-MML_SVG";
document.head.appendChild(n);
