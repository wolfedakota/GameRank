document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#profileDropdown').addEventListener('click', function(e) {
      e.preventDefault(); 
      e.stopPropagation(); 
  

      const dropdown = new bootstrap.Dropdown(document.querySelector('#profileDropdown'));
      dropdown.toggle();
    });
  });