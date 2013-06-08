// ==UserScript==
// @name        Youtube: isiton
// @namespace   com.adnissen.userscript.isiton
// @include     https://www.youtube.com/*
// @include     http://www.youtube.com/*
// @version     0.0.2
// ==/UserScript==

// a function that loads jQuery and calls a callback function when jQuery has finished loading
function addJQuery(callback) {
  var script = document.createElement("script");
  script.setAttribute("src", "//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js");
  script.addEventListener('load', function() {
    var script = document.createElement("script");
    script.textContent = "window.jQ=jQuery.noConflict(true);(" + callback.toString() + ")();";
    document.body.appendChild(script);
  }, false);
  document.body.appendChild(script);
}

// the guts of this userscript
function main() {
  // Note, jQ replaces $ to avoid conflicts.
  function checkTitle() {
        var title = jQ('.watch-title').attr('title');
        jQ.ajax({
        url: "http://127.0.0.1:5000/search/" + title
        }).done(function (data) {
            if (data.rdio_url != "" || data.spotify_url != "")
            {
                 jQ('#eow-description').append('<br><br><strong>Stream this on: </strong>');
                 console.log(data);
            }
            if (data.rdio_url != "")
               jQ('#eow-description').append('<br><a href="' + data.rdio_url + '">rdio</a>');
            if (data.spotify_url != "")    
               jQ('#eow-description').append('<br><a href="' + data.spotify_url + '">Spotify</a>');
        });
    }
checkTitle();
}

// load jQuery and execute the main function
addJQuery(main);

 