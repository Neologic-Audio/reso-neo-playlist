window.onkeydown = function(e) {
    return !(e.keyCode == 32);
};

/*
  Handles a click on the down button to slide down the playlist.
*/
document.getElementsByClassName('down-header')[0].addEventListener('click', function(){
  var list = document.getElementById('list');

  list.style.height = ( parseInt( document.getElementById('flat-black-player-container').offsetHeight ) - 135 ) + 'px';

  document.getElementById('list-screen').classList.remove('slide-out-top');
  document.getElementById('list-screen').classList.add('slide-in-top');
  document.getElementById('list-screen').style.display = "block";
});

/*
  Handles a click on the up arrow to hide the list screen.
*/
document.getElementsByClassName('hide-playlist')[0].addEventListener('click', function(){
  document.getElementById('list-screen').classList.remove('slide-in-top');
  document.getElementById('list-screen').classList.add('slide-out-top');
  document.getElementById('list-screen').style.display = "none";
});

/*
  Handles a click on the song played progress bar.
*/
document.getElementById('song-played-progress').addEventListener('click', function( e ){
  var offset = this.getBoundingClientRect();
  var x = e.pageX - offset.left;

  Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( this.offsetWidth) ) * 100 );
});

document.querySelector('img[data-amplitude-song-info="cover_art_url"]').style.height = document.querySelector('img[data-amplitude-song-info="cover_art_url"]').offsetWidth + 'px';

Amplitude.init({
  "bindings": {
    37: 'prev',
    39: 'next',
    32: 'play_pause'
  },
  "songs": [
    {
      "url": "https://api.resonate.is/v1/stream/",
    },
    {
      "url": "https://api.resonate.is/v1/stream/",
    },
  ]
});

  $(function () {
        function showTrack(released) {
            document.getElementById("player").src = "https://stream.resonate.coop/embed/track/" + released;
            document.getElementById("listen").href = "https://stream.resonate.coop/track/" + released;
        }

        function search() {
            const query = $("#search").find("input[name=search]").val();
            $.get("/search?q=" + encodeURIComponent(query),
                function (data) {
                    const t = $("table#results tbody").empty();
                    if (!data || data.length == 0) return;
                    data.forEach(function (track) {
                        $("<tr><td class='track'>" + track.title + "</td><td>" + track.tagline + "</td></tr>"
                        ).appendTo(t)
                            .click(function () {
                                showTrack(track.released);
                            })
                    });
                    showTrack(data[0].released);
                }, "json");
            return false;
        }

        $("#search").submit(search);
        search();
    })