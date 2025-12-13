const statusDiv = document.querySelector('#status-div');
const uploadForm = document.querySelector('#upload-form');
const companiesTableBody = document.querySelector('#companies-table-body');
const scrapeButton = document.querySelector('#scrape-selected');

function setStatus(message, state = 'waiting') {
  if (!statusDiv) return;
  statusDiv.textContent = message;
  statusDiv.classList.remove('alert-secondary', 'alert-danger', 'alert-success');
  const className = state === 'running' ? 'alert-success' : state === 'error' ? 'alert-danger' : 'alert-secondary';
  statusDiv.classList.add(className);
}

async function fetchCompanies(limit = 50) {
  try {
    const response = await fetch(`/fetch_companies/?limit=${limit}`);
    const payload = await response.json();
    if (payload.status === 'success') {
      renderCompanies(payload.data || []);
      setStatus(`Loaded ${payload.data.length} companies from Supabase.`);
    } else {
      throw new Error(payload.message || 'Unknown error');
    }
  } catch (error) {
    console.error('Error loading companies', error);
    setStatus('Unable to load companies. Check Supabase credentials.', 'error');
  }
}

function renderCompanies(companies) {
  if (!companiesTableBody) return;
  companiesTableBody.innerHTML = '';

  companies.forEach((company, index) => {
    const row = document.createElement('tr');
    const checkboxCell = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.dataset.companyId = company.id;
    checkbox.dataset.companyUrl = company.url;
    checkbox.classList.add('company-checkbox');
    checkboxCell.appendChild(checkbox);

    const nameCell = document.createElement('td');
    nameCell.textContent = company.company_name || 'Unknown';

    const urlCell = document.createElement('td');
    const urlLink = document.createElement('a');
    urlLink.href = company.url;
    urlLink.textContent = company.url;
    urlLink.target = '_blank';
    urlCell.appendChild(urlLink);

    const careerCell = document.createElement('td');
    const careerLink = document.createElement('a');
    careerLink.href = company.career_page_url || '#';
    careerLink.textContent = company.career_page_url ? 'Career Page' : 'Unknown';
    careerLink.target = '_blank';
    careerCell.appendChild(careerLink);

    const rolesCell = document.createElement('td');
    rolesCell.textContent = company.roles?.length ? `${company.roles.length} tracked` : '0';

    row.appendChild(checkboxCell);
    row.appendChild(nameCell);
    row.appendChild(urlCell);
    row.appendChild(careerCell);
    row.appendChild(rolesCell);
    companiesTableBody.appendChild(row);
  });
}

async function handleUpload(event) {
  event.preventDefault();
  if (!uploadForm) return;
  const formData = new FormData(uploadForm);
  setStatus('Uploading and parsing CSV...', 'running');

  try {
    const response = await fetch('/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    setStatus('Upload complete. Supabase is being updated.');
    await fetchCompanies();
  } catch (error) {
    console.error('Upload failed', error);
    setStatus('Error during upload.', 'error');
  }
}

async function handleScrapeSelected() {
  const selected = Array.from(document.querySelectorAll('.company-checkbox:checked')).map((checkbox) => ({
    id: checkbox.dataset.companyId,
    url: checkbox.dataset.companyUrl,
  }));

  if (!selected.length) {
    setStatus('Select at least one company to scrape.', 'error');
    return;
  }

  try {
    setStatus('Scraping selected companies...', 'running');
    const response = await fetch('/start_scraping/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      body: JSON.stringify({ selectedRows: selected }),
    });

    const payload = await response.json();
    if (payload.status !== 'success') {
      throw new Error(payload.message || 'Scrape failed');
    }

    setStatus('Scrape triggered. Refreshing data...');
    await fetchCompanies();
  } catch (error) {
    console.error('Scrape failed', error);
    setStatus('Unable to start scraping.', 'error');
  }
}

if (uploadForm) {
  uploadForm.addEventListener('submit', handleUpload);
}

if (scrapeButton) {
  scrapeButton.addEventListener('click', handleScrapeSelected);
}

fetchCompanies();
