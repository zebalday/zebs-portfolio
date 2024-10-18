document.addEventListener('DOMContentLoaded', function () {
    const stackSection = document.getElementById('stack');
    const projectsSection = document.getElementById('projects');

    const showStackButton = document.getElementById('show-stack');
    const showProjectsButton = document.getElementById('show-projects');

    // Initially show 'stack' and hide 'projects'
    stackSection.style.display = 'grid';
    showStackButton.classList.add('active-button');
    projectsSection.style.display = 'none';

    // Toggle to show 'stack'
    showStackButton.addEventListener('click', function () {
        stackSection.style.display = 'grid';
        showStackButton.classList.add('active-button');

        showProjectsButton.classList.remove('active-button');
        projectsSection.style.display = 'none';
    });

    // Toggle to show 'projects'
    showProjectsButton.addEventListener('click', function () {
        stackSection.style.display = 'none';
        showStackButton.classList.remove('active-button');

        projectsSection.style.display = 'grid';
        showProjectsButton.classList.add('active-button');
    });
});
