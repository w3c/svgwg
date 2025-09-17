var local = location.protocol == "file:";
if (local) {
  for (n = document.head.firstChild; n; n = n.nextSibling) {
    if (n.nodeName.toLowerCase() == "link" &&
        n.getAttribute("href").indexOf("//") == 0) {
      n.href = "https:" + n.getAttribute("href");
    }
  }
}
