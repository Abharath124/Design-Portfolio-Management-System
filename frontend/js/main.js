// admin-main.js
console.log('main.js loaded');

// Use the same host as the page, port 5000 for Flask
// const API = `${location.protocol}//${location.hostname}:5000/api`;
const API = `http://localhost:5000/api`;
console.log('API base =', API);

// helper to log fetch and parse response
async function call(path, opts = {}) {
    console.log('CALL', path, opts);
    try {
        console.log(API + path + opts);

        const res = await fetch(API + path, opts);
        const text = await res.text();
        let json;
        try { json = JSON.parse(text); } catch (e) { json = { raw: text }; }
        console.log('RESP', res.status, json);
        if (!res.ok) throw { status: res.status, body: json };
        return json;
    } catch (err) {
        console.error('FETCH ERROR', err);
        throw err;
    }
}

async function fetchProjects() { return call('/projects', { method: 'GET' }); }
async function getProject(id) { return call('/projects/' + id, { method: 'GET' }); }
async function renderGallery() {
    const gallery = document.getElementById('gallery');

    if (!gallery) return; // not on index.html

    const searchEl = document.getElementById('search');
    const categoryEl = document.getElementById('filterCategory');
    const yearEl = document.getElementById('filterYear');

    async function load() {
        try {
            const params = {};
            if (searchEl && searchEl.value) params.q = searchEl.value;
            if (categoryEl && categoryEl.value) params.category = categoryEl.value;
            if (yearEl && yearEl.value) params.year = yearEl.value;

            const projects = await fetchProjects(params);

            if (!Array.isArray(projects)) {
                gallery.innerHTML = '<p>Invalid response from API</p>';
                console.log('projects not array', projects);
                return;
            }

            if (projects.length === 0) {
                gallery.innerHTML = '<p>No projects found.</p>';
                return;
            }

            gallery.innerHTML = projects.map(p => `
        <div class="card">
          <img src="${(p.imageUrls && p.imageUrls[0]) || 'https://via.placeholder.com/400x240'}" alt="${p.title}" />
          <div class="card-body">
            <h3>${p.title}</h3>
            <p class="muted">${p.category || ''} ${p.completionYear ? '• ' + p.completionYear : ''}</p>
            <p>${(p.description || '').substring(0, 120)}...</p>
            <div class="card-actions">
              <a href="project.html?id=${p.id}">View</a>
            </div>
          </div>
        </div>
      `).join('');
        } catch (e) {
            console.error('Error loading gallery', e);
            gallery.innerHTML = '<p>Error loading projects — check console</p>';
        }
    }

    if (searchEl) searchEl.addEventListener('input', load);
    if (categoryEl) categoryEl.addEventListener('change', load);
    if (yearEl) yearEl.addEventListener('change', load);

    // initial load
    load();
}
async function renderProjectPage() {
    const container = document.getElementById('projectContent');
    if (!container) return; // not on project.html

    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    if (!id) {
        container.innerHTML = '<p>No project selected.</p>';
        return;
    }

    try {
        const p = await getProject(id);
        container.innerHTML = `
      <h2>${p.title}</h2>
      <p class="muted">${p.category || ''} ${p.completionYear ? '• ' + p.completionYear : ''}</p>
      <div class="images">
        ${(p.imageUrls || []).map(url => `<img src="${url}" />`).join('')}
      </div>
      <p>${p.description}</p>
      <p><strong>Tools:</strong> ${(p.tools || []).join(', ')}</p>
      <p><strong>Tags:</strong> ${(p.tags || []).join(', ')}</p>
      ${p.projectUrl ? `<p><a href="${p.projectUrl}" target="_blank">Open Project</a></p>` : ''}
    `;
    } catch (e) {
        console.error('Error loading project', e);
        container.innerHTML = '<p>Error loading project — check console.</p>';
    }
}
async function createProject(data) {
    return call('/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
}
async function updateProject(id, data) {
    return call('/projects/' + id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
}
async function deleteProject(id) { return call('/projects/' + id, { method: 'DELETE' }); }

/* ---------- Admin UI logic ---------- */
const form = document.getElementById('projectForm');
const list = document.getElementById('list');

function toArr(s) {
    if (!s) return [];
    return String(s).split(',').map(x => x.trim()).filter(Boolean);
}

function readForm() {
    const fd = Object.fromEntries(new FormData(form).entries());
    return {
        title: fd.title,
        description: fd.description,
        category: fd.category || '',
        tools: toArr(fd.tools),
        imageUrls: toArr(fd.imageUrls),
        projectUrl: fd.projectUrl || '',
        clientName: fd.clientName || '',
        completionYear: fd.completionYear ? Number(fd.completionYear) : null,
        tags: toArr(fd.tags),
        isFeatured: !!form.querySelector('[name=isFeatured]').checked
    };
}

if (list) {

    async function loadList() {
        try {
            const projects = await fetchProjects();
            if (!Array.isArray(projects)) { list.innerHTML = '<p>Invalid response</p>'; console.log('projects not array', projects); return; }
            list.innerHTML = projects.map(p => `
          <div class="row">
            <div style="flex:1">
              <strong>${p.title}</strong> <small>${p.category || ''} ${p.completionYear ? '• ' + p.completionYear : ''}</small>
            </div>
            <div>
              <button class="edit" data-id="${p.id}">Edit</button>
              <button class="del" data-id="${p.id}">Delete</button>
            </div>
          </div>
        `).join('');
            // bind buttons
            list.querySelectorAll('.edit').forEach(b => b.onclick = async (e) => {
                const id = e.target.dataset.id;
                const p = await getProject(id);
                form.id.value = p.id;
                form.title.value = p.title;
                form.description.value = p.description;
                form.category.value = p.category || '';
                form.tools.value = (p.tools || []).join(', ');
                form.imageUrls.value = (p.imageUrls || []).join(', ');
                form.projectUrl.value = p.projectUrl || '';
                form.clientName.value = p.clientName || '';
                form.completionYear.value = p.completionYear || '';
                form.tags.value = (p.tags || []).join(', ');
                form.isFeatured.checked = !!p.isFeatured;
                document.getElementById('formTitle').innerText = 'Edit Project';
            });
            list.querySelectorAll('.del').forEach(b => b.onclick = async (e) => {
                const id = e.target.dataset.id;
                if (!confirm('Delete project?')) return;
                await deleteProject(id);
                await loadList();
            });
        } catch (err) {
            console.error('loadList failed', err);
            list.innerHTML = '<p>Error loading projects. See console.</p>';
        }
    }
    loadList();
}

if (form) {

    form.addEventListener('submit', async (ev) => {
        ev.preventDefault();
        try {
            const id = form.id.value;
            const data = readForm();
            if (!data.title || !data.description) {
                alert('Title and description required');
                return;
            }
            if (id) {
                await updateProject(id, data);
                alert('Project updated');
            } else {
                await createProject(data);
                alert('Project created');
            }
            form.reset();
            form.id.value = '';
            document.getElementById('formTitle').innerText = 'Add Project';
            await loadList();
        } catch (err) {
            console.error('submit error', err);
            alert('Submit failed — check console');
        }
    });

}
const resetButton = document.getElementById('resetBtn');
if (resetButton) {
    resetButton.addEventListener('click', () => {
        form.reset(); form.id.value = ''; document.getElementById('formTitle').innerText = 'Add Project';
    });
}


document.addEventListener('DOMContentLoaded', () => {
    renderGallery();
    renderProjectPage();
});