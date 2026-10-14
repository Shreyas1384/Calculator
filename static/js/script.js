/**
 * Shrey's Calc - Modern Scientific Calculator Controller
 * Single-line contiguous expression builder with Python backend integration.
 */

class ShreysCalculator {
    constructor() {
        this.expression = '0';
        this.previousEquation = '';
        this.memory = 0;
        this.angleMode = 'DEG'; // 'DEG' or 'RAD'
        this.is2ndActive = false;
        this.isEvaluated = false;
        this.soundEnabled = true;
        this.themes = ['dark', 'cyberpunk', 'light'];
        this.currentThemeIndex = 0;

        // Audio Context (initialized on first interaction)
        this.audioCtx = null;

        // DOM Elements
        this.initDOMElements();
        this.bindEvents();
        this.loadSettings();
        this.fetchHistory();
        this.updateDisplay();
    }

    initDOMElements() {
        this.mainDisplay = document.getElementById('main-display');
        this.expressionPreview = document.getElementById('expression-preview');
        this.liveEvalPreview = document.getElementById('live-eval-preview');
        this.memIndicator = document.getElementById('mem-indicator');
        this.angleBadge = document.getElementById('angle-badge');
        this.degRadBtn = document.getElementById('deg-rad-btn');
        this.angleModeLabel = document.getElementById('angle-mode-label');
        this.copyBtn = document.getElementById('copy-btn');
        this.soundBtn = document.getElementById('sound-btn');
        this.themeBtn = document.getElementById('theme-btn');
        this.historyToggleBtn = document.getElementById('history-toggle-btn');
        this.closeHistoryBtn = document.getElementById('close-history-btn');
        this.clearHistoryBtn = document.getElementById('clear-history-btn');
        this.historyPanel = document.getElementById('history-panel');
        this.historyList = document.getElementById('history-list');
        this.sciToggleBtn = document.getElementById('btn-sci-toggle');
        this.sciTray = document.getElementById('sci-tray');
        this.btn2nd = document.getElementById('btn-2nd');
        this.btnSin = document.getElementById('btn-sin');
        this.btnCos = document.getElementById('btn-cos');
        this.btnTan = document.getElementById('btn-tan');
        this.toast = document.getElementById('toast');
    }

    bindEvents() {
        // Standard Keypad & Sci Keypad
        document.querySelectorAll('.keypad-grid .btn, .scientific-panel .btn-sci, .memory-bar .mem-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.playSound(600, 0.03);
                this.handleButtonPress(btn);
            });
        });

        // DEG / RAD Toggle
        this.degRadBtn.addEventListener('click', () => this.toggleAngleMode());

        // 2nd Function Toggle (Inverse Trig)
        this.btn2nd.addEventListener('click', () => this.toggle2nd());

        // Toggle Scientific Tray
        this.sciToggleBtn.addEventListener('click', () => {
            this.sciToggleBtn.classList.toggle('active');
            this.sciTray.classList.toggle('open');
        });

        // History Drawer Toggle
        this.historyToggleBtn.addEventListener('click', () => {
            this.historyPanel.classList.toggle('mobile-open');
        });
        this.closeHistoryBtn.addEventListener('click', () => {
            this.historyPanel.classList.remove('mobile-open');
        });

        // Clear History
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());

        // Copy button
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());

        // Sound Toggle
        this.soundBtn.addEventListener('click', () => {
            this.soundEnabled = !this.soundEnabled;
            this.soundBtn.style.opacity = this.soundEnabled ? '1' : '0.4';
            this.showToast(this.soundEnabled ? 'Sound enabled' : 'Sound muted');
            localStorage.setItem('shreys_calc_sound', this.soundEnabled ? 'true' : 'false');
        });

        // Theme Toggle
        this.themeBtn.addEventListener('click', () => this.cycleTheme());

        // Global Keyboard Navigation
        window.addEventListener('keydown', (e) => this.handleKeyboardInput(e));
    }

    loadSettings() {
        const savedSound = localStorage.getItem('shreys_calc_sound');
        if (savedSound !== null) {
            this.soundEnabled = savedSound === 'true';
            this.soundBtn.style.opacity = this.soundEnabled ? '1' : '0.4';
        }

        const savedTheme = localStorage.getItem('shreys_calc_theme');
        if (savedTheme && this.themes.includes(savedTheme)) {
            this.currentThemeIndex = this.themes.indexOf(savedTheme);
            document.documentElement.setAttribute('data-theme', savedTheme);
        }

        const savedAngle = localStorage.getItem('shreys_calc_angle');
        if (savedAngle && ['DEG', 'RAD'].includes(savedAngle)) {
            this.angleMode = savedAngle;
            this.updateAngleModeDisplay();
        }
    }

    toggleAngleMode() {
        this.angleMode = this.angleMode === 'DEG' ? 'RAD' : 'DEG';
        this.updateAngleModeDisplay();
        localStorage.setItem('shreys_calc_angle', this.angleMode);
        this.showToast(`Angle Mode: ${this.angleMode}`);
        this.updateLivePreview();
    }

    updateAngleModeDisplay() {
        this.angleModeLabel.textContent = this.angleMode;
        this.angleBadge.textContent = this.angleMode;
    }

    toggle2nd() {
        this.is2ndActive = !this.is2ndActive;
        this.btn2nd.classList.toggle('active-2nd', this.is2ndActive);

        if (this.is2ndActive) {
            this.btnSin.textContent = 'sin⁻¹';
            this.btnCos.textContent = 'cos⁻¹';
            this.btnTan.textContent = 'tan⁻¹';
            this.btnSin.setAttribute('data-fn', 'asin');
            this.btnCos.setAttribute('data-fn', 'acos');
            this.btnTan.setAttribute('data-fn', 'atan');
        } else {
            this.btnSin.textContent = 'sin';
            this.btnCos.textContent = 'cos';
            this.btnTan.textContent = 'tan';
            this.btnSin.setAttribute('data-fn', 'sin');
            this.btnCos.setAttribute('data-fn', 'cos');
            this.btnTan.setAttribute('data-fn', 'tan');
        }
    }

    cycleTheme() {
        this.currentThemeIndex = (this.currentThemeIndex + 1) % this.themes.length;
        const newTheme = this.themes[this.currentThemeIndex];
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('shreys_calc_theme', newTheme);
        this.showToast(`Theme: ${newTheme.toUpperCase()}`);
    }

    playSound(freq = 600, duration = 0.03) {
        if (!this.soundEnabled) return;
        try {
            if (!this.audioCtx) {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                this.audioCtx = new AudioContext();
            }
            if (this.audioCtx.state === 'suspended') {
                this.audioCtx.resume();
            }
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);

            gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + duration);

            osc.connect(gain);
            gain.connect(this.audioCtx.destination);

            osc.start();
            osc.stop(this.audioCtx.currentTime + duration);
        } catch (e) {}
    }

    // --- User Actions ---
    handleButtonPress(btn) {
        const digit = btn.getAttribute('data-digit');
        const operator = btn.getAttribute('data-operator');
        const action = btn.getAttribute('data-action');
        const fn = btn.getAttribute('data-fn');

        if (digit !== null) {
            this.inputDigit(digit);
        } else if (operator !== null) {
            this.inputOperator(operator);
        } else if (fn !== null) {
            this.handleScientificFunction(fn);
        } else if (action !== null) {
            this.handleAction(action);
        }

        this.updateDisplay();
    }

    inputDigit(digit) {
        if (this.isEvaluated) {
            this.expression = digit;
            this.isEvaluated = false;
        } else if (this.expression === '0') {
            this.expression = digit;
        } else {
            this.expression += digit;
        }
        this.updateLivePreview();
    }

    inputOperator(op) {
        if (this.isEvaluated) {
            this.isEvaluated = false;
        }

        const trimmed = this.expression.trim();
        // Check if trailing ends with an operator: replace it
        if (/[\+\-×÷\^%]$/.test(trimmed)) {
            this.expression = trimmed.slice(0, -1).trim() + ` ${op} `;
        } else {
            this.expression = `${trimmed} ${op} `;
        }
    }

    inputDecimal() {
        if (this.isEvaluated) {
            this.expression = '0.';
            this.isEvaluated = false;
            return;
        }

        // Get the current operand (last number chunk after operator or parenthesis)
        const parts = this.expression.split(/[\s\+\-×÷\^%\(\)]+/);
        const lastPart = parts[parts.length - 1];

        if (!lastPart.includes('.')) {
            if (this.expression.endsWith(' ') || this.expression === '') {
                this.expression += '0.';
            } else {
                this.expression += '.';
            }
        }
    }

    negate() {
        if (this.expression === '0') return;

        // Try to toggle negation on the last operand
        const match = this.expression.match(/(-?\d+(\.\d+)?)$/);
        if (match) {
            const numStr = match[0];
            const startIdx = match.index;
            if (numStr.startsWith('-')) {
                this.expression = this.expression.substring(0, startIdx) + numStr.substring(1);
            } else {
                this.expression = this.expression.substring(0, startIdx) + '-' + numStr;
            }
        } else {
            this.expression = `-(${this.expression})`;
        }
        this.updateLivePreview();
    }

    percent() {
        const match = this.expression.match(/(\d+(\.\d+)?)$/);
        if (match) {
            const val = parseFloat(match[0]);
            const pct = val / 100;
            this.expression = this.expression.substring(0, match.index) + String(pct);
            this.updateLivePreview();
        }
    }

    handleScientificFunction(fn) {
        if (this.isEvaluated) {
            this.isEvaluated = false;
        }

        const trimmed = this.expression.trim();

        switch (fn) {
            // Function with parentheses: sin, cos, tan, asin, acos, atan, ln, log, exp, sqrt, cbrt, abs
            case 'sin':
            case 'cos':
            case 'tan':
            case 'asin':
            case 'acos':
            case 'atan':
            case 'ln':
            case 'log':
            case 'exp':
            case 'sqrt':
            case 'cbrt':
            case 'abs':
                const fnName = fn === 'log' ? 'log' : fn;
                if (trimmed === '0' || trimmed === '') {
                    this.expression = `${fnName}(`;
                } else if (/[\+\-×÷\^%(\s]$/.test(trimmed)) {
                    this.expression += `${fnName}(`;
                } else {
                    // Wrap last number or expression
                    this.expression = `${fnName}(${trimmed})`;
                }
                break;

            case 'sqr':
                this.expression = (trimmed === '0') ? '0' : `(${trimmed}) ^ 2`;
                break;
            case 'cube':
                this.expression = (trimmed === '0') ? '0' : `(${trimmed}) ^ 3`;
                break;
            case 'power':
                this.inputOperator('^');
                break;
            case 'reciprocal':
                this.expression = (trimmed === '0') ? '1 / ' : `1 / (${trimmed})`;
                break;
            case 'fact':
                this.expression = `${trimmed}!`;
                break;
            case 'pi':
                if (trimmed === '0' || trimmed === '') this.expression = 'π';
                else if (/[\+\-×÷\^%(\s]$/.test(trimmed)) this.expression += 'π';
                else this.expression += ' × π';
                break;
            case 'e':
                if (trimmed === '0' || trimmed === '') this.expression = 'e';
                else if (/[\+\-×÷\^%(\s]$/.test(trimmed)) this.expression += 'e';
                else this.expression += ' × e';
                break;
            case 'paren-open':
                if (trimmed === '0') this.expression = '(';
                else if (/[\+\-×÷\^%(\s]$/.test(trimmed)) this.expression += '(';
                else this.expression += ' × (';
                break;
            case 'paren-close':
                this.expression += ')';
                break;
            case 'mod':
                this.inputOperator('mod');
                break;
        }
        this.updateLivePreview();
    }

    handleAction(action) {
        switch (action) {
            case 'clear':
                this.clearAll();
                break;
            case 'backspace':
                this.backspace();
                break;
            case 'decimal':
                this.inputDecimal();
                break;
            case 'negate':
                this.negate();
                break;
            case 'percent':
                this.percent();
                break;
            case 'calculate':
                this.calculateResult();
                break;
            case 'mc':
                this.memory = 0;
                this.updateMemoryDisplay();
                this.showToast('Memory Cleared');
                break;
            case 'mr':
                if (this.expression === '0' || this.isEvaluated) {
                    this.expression = String(this.memory);
                } else if (/[\+\-×÷\^%(\s]$/.test(this.expression.trim())) {
                    this.expression += String(this.memory);
                } else {
                    this.expression += ` × ${this.memory}`;
                }
                this.isEvaluated = false;
                this.showToast(`Recalled Memory: ${this.memory}`);
                this.updateLivePreview();
                break;
            case 'm-plus':
                this.memory += parseFloat(this.expression) || 0;
                this.updateMemoryDisplay();
                this.showToast(`M+: ${this.memory}`);
                break;
            case 'm-minus':
                this.memory -= parseFloat(this.expression) || 0;
                this.updateMemoryDisplay();
                this.showToast(`M−: ${this.memory}`);
                break;
        }
    }

    clearAll() {
        this.expression = '0';
        this.previousEquation = '';
        this.isEvaluated = false;
        this.expressionPreview.textContent = '';
        this.liveEvalPreview.textContent = '';
        this.updateDisplay();
    }

    backspace() {
        if (this.isEvaluated) {
            this.clearAll();
            return;
        }

        let expr = this.expression.trimEnd();

        // Check for multi-char function tags like "sin(", "cos(", "asin(", etc.
        const fnMatch = expr.match(/(asin\(|acos\(|atan\(|sin\(|cos\(|tan\(|log\(|ln\(|exp\(|sqrt\(|cbrt\(|abs\(|mod )$/);
        if (fnMatch) {
            expr = expr.slice(0, -fnMatch[0].length);
        } else if (expr.length > 1) {
            expr = expr.slice(0, -1).trimEnd();
        } else {
            expr = '0';
        }

        this.expression = expr || '0';
        this.updateLivePreview();
    }

    // --- Backend Evaluation via Python Engine ---
    async calculateResult() {
        const fullExpr = this.expression.trim();
        if (!fullExpr || fullExpr === '0') return;

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    expression: fullExpr,
                    angle_mode: this.angleMode
                })
            });

            const data = await response.json();

            if (data.success) {
                this.previousEquation = `${fullExpr} =`;
                this.expressionPreview.textContent = this.previousEquation;
                this.expression = String(data.result);
                this.isEvaluated = true;
                this.liveEvalPreview.textContent = `Ans = ${data.result}`;
                this.fetchHistory();
            } else {
                this.showToast(data.error || 'Evaluation Error');
            }
        } catch (err) {
            this.showToast('Backend Connection Error');
        }

        this.updateDisplay();
    }

    // Live preview evaluation in the background
    async updateLivePreview() {
        const expr = this.expression.trim();
        // Only run live preview if expression has operators or functions and doesn't end with an operator
        if (!/[\+\-×÷\^%!]|sin|cos|tan|log|ln|sqrt/.test(expr) || /[\+\-×÷\^%]$/.test(expr)) {
            this.liveEvalPreview.textContent = '';
            return;
        }

        try {
            const res = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ expression: expr, angle_mode: this.angleMode })
            });
            const data = await res.json();
            if (data.success && !this.isEvaluated) {
                this.liveEvalPreview.textContent = `= ${data.result}`;
            } else {
                this.liveEvalPreview.textContent = '';
            }
        } catch (e) {
            this.liveEvalPreview.textContent = '';
        }
    }

    // --- History Log Management ---
    async fetchHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            if (data.success && data.history) {
                this.renderHistory(data.history);
            }
        } catch (err) {
            console.error('Failed to load history', err);
        }
    }

    renderHistory(history) {
        if (!this.historyList) return;

        if (history.length === 0) {
            this.historyList.innerHTML = `
                <div class="empty-history-message">
                    <span>No calculations yet</span>
                    <small>Your math will be saved here</small>
                </div>
            `;
            return;
        }

        this.historyList.innerHTML = '';
        history.forEach(item => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.innerHTML = `
                <span class="history-item-expr">${this.escapeHTML(item.expression)} =</span>
                <span class="history-item-result">${this.escapeHTML(String(item.result))}</span>
            `;
            div.addEventListener('click', () => {
                this.expression = String(item.result);
                this.previousEquation = `${item.expression} =`;
                this.expressionPreview.textContent = this.previousEquation;
                this.isEvaluated = true;
                this.updateDisplay();
                this.showToast(`Loaded ${item.result}`);
                if (window.innerWidth <= 820) {
                    this.historyPanel.classList.remove('mobile-open');
                }
            });
            this.historyList.appendChild(div);
        });
    }

    async clearHistory() {
        try {
            const res = await fetch('/api/clear-history', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                this.renderHistory([]);
                this.showToast('History Cleared');
            }
        } catch (e) {
            this.showToast('Failed to clear history');
        }
    }

    // --- Display & Scaling ---
    updateDisplay() {
        // Show the entire contiguous equation in the main display on the SAME LINE!
        this.mainDisplay.textContent = this.expression || '0';
        if (this.previousEquation && this.isEvaluated) {
            this.expressionPreview.textContent = this.previousEquation;
        } else if (!this.isEvaluated) {
            this.expressionPreview.textContent = '';
        }

        // Dynamically scale font so calculation stays comfortably on one line
        const len = this.mainDisplay.textContent.length;
        if (len > 24) {
            this.mainDisplay.style.fontSize = '1.35rem';
        } else if (len > 18) {
            this.mainDisplay.style.fontSize = '1.65rem';
        } else if (len > 12) {
            this.mainDisplay.style.fontSize = '2.1rem';
        } else {
            this.mainDisplay.style.fontSize = '2.75rem';
        }

        // Auto-scroll to end so user always sees latest typing
        this.mainDisplay.scrollLeft = this.mainDisplay.scrollWidth;
    }

    updateMemoryDisplay() {
        if (this.memory !== 0) {
            this.memIndicator.classList.remove('inactive');
            this.memIndicator.classList.add('active');
            this.memIndicator.textContent = `M: ${this.memory}`;
        } else {
            this.memIndicator.classList.add('inactive');
            this.memIndicator.classList.remove('active');
            this.memIndicator.textContent = 'M: 0';
        }
    }

    async copyToClipboard() {
        const text = this.mainDisplay.textContent;
        try {
            await navigator.clipboard.writeText(text);
            this.showToast(`Copied ${text} to clipboard!`);
        } catch (e) {
            this.showToast('Copy failed');
        }
    }

    showToast(message) {
        if (!this.toast) return;
        this.toast.textContent = message;
        this.toast.classList.add('show');
        clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
            this.toast.classList.remove('show');
        }, 2200);
    }

    escapeHTML(str) {
        return str.replace(/[&<>'"]/g, tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag));
    }

    // --- Global Keyboard Support ---
    handleKeyboardInput(e) {
        if (['/', '*', '+', '-', '=', 'Enter'].includes(e.key)) {
            e.preventDefault();
        }

        let buttonToHighlight = null;

        if (e.key >= '0' && e.key <= '9') {
            this.inputDigit(e.key);
            buttonToHighlight = document.getElementById(`btn-${e.key}`);
        } else if (e.key === '.') {
            this.inputDecimal();
            buttonToHighlight = document.getElementById('btn-decimal');
        } else if (e.key === '+') {
            this.inputOperator('+');
            buttonToHighlight = document.getElementById('btn-add');
        } else if (e.key === '-') {
            this.inputOperator('-');
            buttonToHighlight = document.getElementById('btn-subtract');
        } else if (e.key === '*' || e.key === 'x') {
            this.inputOperator('×');
            buttonToHighlight = document.getElementById('btn-multiply');
        } else if (e.key === '/') {
            this.inputOperator('÷');
            buttonToHighlight = document.getElementById('btn-divide');
        } else if (e.key === '^') {
            this.inputOperator('^');
            buttonToHighlight = document.getElementById('btn-pow');
        } else if (e.key === '%') {
            this.percent();
            buttonToHighlight = document.getElementById('btn-percent');
        } else if (e.key === '!') {
            this.handleScientificFunction('fact');
            buttonToHighlight = document.getElementById('btn-fact');
        } else if (e.key === 's') {
            this.handleScientificFunction('sin');
            buttonToHighlight = document.getElementById('btn-sin');
        } else if (e.key === 'c') {
            this.handleScientificFunction('cos');
            buttonToHighlight = document.getElementById('btn-cos');
        } else if (e.key === 't') {
            this.handleScientificFunction('tan');
            buttonToHighlight = document.getElementById('btn-tan');
        } else if (e.key === 'l') {
            this.handleScientificFunction('ln');
            buttonToHighlight = document.getElementById('btn-ln');
        } else if (e.key === 'Enter' || e.key === '=') {
            this.calculateResult();
            buttonToHighlight = document.getElementById('btn-equals');
        } else if (e.key === 'Backspace') {
            this.backspace();
            buttonToHighlight = document.getElementById('btn-backspace');
        } else if (e.key === 'Escape') {
            this.clearAll();
            buttonToHighlight = document.getElementById('btn-clear');
        } else if (e.key === '(') {
            this.handleScientificFunction('paren-open');
            buttonToHighlight = document.getElementById('btn-paren-open');
        } else if (e.key === ')') {
            this.handleScientificFunction('paren-close');
            buttonToHighlight = document.getElementById('btn-paren-close');
        }

        if (buttonToHighlight) {
            this.playSound(620, 0.025);
            buttonToHighlight.classList.add('keyboard-active');
            setTimeout(() => buttonToHighlight.classList.remove('keyboard-active'), 120);
        }

        this.updateDisplay();
    }
}

// Instantiate on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.shreysCalcApp = new ShreysCalculator();
});
