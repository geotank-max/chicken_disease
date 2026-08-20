/**
 * Offline Diagnosis Engine for IDNS
 * Caches the knowledge base in IndexedDB and runs inference client-side
 * when the network is unavailable.
 */

const DB_NAME = 'idns-kb';
const DB_VERSION = 1;
const STORE_NAME = 'knowledge_base';
const KB_KEY = 'latest';

// ─── IndexedDB helpers ─────────────────────────────────────────

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME);
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function saveKB(data) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).put(data, KB_KEY);
    tx.oncomplete = resolve;
    tx.onerror = () => reject(tx.error);
  });
}

async function loadKB() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const req = tx.objectStore(STORE_NAME).get(KB_KEY);
    req.onsuccess = () => resolve(req.result || null);
    req.onerror = () => reject(req.error);
  });
}

// ─── Sync knowledge base ───────────────────────────────────────

async function syncKnowledgeBase() {
  try {
    const resp = await fetch('/api/knowledge-base');
    if (!resp.ok) return null;
    const data = await resp.json();
    await saveKB(data);
    console.log('[IDNS] Knowledge base synced:', data.symptoms.length, 'symptoms,', data.rules.length, 'rules');
    return data;
  } catch (err) {
    console.warn('[IDNS] Could not sync knowledge base (offline?):', err.message);
    return null;
  }
}

// ─── Client-side inference engine ──────────────────────────────

const MIN_CONFIDENCE = 30.0;

function runOfflineInference(selectedSymptomIds, knowledgeBase) {
  if (!knowledgeBase || !knowledgeBase.rules) return [];

  const inputIds = new Set(selectedSymptomIds);
  const results = [];

  for (const rule of knowledgeBase.rules) {
    const ruleSymptomIds = new Set(rule.symptom_ids);
    if (ruleSymptomIds.size === 0) continue;

    const matches = [...inputIds].filter((id) => ruleSymptomIds.has(id));
    if (matches.length === 0) continue;

    const matchRatio = matches.length / ruleSymptomIds.size;
    const weighted = matchRatio * (rule.confidence || 100);
    const confidence = Math.min(Math.round(weighted * 100) / 100, 100);

    if (confidence < MIN_CONFIDENCE) continue;

    const disease = knowledgeBase.diseases.find((d) => d.id === rule.disease_id);
    if (!disease) continue;

    results.push({
      disease: disease,
      confidence: confidence,
      matched_count: matches.length,
      required_count: ruleSymptomIds.size,
      treatment: disease.treatment,
      priority: rule.priority,
    });
  }

  // Sort: confidence desc, priority asc, matched_count desc
  results.sort((a, b) => {
    if (b.confidence !== a.confidence) return b.confidence - a.confidence;
    if (a.priority !== b.priority) return a.priority - b.priority;
    return b.matched_count - a.matched_count;
  });

  return results;
}

// ─── Get symptoms grouped by category ──────────────────────────

function getSymptomsGrouped(knowledgeBase) {
  if (!knowledgeBase || !knowledgeBase.symptoms) return {};
  const grouped = {};
  for (const symptom of knowledgeBase.symptoms) {
    const cat = symptom.category_name || 'Other';
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(symptom);
  }
  return grouped;
}

// ─── Initialize: sync KB on page load ──────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  // Sync knowledge base in background (won't block page)
  syncKnowledgeBase();
});

// Expose for use in diagnosis page
window.IDNS_Offline = {
  syncKnowledgeBase,
  loadKB,
  runOfflineInference,
  getSymptomsGrouped,
};
