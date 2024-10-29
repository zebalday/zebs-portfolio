// Commits container
const commitsContainer = document.getElementById('commits-container');
const loader = document.getElementById('commits-loader');


// Fetch Commits from GitHubAPi endpoint
function fetchCommits() {

  // Show loader
  loader.style.display = 'block';

  // Petition
  $.ajax({
      url: '/portfolio/get-last-commits',
      dataType: 'json',
      success: function(data) {
        console.log(data['commits'])
        let commits = data['commits'];
        displayCommits(commits)
      },
      complete: function () {  
        loader.style.display = 'none';
      }
  });
}

// Display data on html
function displayCommits(commits) {

  let content = '<h3>Last commits...</h3>';

  // Ensure the input is an array before processing
  if (!Array.isArray(commits)) {
    console.error('Expected an array of commits');
    return;
  }

  // Clear the container before appending new content
  commitsContainer.innerHTML = '';

  // Iterate over each commit and create a div for the repo_name
  commits.forEach(commit => {

    // Commit data
    let repoName = commit.repo_name;
    let commitDate = commit.commit_date;
    let commitMessage = commit.commit_message;
    let repoURL = commit.repo_url;

    // Inner content
    innerContent = `<div class="commit-card">
                      <h4>`+repoName+`<a href="`+repoURL+`" traget="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i></a></h4>
                      <p>`+commitDate+`</p>
                      <p>`+commitMessage+`</p>
                    </div>`;

    content += innerContent;
    
  });

  commitsContainer.innerHTML = content;
}

// Execute on window load
window.onload = fetchCommits;