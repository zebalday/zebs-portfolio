// Commits container
const recentlyPlayedContainer = document.getElementById('recently-played-container');


// Fetch Commits from GitHubAPi endpoint
function fetchRecentlyTracks() {

    $.ajax({
        url: '/portfolio/get-recently-played',
        dataType: 'json',
        success: function(data) {
          /* console.log('Recently played tracks ' + JSON.stringify(data)); */
          displayRecentlyPlayed(data.tracks);
        }
    });
}


// Dsiplay data
function displayRecentlyPlayed(tracks) {

  let content = '<h3>Recently played...</h3>';

  tracks.forEach(track => {

    // Track data
    let trackCardClass = 'recently-played';
    let trackImage = track.track.album.images[0].url;
    let trackName = track.track.name;
    let trackURL = track.track.external_urls.spotify;
    let albumName = track.track.album.name;
    let albumURL = track.track.album.external_urls.spotify;
    let artists = track.track.artists;

    // Track Artists
    let artistsInfo = '';
    artists.forEach((artist, index) => {
        artistsInfo += '<a href="'+artist.external_urls.spotify+'">'+artist.name+'</a>';
        if (index < artists.length - 1) {artistsInfo += ' - ';}
    });
    
    // Cards creation
    let innerContent = `<div id="track-card" class="`+ trackCardClass +`">
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

    /* console.log(trackName); */
    
    content += innerContent;

  });

  
  recentlyPlayedContainer.innerHTML = content;
}


setInterval(fetchRecentlyTracks, 60000);