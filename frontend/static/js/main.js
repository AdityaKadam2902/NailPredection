(function () {
  'use strict';

  const CONFIG = {
    MAX_FILE_SIZE: 10 * 1024 * 1024,
    ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/bmp', 'image/webp'],
    ALLOWED_EXTENSIONS: ['.jpg', '.jpeg', '.png', '.bmp', '.webp'],
    API_ENDPOINT: '/api/predict',
  };

  /* ── Helpers ─────────────────────────────────────────── */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  function esc(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  /* ── Header: scroll + active nav ─────────────────────── */
  function initHeader() {
    const header = $('#site-header');
    if (!header) return;

    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 8);
    }, { passive: true });

    const path = window.location.pathname.split('/').pop() || '';
    $$('.nav-link, .nav-cta').forEach(link => {
      const href = (link.getAttribute('href') || '').replace(/^\//, '');
      const isCurrent =
        href === path ||
        (href === '' && (path === '' || path === 'index.html')) ||
        (href === '/' && path === '');
      if (isCurrent) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });

    const toggle = $('.menu-toggle');
    const nav = $('.main-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', () => {
        const open = nav.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open);
      });
      document.addEventListener('click', e => {
        if (!nav.contains(e.target) && !toggle.contains(e.target)) {
          nav.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    }
  }

  /* ── FAQ ─────────────────────────────────────────────── */
  function initFAQ() {
    $$('.faq-item').forEach(item => {
      const btn = item.querySelector('.faq-q');
      if (!btn) return;
      btn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        $$('.faq-item.open').forEach(o => {
          o.classList.remove('open');
          o.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
        });
        if (!isOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  /* ── Upload / Prediction ─────────────────────────────── */
  function initUpload() {
    const dropZone    = $('#dropZone');
    if (!dropZone) return;

    const fileInput       = $('#fileInput');
    const dropzoneIdle    = $('#dropzoneIdle');
    const dropzonePreview = $('#dropzonePreview');
    const previewImg      = $('#previewImg');
    const previewMeta     = $('#previewMeta');
    const predictBtn      = $('#predictBtn');
    const clearBtn        = $('#clearBtn');
    const errorMsg        = $('#errorMessage');
    const loadingState    = $('#loadingState');
    const resultsPanel    = $('#resultsPanel');
    const resultBlock     = $('#resultBlock');

    let currentFile = null;
    let currentObjectURL = null;

    /* Drag events */
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev => {
      dropZone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); });
    });
    ['dragenter', 'dragover'].forEach(ev => dropZone.addEventListener(ev, () => dropZone.classList.add('dragover')));
    ['dragleave', 'drop'].forEach(ev => dropZone.addEventListener(ev, () => dropZone.classList.remove('dragover')));
    dropZone.addEventListener('drop', e => {
      const files = e.dataTransfer?.files;
      if (files && files.length) handleFile(files[0]);
    });

    /* Keyboard activate */
    dropZone.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
    });

    fileInput.addEventListener('change', e => {
      if (e.target.files.length) handleFile(e.target.files[0]);
    });

    if (predictBtn) {
      predictBtn.addEventListener('click', runPrediction);
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', resetAll);
    }

    /* Validate */
    function validate(file) {
      if (!file) return 'No file selected.';
      if (file.size === 0) return 'The selected file is empty.';
      if (file.size > CONFIG.MAX_FILE_SIZE) return `File too large — maximum is ${CONFIG.MAX_FILE_SIZE / 1024 / 1024} MB.`;
      const ext = '.' + file.name.split('.').pop().toLowerCase();
      if (!CONFIG.ALLOWED_EXTENSIONS.includes(ext)) return `Unsupported format: ${ext}. Use JPG, PNG, or WebP.`;
      return null;
    }

    function handleFile(file) {
      const err = validate(file);
      if (err) { showError(err); return; }
      hideError();
      currentFile = file;

      if (currentObjectURL) URL.revokeObjectURL(currentObjectURL);
      currentObjectURL = URL.createObjectURL(file);

      previewImg.src = currentObjectURL;
      previewMeta.textContent = `${file.name}  ·  ${(file.size / 1024).toFixed(1)} KB`;
      dropzoneIdle.style.display = 'none';
      dropzonePreview.style.display = 'block';

      predictBtn.disabled = false;
      clearBtn.classList.remove('hidden');
      resultsPanel.classList.add('hidden');
      resultBlock.innerHTML = '';
    }

    async function runPrediction() {
      if (!currentFile) { showError('Please select an image first.'); return; }
      hideError();
      setLoading(true);

      const fd = new FormData();
      fd.append('file', currentFile);

      try {
        const res  = await fetch(CONFIG.API_ENDPOINT, { method: 'POST', body: fd });
        const data = await res.json();
        if (!res.ok || !data.success) throw new Error(data.error?.message || 'Prediction failed.');
        renderResults(data.data, currentObjectURL);
      } catch (err) {
        showError(err.message || 'Could not reach the server. Please try again.');
      } finally {
        setLoading(false);
      }
    }

    function setLoading(on) {
      if (on) {
        loadingState.classList.remove('hidden');
        predictBtn.disabled = true;
        predictBtn.innerHTML = '<span style="display:inline-block;width:15px;height:15px;border:2px solid rgba(255,255,255,0.3);border-top-color:#fff;border-radius:50%;animation:spin 0.9s linear infinite;vertical-align:middle;margin-right:8px;"></span>Analyzing…';
        resultsPanel.classList.add('hidden');
      } else {
        loadingState.classList.add('hidden');
        predictBtn.disabled = false;
        predictBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/><path d="M6 5.5l4 2.5-4 2.5V5.5z" fill="currentColor"/></svg> Analyze Image';
      }
    }

    function renderResults(data, imgUrl) {
      const pred     = data.prediction;
      const info     = data.disease_info;
      const top      = data.top_predictions || [];
      const lvl      = (pred.confidence_level || 'low').toLowerCase();
      const sev      = (info.severity || 'moderate').toLowerCase();

      const sevClass = sev === 'low' ? 'sev-low' : sev === 'high' ? 'sev-high' : 'sev-moderate';
      const sevLabel = info.severity || 'Moderate';

      const altRows = top.map((p, i) => `
        <div class="alt-row">
          <span class="alt-rank${i === 0 ? ' is-top' : ''}">${p.rank}</span>
          <span class="alt-name">${esc(p.disease_name)}</span>
          <div class="alt-bar-track"><div class="alt-bar-fill${i === 0 ? ' is-top' : ''}" style="width:0%" data-w="${p.confidence}%"></div></div>
          <span class="alt-pct">${p.confidence.toFixed(1)}%</span>
        </div>
      `).join('');

      const symptoms = (info.symptoms || []).map(s => `<span class="symptom-chip">${esc(s)}</span>`).join('');

      resultBlock.innerHTML = `
        <div class="result-top">
          <img src="${imgUrl}" alt="Analyzed nail image" class="result-nail-img">
          <div class="result-meta-group">
            <div class="result-meta-label">Detected Condition</div>
            <div class="result-condition">${esc(pred.disease_name)}</div>
            <span class="sev-pill ${sevClass}">${sevLabel} Severity</span>
          </div>
        </div>

        <div class="result-confidence">
          <div class="conf-row">
            <span class="conf-label">AI Confidence</span>
            <span class="conf-value ${lvl}">${pred.confidence.toFixed(1)}%</span>
          </div>
          <div class="conf-track">
            <div class="conf-fill ${lvl}" style="width:0%" data-w="${pred.confidence}%"></div>
          </div>
        </div>

        <div class="result-info">
          <div class="info-row">
            <div>
              <div class="info-row-label">Description</div>
              <div class="info-row-text">${esc(info.description)}</div>
            </div>
          </div>
          ${symptoms ? `
          <div class="info-row">
            <div>
              <div class="info-row-label">Observable Symptoms</div>
              <div class="symptom-chips">${symptoms}</div>
            </div>
          </div>` : ''}
          <div class="info-row">
            <div>
              <div class="info-row-label">Recommended Next Steps</div>
              <div class="info-row-text">${esc(info.next_steps)}</div>
            </div>
          </div>
        </div>

        ${top.length ? `
        <div class="result-alts">
          <div class="alts-title">Alternative Predictions</div>
          ${altRows}
        </div>` : ''}

        <div class="result-actions">
          <button type="button" class="btn btn-outline" id="resetBtn">Upload Another Image</button>
        </div>
      `;

      resultsPanel.classList.remove('hidden');
      resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });

      /* Animate bars after paint */
      requestAnimationFrame(() => {
        setTimeout(() => {
          resultBlock.querySelectorAll('[data-w]').forEach(el => {
            el.style.width = el.getAttribute('data-w');
          });
        }, 80);
      });

      /* Reset button */
      $('#resetBtn', resultBlock)?.addEventListener('click', resetAll);
    }

    function resetAll() {
      currentFile = null;
      if (currentObjectURL) { URL.revokeObjectURL(currentObjectURL); currentObjectURL = null; }
      fileInput.value = '';
      previewImg.src = '';
      previewMeta.textContent = '';
      dropzonePreview.style.display = 'none';
      dropzoneIdle.style.display = 'block';
      predictBtn.disabled = true;
      predictBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/><path d="M6 5.5l4 2.5-4 2.5V5.5z" fill="currentColor"/></svg> Analyze Image';
      clearBtn.classList.add('hidden');
      resultsPanel.classList.add('hidden');
      resultBlock.innerHTML = '';
      hideError();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showError(msg) {
      if (!errorMsg) return;
      errorMsg.textContent = msg;
      errorMsg.classList.remove('hidden');
    }

    function hideError() {
      if (!errorMsg) return;
      errorMsg.classList.add('hidden');
    }
  }

  /* ── Boot ────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initFAQ();
    initUpload();
  });
})();
