// Color chip selection
const chips = document.querySelectorAll('.chip');
const selectedColors = new Set();

chips.forEach(chip => {
    chip.addEventListener('click', () => {
        const color = chip.dataset.color;
        if (selectedColors.has(color)) {
            selectedColors.delete(color);
            chip.classList.remove('selected');
        } else {
            selectedColors.add(color);
            chip.classList.add('selected');
        }
    });
});

// Generate button
const btn = document.getElementById('generateBtn');
btn.addEventListener('click', generateBouquet);

async function generateBouquet() {
    const prompt = document.getElementById('prompt').value.trim();
    const occasion = document.getElementById('occasion').value;
    const style = document.getElementById('style').value;

    if (!prompt) {
        document.getElementById('prompt').focus();
        document.getElementById('prompt').style.borderColor = '#c0392b';
        setTimeout(() => document.getElementById('prompt').style.borderColor = '', 2000);
        return;
    }

    // Show loading
    showState('loading');
    btn.disabled = true;

    try {
        const res = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                occasion,
                style,
                colors: [...selectedColors]
            })
        });

        const data = await res.json();

        if (!res.ok || data.error) {
            showError(data.error || 'Something went wrong. Please try again.');
            return;
        }

        renderResult(data);

    } catch (err) {
        showError('Network error. Is the server running?');
    } finally {
        btn.disabled = false;
    }
}

function renderResult(data) {
    const b = data.bouquet;

    document.getElementById('bouquetName').textContent = b.bouquet_name || 'Your Bouquet';
    document.getElementById('bouquetDesc').textContent = b.description || '';
    document.getElementById('infoFlowers').textContent = Array.isArray(b.flowers) ? b.flowers.join(', ') : b.flowers || '';
    document.getElementById('infoColors').textContent = Array.isArray(b.color_palette) ? b.color_palette.join(', ') : b.color_palette || '';
    document.getElementById('infoStyle').textContent = b.arrangement_style || '';
    document.getElementById('infoSymbolism').textContent = b.symbolism || '';
    document.getElementById('infoCare').textContent = b.care_tips || '';

    const imgEl = document.getElementById('bouquetImage');
    const fallback = document.getElementById('imageFallback');

    if (data.image) {
        imgEl.src = `data:image/png;base64,${data.image}`;
        imgEl.style.display = 'block';
        fallback.style.display = 'none';
    } else {
        imgEl.style.display = 'none';
        fallback.style.display = 'flex';
    }

    showState('result');
    document.getElementById('resultContent').classList.add('fade-in');
}

function showState(state) {
    document.getElementById('placeholder').style.display = 'none';
    document.getElementById('resultContent').style.display = 'none';
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('errorState').style.display = 'none';

    if (state === 'loading') {
        document.getElementById('loadingState').style.display = 'flex';
    } else if (state === 'result') {
        document.getElementById('resultContent').style.display = 'flex';
    } else if (state === 'error') {
        document.getElementById('errorState').style.display = 'flex';
    } else {
        document.getElementById('placeholder').style.display = 'flex';
    }
}

function showError(msg) {
    document.getElementById('errorMsg').textContent = msg;
    showState('error');
}

// Allow Enter in textarea with Ctrl/Cmd
document.getElementById('prompt').addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        generateBouquet();
    }
});
