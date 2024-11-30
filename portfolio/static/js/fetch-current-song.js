// Commits container
const currentlyPlayingContainer = document.getElementById('current-playing-container');
const currentSongLoader = document.getElementById('current-song-loader');

// Fetch Commits from GitHubAPi endpoint
function fetchCurrentTrack() {

    // Show loader
    /* currentSongLoader.style.display = 'block'; */

    $.ajax({
        url: '/portfolio/get-current-song',
        dataType: 'json',
        success: function(data) {
          /* console.log('Current playing track ' + JSON.stringify(data)); */
          displayCurrentSong(data);
        },
        complete: function(){
            currentSongLoader.style.display = 'none';
        }
    });
}

// Display current song data
function displayCurrentSong(currentSong){

  //console.log(JSON.stringify(currentSong));

  if (currentSong.currently_playing == true) {

    // Clear content
    currentlyPlayingContainer.innerHTML= '';
  
    // Track data
    let trackCardClass = 'current-playing';
    let trackImage = currentSong.track.item.album.images[0].url;
    let trackName = currentSong.track.item.name;
    let trackURL = currentSong.track.item.external_urls.spotify;
    let albumName = currentSong.track.item.album.name;
    let albumURL = currentSong.track.item.album.external_urls.spotify;
    let artists = currentSong.track.item.artists;
    
    /* console.log(JSON.stringify(artists)); */

    // Create artists list info
    let artistsInfo = '';
    artists.forEach((artist, index) => {
        artistsInfo += '<a href="'+artist.external_urls.spotify+'">'+artist.name+'</a>';
        if (index < artists.length - 1) {artistsInfo += ' - ';}
    });
    /* console.log(artistsInfo) */

    // Set content
    content = `<h3>Currently playing</h3>
                <div id="track-card" class="`+ trackCardClass +`">
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
                                <p>`+artistsInfo+`</p>
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


setInterval(fetchCurrentTrack, 5000);
