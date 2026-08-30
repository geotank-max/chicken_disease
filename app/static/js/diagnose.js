// Interactive symptom picker for Step 2 of the diagnosis wizard.
// Handles: live search, tag management, category tab switching, Next/Prev category cycling,
// and real-time live AI candidate illness matches.
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('symptomSearch');
    if (!searchInput) return;

    const suggestionBox = document.getElementById('symptomSuggestions');
    const tagsBox = document.getElementById('symptomTags');
    const noResults = document.getElementById('symptomNoResults');
    const topIllnessesBox = document.getElementById('topIllnesses');
    const clearBtn = document.getElementById('clearSymptoms');
    const tabs = Array.from(document.querySelectorAll('.category-substep-tab'));
    const panes = Array.from(document.querySelectorAll('.symptom-category-pane'));
    const items = Array.from(document.querySelectorAll('.symptom-item'));
    const prevCatBtn = document.getElementById('prevCatBtn');
    const nextCatBtn = document.getElementById('nextCatBtn');
    const submitStep2Btn = document.getElementById('submitStep2Btn');

    // Parse diagnosis knowledge base for live prediction
    let diseaseData = { diseases: {}, symptomToDiseases: {} };
    try {
        const raw = document.getElementById('symptomDiagnosisData')?.textContent || '{}';
        const parsed = JSON.parse(raw);
        diseaseData = {
            diseases: parsed.diseases || {},
            symptomToDiseases: parsed.symptomToDiseases || {},
        };
    } catch (e) {
        console.warn('Could not parse symptomDiagnosisData', e);
    }

    // Build symptom item registry
    const symptomIndex = items.map(function (el) {
        const input = el.querySelector('input[type="checkbox"]');
        const nameEl = el.querySelector('.fw-semibold');
        const descEl = el.querySelector('.small.text-muted');
        return {
            id: el.dataset.id,
            name: (nameEl ? nameEl.textContent : '').trim(),
            search: (el.dataset.name || '').toLowerCase(),
            desc: (descEl ? descEl.textContent : '').trim(),
            category: (el.dataset.category || '').trim(),
            input: input,
            el: el,
        };
    });

    function getSelectedSymptoms() {
        return symptomIndex.filter(function (s) { return s.input && s.input.checked; });
    }

    // ── Category Switching ──
    let activeCatName = tabs[0]?.dataset.catName || 'all';

    function switchCategory(catName) {
        activeCatName = (catName || 'all').trim();

        // Update tab styling
        tabs.forEach(function (tab) {
            const isMatch = (tab.dataset.catName || '').trim() === activeCatName;
            tab.classList.toggle('active', isMatch);
        });

        // Show/hide category panes
        panes.forEach(function (pane) {
            const paneCat = (pane.dataset.paneCategory || '').trim();
            if (activeCatName === 'all') {
                pane.classList.add('active');
                pane.style.display = 'block';
            } else {
                const isMatch = paneCat === activeCatName;
                pane.classList.toggle('active', isMatch);
                pane.style.display = isMatch ? 'block' : 'none';
            }
        });

        filterSymptoms();
    }

    // Tab button click handlers
    tabs.forEach(function (tab) {
        tab.addEventListener('click', function (e) {
            e.preventDefault();
            const cat = this.dataset.catName;
            switchCategory(cat);
        });
    });

    // Next / Prev category cycling
    if (nextCatBtn) {
        nextCatBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const currentIdx = tabs.findIndex(function (t) {
                return (t.dataset.catName || '').trim() === activeCatName;
            });
            if (currentIdx === -1 || currentIdx >= tabs.length - 1) {
                // If on last tab (e.g. 'all'), scroll down or focus the Submit button!
                if (submitStep2Btn) {
                    submitStep2Btn.focus();
                    submitStep2Btn.classList.add('pulse-highlight');
                    setTimeout(function () { submitStep2Btn.classList.remove('pulse-highlight'); }, 800);
                }
            } else {
                const nextTab = tabs[currentIdx + 1];
                if (nextTab) switchCategory(nextTab.dataset.catName);
            }
        });
    }

    if (prevCatBtn) {
        prevCatBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const currentIdx = tabs.findIndex(function (t) {
                return (t.dataset.catName || '').trim() === activeCatName;
            });
            if (currentIdx > 0) {
                const prevTab = tabs[currentIdx - 1];
                if (prevTab) switchCategory(prevTab.dataset.catName);
            }
        });
    }

    // ── Live Filtering (Search + Category) ──
    function filterSymptoms() {
        const query = (searchInput.value || '').toLowerCase().trim();
        let anyVisible = false;

        symptomIndex.forEach(function (s) {
            const catMatch = activeCatName === 'all' || s.category === activeCatName;
            const searchMatch = !query || s.search.includes(query) || s.desc.toLowerCase().includes(query);
            // If user is searching, show all matches regardless of category tab
            const isVisible = query ? searchMatch : (catMatch && searchMatch);

            s.el.style.display = isVisible ? '' : 'none';
            if (isVisible) anyVisible = true;
        });

        if (noResults) noResults.classList.toggle('d-none', anyVisible);
    }

    // ── Search Suggestions ──
    function renderSuggestions() {
        const query = (searchInput.value || '').toLowerCase().trim();
        if (!query || !suggestionBox) {
            if (suggestionBox) {
                suggestionBox.classList.add('d-none');
                suggestionBox.innerHTML = '';
            }
            return;
        }

        const matches = symptomIndex.filter(function (s) {
            return !s.input.checked && (s.search.includes(query) || s.desc.toLowerCase().includes(query));
        }).slice(0, 6);

        if (matches.length === 0) {
            suggestionBox.classList.add('d-none');
            suggestionBox.innerHTML = '';
            return;
        }

        suggestionBox.innerHTML = '';
        matches.forEach(function (s) {
            const item = document.createElement('div');
            item.className = 'p-2 border-bottom cursor-pointer hover-bg-light';
            item.innerHTML = '<div class="fw-bold text-dark small">' + escapeHtml(s.name) + '</div>' +
                (s.desc ? '<div class="text-muted" style="font-size:0.75rem;">' + escapeHtml(s.desc) + '</div>' : '');
            item.addEventListener('click', function (e) {
                e.preventDefault();
                s.input.checked = true;
                searchInput.value = '';
                suggestionBox.classList.add('d-none');
                suggestionBox.innerHTML = '';
                onSelectionChanged();
                filterSymptoms();
            });
            suggestionBox.appendChild(item);
        });
        suggestionBox.classList.remove('d-none');
    }

    // ── Removable Selected Tags ──
    function renderTags() {
        if (!tagsBox) return;
        const selected = getSelectedSymptoms();
        tagsBox.innerHTML = '';
        if (selected.length === 0) {
            tagsBox.classList.add('d-none');
            return;
        }
        tagsBox.classList.remove('d-none');
        selected.forEach(function (s) {
            const tag = document.createElement('span');
            tag.className = 'symptom-tag';
            tag.innerHTML = '<span>' + escapeHtml(s.name) + '</span>';
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.innerHTML = '<i class="bi bi-x"></i>';
            btn.setAttribute('aria-label', 'Remove ' + s.name);
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                s.input.checked = false;
                onSelectionChanged();
            });
            tag.appendChild(btn);
            tagsBox.appendChild(tag);
        });
    }

    // ── Live AI Match Prediction Widget ──
    function renderTopIllnesses() {
        if (!topIllnessesBox) return;
        const selectedIds = getSelectedSymptoms().map(function (s) { return String(s.id); });

        if (selectedIds.length === 0) {
            topIllnessesBox.innerHTML = '<div class="symptom-illness-empty text-muted small text-center py-3 bg-light rounded-3">' +
                '<i class="bi bi-check2-circle d-block fs-3 mb-1 text-primary"></i>' +
                'ជ្រើសរើសរោគសញ្ញា ដើម្បីមើលការទស្សន៍ទាយជំងឺ</div>';
            return;
        }

        const scores = [];
        Object.keys(diseaseData.diseases).forEach(function (name) {
            const info = diseaseData.diseases[name];
            const diseaseSymptoms = (info.symptoms || []).map(String);
            const overlap = selectedIds.filter(function (id) {
                return diseaseSymptoms.indexOf(id) !== -1;
            }).length;
            if (overlap > 0) {
                const ratio = diseaseSymptoms.length ? overlap / diseaseSymptoms.length : 0;
                scores.push({ name: name, overlap: overlap, ratio: ratio, info: info });
            }
        });

        if (scores.length === 0) {
            topIllnessesBox.innerHTML = '<div class="text-muted small text-center py-3 bg-light rounded-3">' +
                '<i class="bi bi-info-circle me-1"></i>មិនទាន់មានជំងឺដែលត្រូវនឹងរោគសញ្ញាទេ</div>';
            return;
        }

        scores.sort(function (a, b) {
            if (b.overlap !== a.overlap) return b.overlap - a.overlap;
            return b.ratio - a.ratio;
        });

        topIllnessesBox.innerHTML = '';
        scores.slice(0, 4).forEach(function (item) {
            const pct = Math.round(item.ratio * 100);
            const row = document.createElement('div');
            row.className = 'symptom-illness-item shadow-xs mb-2 p-2 rounded-2 border-start border-4 border-success bg-white';
            row.innerHTML = '<div class="d-flex justify-content-between align-items-start">' +
                '<div>' +
                    '<div class="fw-bold text-dark small mb-0">' + escapeHtml(item.name) + '</div>' +
                    '<div class="text-muted" style="font-size: 0.72rem;">' + item.overlap + ' រោគសញ្ញាត្រូវគ្នា</div>' +
                '</div>' +
                '<div class="text-end">' +
                    '<span class="badge bg-success bg-opacity-10 text-success fw-bold">' + pct + '%</span>' +
                '</div>' +
            '</div>';
            topIllnessesBox.appendChild(row);
        });
    }

    // ── Update Badge Counts & Global State ──
    function onSelectionChanged() {
        renderTags();
        renderTopIllnesses();

        // Update category badges with count of checked symptoms
        const selected = getSelectedSymptoms();
        tabs.forEach(function (tab) {
            const cat = (tab.dataset.catName || '').trim();
            const badge = tab.querySelector('[data-category-badge]');
            if (badge) {
                const countInCat = selected.filter(function (s) { return s.category === cat; }).length;
                badge.textContent = countInCat;
                badge.classList.toggle('d-none', countInCat === 0);
            }
        });
    }

    // Checkbox change events
    symptomIndex.forEach(function (s) {
        if (s.input) {
            s.input.addEventListener('change', onSelectionChanged);
        }
    });

    // Search input events
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            filterSymptoms();
            renderSuggestions();
        });
    }

    // Clear all symptoms button (លុបការជ្រើសទាំងអស់)
    if (clearBtn) {
        clearBtn.addEventListener('click', function (e) {
            e.preventDefault();
            symptomIndex.forEach(function (s) {
                if (s.input) s.input.checked = false;
            });
            onSelectionChanged();
            filterSymptoms();
        });
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str || '';
        return div.innerHTML;
    }

    // Initial setup
    onSelectionChanged();
    switchCategory(activeCatName);
});
