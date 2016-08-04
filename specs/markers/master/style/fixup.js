/******************************************************************************
 *                 JS Extension for the W3C Spec Style Sheet                  *
 *                                                                            *
 * This code handles some fixup to improve the table of contents.             *
 * It is intended to be a very simple script for 2016.                        *
 ******************************************************************************/
(function(){
  function toggleSidebar(on) {

    /* Don't scroll to compensate for the ToC if we're above it already. */
    var headY = 0;
    var head = document.querySelector('.head');
    headY += head.offsetTop + head.offsetHeight; // terrible approx of "top of ToC"
    var skipScroll = window.scrollY < headY;

    if (on == undefined) {
      on = !document.body.classList.contains('toc-sidebar');
    }

    var toggle = document.getElementById('toc-toggle');
    var toggleAbbr = toggle.firstChild;
    var tocNav = document.getElementById('toc');
    if (on) {
      var tocHeight = tocNav.offsetHeight;
      document.body.classList.add('toc-sidebar');
      document.body.classList.remove('toc-inline');
      toggleAbbr.textContent = "←";
      toggleAbbr.title = "Collapse Sidebar";
      if (!skipScroll) {
        window.scrollBy(0, 0 - tocHeight);
      }
      tocNav.focus();
    }
    else {
      document.body.classList.add('toc-inline');
      document.body.classList.remove('toc-sidebar');
      toggleAbbr.textContent = "→";
      toggleAbbr.title = "Pop Out Sidebar";
      if (!skipScroll) {
        window.scrollBy(0, tocNav.offsetHeight);
      }
      if (toggle.matches(':hover')) {
        /* Unfocus button when not using keyboard navigation,
           because I don't know where else to send the focus. */
        toggle.blur();
      }
    }
  }

  function createSidebarToggle() {
    /* Create the sidebar toggle in JS; it shouldn't exist when JS is off. */
    var toggle = document.createElement('a');
      /* This should probably be a button, but appearance isn't standards-track.*/
    toggle.setAttribute('id', 'toc-toggle');
    toggle.setAttribute('class', 'toc-toggle');
    toggle.setAttribute('href', '#toc');
    toggle.addEventListener('click', function(e){ e.preventDefault(); toggleSidebar(); return false;}, false);
    toggle.innerHTML = "<abbr title='Collapse Sidebar'>←</abbr>";

    /* Get <nav id=toc-nav>, or make it if we don't have one. */
    var tocNav = document.getElementById('toc-nav');
    if (!tocNav) {
      tocNav = document.createElement('nav');
      tocNav.setAttribute('id', 'toc-nav');
      /* Prepend for better keyboard navigation */
      document.body.insertBefore(tocNav, document.body.firstChild);
    }
    /* While we're at it, make sure we have a Jump to Toc link. */
    var tocJump = document.getElementById('toc-jump');
    if (!tocJump) {
      tocJump = document.createElement('a');
      tocJump.setAttribute('id', 'toc-jump');
      tocJump.setAttribute('href', '#toc');
      tocJump.innerHTML = "<abbr title='Jump to Table of Contents'>↑</abbr>";
      tocNav.appendChild(tocJump);
    }

    tocNav.appendChild(toggle);
  }

  createSidebarToggle();
  var sidebarMedia = window.matchMedia('screen and (min-width: 78em)');
  if(sidebarMedia.addEventListener) {
    sidebarMedia.addEventListener('change', function(e){toggleSidebar(e.matches);}, false);
  } else if(sidebarMedia.addListener) {
    sidebarMedia.addListener(function(e){toggleSidebar(e.matches);});
  }
  toggleSidebar(sidebarMedia.matches);

  /* If the sidebar has been manually opened and is currently overlaying the text
     (window too small for the MQ to add the margin to body),
     then auto-close the sidebar once you click on something in there. */
  document.getElementById('toc').addEventListener('click', function(e) {
    if(e.target.tagName.toLowerCase() == "a" && document.body.classList.contains('toc-sidebar') && !sidebarMedia.matches) {
      toggleSidebar();
    }
  }, false);

  /* Wrap tables in case they overflow */
  var tables = document.querySelectorAll(':not(.overlarge) > table.data, :not(.overlarge) > table.index');
  var numTables = tables.length;
  for (var i = 0; i < numTables; i++) {
    var table = tables[i];
    var wrapper = document.createElement('div');
    wrapper.className = 'overlarge';
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
  }

})();
