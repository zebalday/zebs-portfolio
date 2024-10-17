// Update time function
function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const formattedTime = `${hours}:${minutes}:${seconds}`;
    
    // Update the h3 element within the 'header-time' container
    document.querySelector('#header-time h1').innerHTML = formattedTime;
  }

// Run the function every 5 seconds (5000 ms)
setInterval(updateTime, 1000);

// Optional: Update the time immediately on page load
window.onload = updateTime;