// Toggle between showing and hiding the sidebar when clicking the menu icon
var mySidebar = document.getElementById("mySidebar");

function w3_open() {
  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
    overlayBg.style.display = "none";
  } else {
    mySidebar.style.display = 'block';
    overlayBg.style.display = "block";
  }
}

// Close the sidebar with the close button
function w3_close() {
  mySidebar.style.display = "none";
  overlayBg.style.display = "none";
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth'
      });
      // Close sidebar on mobile after clicking
      if (window.innerWidth <= 768) {
        w3_close();
      }
    }
  });
});

// Search functionality
function searchPosts() {
  const input = document.getElementById('searchInput');
  const filter = input.value.toLowerCase();
  const blogList = document.getElementById('blogList');
  const posts = blogList.getElementsByClassName('blog-post');

  for (let post of posts) {
    const title = post.getAttribute('data-title');
    const excerpt = post.getAttribute('data-excerpt');
    if (title.includes(filter) || excerpt.includes(filter)) {
      post.style.display = "";
    } else {
      post.style.display = "none";
    }
  }
} 