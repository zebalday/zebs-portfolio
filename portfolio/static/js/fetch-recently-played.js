// Commits container
const tracksContainer = document.getElementById('track-card');


// Fetch Commits from GitHubAPi endpoint
function fetchRecentlyTracks() {

    $.ajax({
        url: '/portfolio/get-recently-played',
        dataType: 'json',
        success: function(data) {
          console.log('Recently played tracks ' + JSON.stringify(data))
        }
    });
}



//setInterval(fetchRecentlyTracks, 20000);