const searchInput = document.getElementById('search');
const autosuggestResults = document.getElementById('autosuggest-results');

searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim();

    if (query.length > 0) {
        fetch(`/autosuggest/?search=${query}`)
            .then(response => response.json())
            .then(data => {
                autosuggestResults.innerHTML = '';
                data.slice(0,9).forEach(item => {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item')
                    if (item.type == 'country') {
                        const a = document.createElement('a');
                        a.href = `/country_details/${item.code}`;  // Add your URL or modify as needed
                        a.textContent = item.name;
                        li.appendChild(a);
                    } else {
                        li.style.cursor = 'pointer'
                        li.textContent = item.name
                        li.addEventListener('click',()=>{
                            searchInput.value = item.name
                            autosuggestResults.innerHTML=''
                        })
                    }
                    autosuggestResults.appendChild(li);
                });
            });
    } else {
        autosuggestResults.innerHTML = '';
    }
});
