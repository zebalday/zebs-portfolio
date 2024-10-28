// Commits container
const commitsContainer = document.getElementById('commits-container');


// Fetch Commits from GitHubAPi endpoint
function fetchCommits() {

  $.ajax({
      url: '/portfolio/get-last-commits',
      dataType: 'json',
      success: function(data) {
        console.log(data['commits'])
        let commits = data['commits'];
        displayCommits(commits)
      }
  });
}

// Display data on html
function displayCommits(commits) {

  // Ensure the input is an array before processing
  if (!Array.isArray(commits)) {
    console.error('Expected an array of commits');
    return;
  }

  // Clear the container before appending new content
  commitsContainer.innerHTML = '';

  // Iterate over each commit and create a div for the repo_name
  commits.forEach(commit => {

    // Commit card & onclick event
    const commitDiv = document.createElement('div');
    commitDiv.classList.add('commit-card');
    commitDiv.onclick = () => {window.open(commit.repo_url, '_blank');};

    // Repo name, commit date, commite message
    const commitName = document.createElement('h3');
    commitName.textContent = commit.repo_name;
    
    const commitDate = document.createElement('p');
    commitDate.textContent = commit.commit_date;
    
    const commitMessage = document.createElement('p');
    commitMessage.textContent = commit.commit_message;

    // Add data to commit card
    commitDiv.appendChild(commitName);
    commitDiv.appendChild(commitDate);
    commitDiv.appendChild(commitMessage);

    // Add commit card to commits container
    commitsContainer.appendChild(commitDiv); // Append the div to the container
  });
}

// Execute on window load
window.onload = fetchCommits;