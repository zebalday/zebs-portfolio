// Commits container
const currentlyPlayingContainer = document.getElementById('current-playing-container');


// Fetch Commits from GitHubAPi endpoint
function fetchCurrentTrack() {

    $.ajax({
        url: '/portfolio/get-current-song',
        dataType: 'json',
        success: function(data) {
          //console.log('Current playing track ' + JSON.stringify(data));
          displayCurrentSong(data);
        }
    });
}

// Display current song data
function displayCurrentSong(currentSong){

  console.log(JSON.stringify(currentSong));

  if (currentSong.currently_playing == true) {

    // Clear content
    currentlyPlayingContainer.innerHTML= '';
  
    // Track data
    trackCardClass = 'current-playing';
    trackImage = currentSong.track.item.album.images[0].url;
    trackName = currentSong.track.item.name;
    trackURL = currentSong.track.item.external_urls.spotify;
    albumName = currentSong.track.item.album.name;
    albumURL = currentSong.track.item.album.external_urls.spotify;
  
    // Set content
    content = `<div id="track-card" class="`+ trackCardClass +`">
                <div class="container">
                    <!-- THUMBNAIL -->
                    <div class="thumbnail-container">
                        <img src="`+trackImage+`" alt="track-thumbnail">
                    </div>
                    <!-- TRACK INFO -->
                    <div class="track-info">
                        <!-- TRACK NAME -->
                        <div class="track-name">
                            <h4><a href=`+trackURL+`>`+trackName+`</a></h4>
                        </div>
                        <!-- ALBUM -->
                        <div class="track-album">
                            <p><a href=`+albumURL+`>`+albumName+`</a></p>
                        </div>
                        <!-- ARTISTS -->
                        <div class="artists-list">
                            <p>
                                {% for artist in track.artists %}
                                    <a href={{artist.external_urls.spotify}}>{{ artist.name }}</a> {% if not forloop.last %} - {% endif %}
                                {% endfor %}
                            </p>
                        </div>
                    </div>
                </div>
            </div>`;

    //console.log(content);
    currentlyPlayingContainer.innerHTML = content;

  }
  else{
    currentlyPlayingContainer.innerHTML= '';
    console.log("No song playing right now.");
  }
}



setInterval(fetchCurrentTrack, 2000);
