function fetchSearchResults(query) {
  const preview = document.getElementById('search-preview');

  if (query.length < 2) { // Only show dropdown for 2+ characters
    preview.style.display = 'none';
    return;
  }

  fetch('/search-preview/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: JSON.stringify({ query: query })
  })
  .then(response => response.json())
  .then(data => {
    if (data.results && data.results.length > 0) {
      preview.style.display = 'block';
      console.log(data.results)
      preview.innerHTML = data.results
        .map(item => `<li class="search-preview-list" onclick="selectResult('${item.ticker }')">
            <div>
              <div>
                <div class="search-prewiew-name">${item.name} </div>
                <div class="search-preview-ticker">${item.ticker}</div>
              </div>
            </div>
            <div>
              <div>
                <span>NASDAQ</span>
              </div>
            </div>
          </li>`)
        .join('');
    } else {
      preview.style.display = 'none';
    }
  })
  .catch(error => {
    console.error('Error fetching search results:', error);
    preview.style.display = 'none';
  });
}

function selectResult(value) {
  const searchField = document.getElementById('search');
  searchField.value = value; // Set the selected value in the input field
  document.getElementById('search-preview').style.display = 'none'; // Hide the dropdown
}
