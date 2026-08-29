// Interactive symptom picker for Step 2 of the diagnosis wizard.
// Handles: live search with suggestions, removable tags, collapsible category
// groups, category quick-filter, and a live "Top Possible Illnesses" widget.
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('symptomSearch');
    if (!searchInput) return;

    const suggestionBox = document.getElementById('symptomSuggestions');
    const tagsBox = document.getElementById('symptomTags');
    const noResults = document.getElementById('symptomNoResults');
    const topIllnessesBox = document.getElementById('topIllnesses');
    const clearBtn = document.getElementById('clearSymptoms');
    const tabs = Array.from(document.querySelectorAll('.category-tab'));
    const groups = Array.from(document.querySelectorAll('.symptom-group'));
    const items = Array.from(document.querySelectorAll('.symptom-item'));

    let activeCategory = 'all';
    let activeSuggestion = -1;

    // ── Parse the symptom index passed from the server ──
    let diseaseData = { diseases: {}, symptomToDiseases: {} };
    try {
        const raw = document.getElementById('symptomDiagnosisData')?.textContent || '{}';
        const parsed = JSON.parse(raw);
        diseaseData = {
            diseases: parsed.diseases || {},
            symptomToDiseases: parsed.symptomToDiseases || {},
        };
    } catch (e) {
        // fall back to empty index; picker still works without suggestions
    }

    // Build a quick lookup of every symptom item: {id, name, desc, category, input, el}
    const symptomIndex = items.map(function (el) {
        const input = el.querySelector('input[type="checkbox"]');
        const nameEl = el.querySelector('.fw-semibold');
        const descEl = el.querySelector('.small.text-muted');
        return {
            id: el.dataset.id,
            name: (nameEl ? nameEl.textContent : '').trim(),
            search: (el.dataset.name || '').toLowerCase(),
            desc: (descEl ? descEl.textContent : '').trim(),
            category: el.dataset.category,
            input: input,
            el: el,
        };
    });

    function checkedInfos() {
        return symptomIndex.filter(function (s) { return s.input && s.input.checked; });
    }

    // ── Tags ──────────────────────────────────────────────────────────────
    function renderTags() {
        const selected = checkedInfos();
        tagsBox.innerHTML = '';
        if (selected.length === 0) {
            tagsBox.classList.add('d-none');
            return;
        }
        tagsBox.classList.remove('d-none');
        selected.forEach(function (s) {
            const tag = document.createElement('span');
            tag.className = 'symptom-tag';
            const label = document.createElement('span');
            label.textContent = s.name;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.setAttribute('aria-label', 'Remove ' + s.name);
            btn.innerHTML = '<i class="bi bi-x"></i>';
            btn.addEventListener('click', function () {
                s.input.checked = false;
                onSelectionChanged();
            });
            tag.appendChild(label);
            tag.appendChild(btn);
            tagsBox.appendChild(tag);
        });
    }

    // ── Group counts + collapse state ───────────────────────────────────────
    function updateGroupCounts() {
        groups.forEach(function (group) {
            const groupItems = group.querySelectorAll('.symptom-item input[type="checkbox"]');
            let count = 0;
            groupItems.forEach(function (cb) { if (cb.checked) count += 1; });
            const badge = group.querySelector('.symptom-group-count');
            if (badge) {
                badge.textContent = count;
                badge.classList.toggle('d-none', count === 0);
            }
        });
    }

    // ── Search + category filtering ─────────────────────────────────────────
    function filterSymptoms() {
        const query = (searchInput.value || '').toLowerCase().trim();
        let anyVisible = false;

        symptomIndex.forEach(function (s) {
            const catMatch = activeCategory === 'all' || s.category === activeCategory;
            const searchMatch = !query || s.search.includes(query) ||
                s.desc.toLowerCase().includes(query);
            const visible = catMatch && searchMatch;
            s.el.style.display = visible ? '' : 'none';
            if (visible) anyVisible = true;
        });

        // Hide groups that have no visible items
        groups.forEach(function (group) {
            const visibleItems = group.querySelectorAll('.symptom-item')
                ? Array.from(group.querySelectorAll('.symptom-item')).filter(function (el) {
                    return el.style.display !== 'none';
                })
                : [];
            group.style.display = visibleItems.length ? '' : 'none';
        });

        if (noResults) noResults.classList.toggle('d-none', anyVisible);
    }

    // ── Suggestions dropdown ────────────────────────────────────────────────
    function renderSuggestions() {
        const query = (searchInput.value || '').toLowerCase().trim();
        activeSuggestion = -1;
        if (!query) {
            suggestionBox.classList.add('d-none');
            suggestionBox.innerHTML = '';
            return;
        }
        const matches = symptomIndex.filter(function (s) {
            return !s.input.checked &&
                (s.search.includes(query) || s.desc.toLowerCase().includes(query));
        }).slice(0, 8);

        if (matches.length === 0) {
            suggestionBox.classList.add('d-none');
            suggestionBox.innerHTML = '';
            return;
        }

        suggestionBox.innerHTML = '';
        matches.forEach(function (s) {
            const row = document.createElement('div');
            row.className = 'symptom-suggestion';
            row.dataset.id = s.id;
            row.innerHTML = '<div class="s-name">' + escapeHtml(s.name) + '</div>' +
                (s.desc ? '<div class="s-desc">' + escapeHtml(s.desc) + '</div>' : '');
            row.addEventListener('mousedown', function (ev) {
                ev.preventDefault(); // keep focus in the input
                selectSymptom(s);
            });
            suggestionBox.appendChild(row);
        });
        suggestionBox.classList.remove('d-none');
    }

    function selectSymptom(s) {
        s.input.checked = true;
        searchInput.value = '';
        suggestionBox.classList.add('d-none');
        suggestionBox.innerHTML = '';
        onSelectionChanged();
        filterSymptoms();
    }

    function moveActiveSuggestion(dir) {
        const rows = Array.from(suggestionBox.querySelectorAll('.symptom-suggestion'));
        if (!rows.length) return;
        activeSuggestion = (activeSuggestion + dir + rows.length) % rows.length;
        rows.forEach(function (r, i) { r.classList.toggle('active', i === activeSuggestion); });
    }

    // ── Top Possible Illnesses widget ───────────────────────────────────────
    function renderTopIllnesses() {
        if (!topIllnessesBox) return;
        const selectedIds = checkedInfos().map(function (s) { return String(s.id); });

        if (selectedIds.length === 0) {
            topIllnessesBox.innerHTML = '<div class="symptom-illness-empty text-muted small">' +
                '<i class="bi bi-search me-1"></i>ជ្រើសរើសរោគសញ្ញា ដើម្បីមើលជំងឺដែលអាចទំនង</div>';
            return;
        }

        // Score each disease by how many selected symptoms it shares.
        const scores = [];
        Object.keys(diseaseData.diseases).forEach(function (name) {
            const info = diseaseData.diseases[name];
            const diseaseSymptoms = (info.symptoms || []).map(String);
            const overlap = selectedIds.filter(function (id) {
                return diseaseSymptoms.indexOf(id) !== -1;
            }).length;
            if (overlap > 0) {
                const ratio = diseaseSymptoms.length
                    ? overlap / diseaseSymptoms.length
                    : 0;
                scores.push({ name: name, overlap: overlap, ratio: ratio, info: info });
            }
        });

        if (scores.length === 0) {
            topIllnessesBox.innerHTML = '<div class="text-muted small">' +
                '<i class="bi bi-info-circle me-1"></i>មិនទាន់មានជំងឺដែលត្រូវនឹងរោគសញ្ញាទេ</div>';
            return;
        }

        scores.sort(function (a, b) {
            if (b.overlap !== a.overlap) return b.overlap - a.overlap;
            return b.ratio - a.ratio;
        });

        const top = scores.slice(0, 5);
        topIllnessesBox.innerHTML = '';
        top.forEach(function (item, idx) {
            const pct = Math.round(item.ratio * 100);
            const row = document.createElement('div');
            row.className = 'symptom-illness-item';
            const meta = [];
            if (item.info.category) meta.push(escapeHtml(item.info.category));
            meta.push(item.overlap + ' រោគសញ្ញាត្រូវគ្នា');
            row.innerHTML =
                '<span class="il-rank">' + (idx + 1) + '</span>' +
                '<div class="flex-grow-1">' +
                    '<div class="il-name">' + escapeHtml(item.name) + '</div>' +
                    '<div class="il-meta">' + meta.join(' • ') + '</div>' +
                    '<div class="il-bar"><span style="width:' + pct + '%"></span></div>' +
                '</div>';
            topIllnessesBox.appendChild(row);
        });
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // ── Central update after any selection change ───────────────────────────
    // Preserve the window scroll position: rendering tags / top-illnesses
    // mutates the DOM above the list and can otherwise shift the viewport,
    // and clicking a hidden checkbox label can nudge the page.
    function onSelectionChanged() {
        const scrollX = window.scrollX;
        const scrollY = window.scrollY;
        renderTags();
        updateGroupCounts();
        renderTopIllnesses();
        window.scrollTo(scrollX, scrollY);
    }

    // ── Wire up events ──────────────────────────────────────────────────────
    searchInput.addEventListener('input', function () {
        filterSymptoms();
        renderSuggestions();
    });

    searchInput.addEventListener('keydown', function (ev) {
        if (suggestionBox.classList.contains('d-none')) return;
        if (ev.key === 'ArrowDown') { ev.preventDefault(); moveActiveSuggestion(1); }
        else if (ev.key === 'ArrowUp') { ev.preventDefault(); moveActiveSuggestion(-1); }
        else if (ev.key === 'Enter') {
            const rows = suggestionBox.querySelectorAll('.symptom-suggestion');
            if (activeSuggestion >= 0 && rows[activeSuggestion]) {
                ev.preventDefault();
                const id = rows[activeSuggestion].dataset.id;
                const s = symptomIndex.find(function (x) { return String(x.id) === String(id); });
                if (s) selectSymptom(s);
            }
        } else if (ev.key === 'Escape') {
            suggestionBox.classList.add('d-none');
        }
    });

    // Hide suggestions when focus leaves the search area
    document.addEventListener('click', function (ev) {
        if (!ev.target.closest('.symptom-search-shell')) {
            suggestionBox.classList.add('d-none');
        }
    });

    // Checkbox changes (direct clicks on cards)
    symptomIndex.forEach(function (s) {
        if (s.input) s.input.addEventListener('change', onSelectionChanged);
    });

    // Category quick-filter pills
    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            tabs.forEach(function (t) { t.classList.remove('active'); });
            this.classList.add('active');
            activeCategory = this.dataset.category;
            filterSymptoms();
        });
    });

    // Collapsible group headers
    groups.forEach(function (group) {
        const header = group.querySelector('.symptom-group-header');
        if (!header) return;
        header.addEventListener('click', function () {
            const collapsed = group.classList.toggle('collapsed');
            header.setAttribute('aria-expanded', String(!collapsed));
        });
    });

    // Clear all selections
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            symptomIndex.forEach(function (s) { if (s.input) s.input.checked = false; });
            searchInput.value = '';
            filterSymptoms();
            onSelectionChanged();
        });
    }

    // ── Initial paint (restores selections coming back from step 3) ──
    onSelectionChanged();
    filterSymptoms();
});
