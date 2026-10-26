/**
 * AAYAM — Ultra-Premium Cyber-Fintech Multi-Page Web Engine
 * Team Credits:
 *   Aditya Singh (FinTech)
 *   Abhishek Shrivastava (Cyber Security)
 *   Aarushi S. (AI/ML)
 *   Ansh Saini (UI/UX)
 *
 * Implements:
 * 1. 4-Pillar Threat Matrix Heuristic Security Screener (Custom text + drag-and-drop file)
 * 2. Client-Side Resilient Engine (Automatic fallback for Vercel / offline / static hosting)
 * 3. Interactive Economic Digital Twin (Cash surplus, DTI, Runway, Resilience score)
 * 4. ArthSim Macroeconomic Shock Trajectory Simulator (Dynamic SVG curves)
 * 5. Opportunity & Mudra Pathway Directory
 * 6. Interactive Recovery Centre & Golden Hour Countdown
 * 7. Settings Drawer (Themes, Currency, Motion) & Quick Jump Palette (Ctrl+K)
 */

// ── 0. Preset Scam Samples Library ──
const SAMPLES = {
    digital_arrest: "CBI POLICE HQ: A parcel under your Aadhaar containing narcotics has been intercepted at Mumbai Customs. A Non-Bailable Arrest Warrant has been issued. Join Skype video call immediately for Digital Arrest verification or police will arrive at your address within 2 hours.",
    electricity: "URGENT NOTICE: Your electricity connection will be disconnected tonight at 9:30 PM because your previous month's bill was not updated. Immediately contact our Power Officer at 9876543210 or install BijliUpdate.apk to update now.",
    upi_reverse: "DEAR CUSTOMER: You have won a cash cashback of ₹5,000 from PhonePe Reward. Scan this reverse QR code in your UPI app and enter your UPI PIN to claim money instantly into your bank account.",
    wfh_task: "CONGRATULATIONS: You have been selected for Part-Time YouTube Video Liking Job. Earn ₹2,500 to ₹8,000 daily. Just like 3 videos, join our Telegram group @EarnDailyFast and pay ₹1,000 security deposit for VIP task assignment.",
    safe_banking: "Dear SBI Customer, your account XX1204 has been credited by Rs 35,000.00 on 24-Oct-25 via UPI Ref 429812908712. Available Balance: Rs 58,420.50. SBI never asks for OTP or PIN.",
    train_ticket: "IRCTC: PNR 2849102841, Train 12952 NDLS-MMCT Tejas Rajdhani. Confirmed Berth B3-42 (MB). Charting done. Wish you a happy journey."
};

// ── 1. Settings & Theme Persistence ──
function initSettings() {
    const savedTheme = localStorage.getItem('aayam_theme') || 'cyber-violet';
    setTheme(savedTheme);

    const savedCurrency = localStorage.getItem('aayam_currency') || 'INR';
    window.currentCurrency = savedCurrency;

    // Apply currency symbols
    document.querySelectorAll('.currency-sym').forEach(el => {
        el.innerText = savedCurrency === 'INR' ? '₹' : '$';
    });
}

function setTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('aayam_theme', theme);
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-theme') === theme);
    });
}

function toggleSettings() {
    const drawer = document.getElementById('settingsDrawer');
    if (drawer) {
        drawer.classList.toggle('active');
    }
}

function toggleCurrency(curr) {
    window.currentCurrency = curr;
    localStorage.setItem('aayam_currency', curr);
    document.querySelectorAll('.currency-sym').forEach(el => {
        el.innerText = curr === 'INR' ? '₹' : '$';
    });
    // Trigger twin refresh if present
    if (typeof calculateTwin === 'function') calculateTwin();
    if (typeof suiteUpdateTwin === 'function') suiteUpdateTwin();
}

// ── 2. Interactive Cursor Glow ──
document.addEventListener('mousemove', (e) => {
    const glow = document.getElementById('cursorGlow');
    if (glow) {
        glow.style.left = `${e.clientX}px`;
        glow.style.top = `${e.clientY}px`;
    }
});

// ── 3. Quick Jump Palette (Ctrl+K or Command+K) ──
window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        toggleQuickJump();
    }
    if (e.key === 'Escape') {
        closeAllModals();
    }
});

function toggleQuickJump() {
    const modal = document.getElementById('quickJumpModal');
    if (modal) {
        const isActive = modal.classList.toggle('active');
        if (isActive) {
            const input = document.getElementById('quickJumpInput');
            if (input) {
                input.value = '';
                input.focus();
                filterQuickJump('');
            }
        }
    }
}

function filterQuickJump(query) {
    const q = (query || '').toLowerCase();
    document.querySelectorAll('.quick-jump-item').forEach(item => {
        const text = item.innerText.toLowerCase();
        item.style.display = text.includes(q) ? 'flex' : 'none';
    });
}

// ── 4. Generic Modal Handlers ──
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

function closeAllModals() {
    document.querySelectorAll('.modal-overlay.active, .quick-jump-modal.active').forEach(m => {
        m.classList.remove('active');
    });
    const drawer = document.getElementById('settingsDrawer');
    if (drawer) drawer.classList.remove('active');
    document.body.style.overflow = 'auto';
}

function scrollToSection(sectionId) {
    const el = document.getElementById(sectionId);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
}

// ── 5. CLIENT-SIDE RESILIENT ENGINES (Vercel & Offline Fallback) ──

/**
 * Robust Client-Side Cyber Risk Screener & 4-Pillar Threat Matrix
 */
function clientSideAssessCyber(text) {
    const raw = (text || '').trim();
    const t = raw.toLowerCase();

    const triggered = [];
    const guidance = [];

    // 1. Digital Arrest / Authority Impersonation
    if (/digital\s*arrest|cbi\s*police|mumbai\s*customs|trai\s*deactivat|skype\s*video|arrest\s*warrant|narcotics\s*department/i.test(raw)) {
        triggered.push({
            code: "DIGITAL_ARREST_IMPERSONATION",
            category: "Digital Arrest / Law Enforcement Impersonation",
            severity: 45,
            explanation: "Indian law enforcement and CBI NEVER conduct arrests, court proceedings, or asset freezing via Skype, WhatsApp, or video calls."
        });
        guidance.push("Disconnect immediately. Government agencies never place citizens under 'Digital Arrest' online.");
    }

    // 2. Urgent Disconnection / Utility Extortion
    if (/electricity\s*(will\s*be\s*)?disconnect|bijli\s*bill|power\s*officer|tonight\s*at\s*9|service\s*blocked/i.test(raw)) {
        triggered.push({
            code: "URGENT_DISCONNECTION_THREAT",
            category: "Utility Bill Disconnection Extortion",
            severity: 35,
            explanation: "DISCOM power utilities never threaten same-night disconnection via private mobile numbers or WhatsApp."
        });
        guidance.push("Check bill status solely on the official DISCOM portal or electricity board application.");
    }

    // 3. Reverse UPI QR / Cashback Trap
    if (/scan\s*(this\s*)?(reverse\s*)?qr|enter\s*(your\s*)?upi\s*pin\s*to\s*receive|cashback\s*of\s*₹|lottery\s*won/i.test(raw)) {
        triggered.push({
            code: "REVERSE_UPI_QR_SCAM",
            category: "Reverse UPI QR / Credential Trap",
            severity: 40,
            explanation: "You NEVER need to enter a UPI PIN or scan a QR code to RECEIVE money. Entering PIN always debits your account."
        });
        guidance.push("NEVER enter your UPI PIN to claim money or cashbacks. PIN is only for debiting funds.");
    }

    // 4. Task-based Work From Home
    if (/part[\s-]*time\s*job|youtube\s*video\s*lik|earn\s*₹?\s*[2-9][0-9]{3}\s*daily|telegram\s*group|vip\s*task/i.test(raw)) {
        triggered.push({
            code: "TASK_BASED_WORK_FROM_HOME_SCAM",
            category: "Task-Based Work-From-Home Scam",
            severity: 35,
            explanation: "Prepaid task scams request initial deposits to unlock fictitious payouts, resulting in total loss."
        });
        guidance.push("Legitimate employers never ask candidates to deposit money or complete paid Telegram tasks.");
    }

    // 5. Malicious APK delivery
    if (/\.apk|install\s*.*\.apk|download\s*our\s*app\s*from\s*(http|bit\.ly)/i.test(raw)) {
        triggered.push({
            code: "MALICIOUS_APK_DELIVERY",
            category: "Malicious APK Delivery",
            severity: 45,
            explanation: "Sideloading unverified APKs bypasses Google Play Protect and gives attackers complete SMS and device control."
        });
        guidance.push("Never install Android APK files received via SMS, WhatsApp, or third-party links.");
    }

    // 6. Remote Screen Sharing Tools
    if (/anydesk|teamviewer|rustdesk|quicksupport/i.test(raw)) {
        triggered.push({
            code: "REMOTE_ACCESS_TOOL_PROMPT",
            category: "Remote Access Screen-Sharing RAT",
            severity: 40,
            explanation: "Fraudsters use remote desktop applications to capture bank credentials, OTPs, and screen gestures."
        });
        guidance.push("Never install AnyDesk or screen-sharing tools on instructions from unknown callers.");
    }

    // 7. Credential / OTP Harvesting
    if (/\botp\b|one[\s-]*time[\s-]*password|cvv|netbanking\s*password|login\s*credentials/i.test(raw) && !/never\s*share/i.test(raw)) {
        triggered.push({
            code: "CREDENTIAL_OTP_HARVESTING",
            category: "OTP & Credential Harvesting",
            severity: 35,
            explanation: "Attempts to solicit 4/6-digit verification codes under pretext of KYC or account maintenance."
        });
        guidance.push("Never disclose SMS OTPs or banking passwords under any circumstances.");
    }

    // Check for legitimate banking notification
    const isBenign = /credited|debited|available balance|otp for logging|bank never asks|txn successful|happy journey|confirmed berth/i.test(raw) && triggered.length === 0;

    // Calculate Scores
    let rawScore = triggered.reduce((acc, curr) => acc + curr.severity, 0);
    let riskScore = Math.min(100, Math.max(0, rawScore));
    if (isBenign) riskScore = 0;

    // 4-Pillar Threat Matrix
    const urgencyScore = Math.min(100, triggered.filter(t => t.code === "URGENT_DISCONNECTION_THREAT").length * 85);
    const financialScore = Math.min(100, triggered.filter(t => ["REVERSE_UPI_QR_SCAM", "TASK_BASED_WORK_FROM_HOME_SCAM"].includes(t.code)).length * 90);
    const authorityScore = Math.min(100, triggered.filter(t => t.code === "DIGITAL_ARREST_IMPERSONATION").length * 95);
    const payloadScore = Math.min(100, triggered.filter(t => ["MALICIOUS_APK_DELIVERY", "REMOTE_ACCESS_TOOL_PROMPT", "CREDENTIAL_OTP_HARVESTING"].includes(t.code)).length * 90);

    let verdict = "SAFE_BENIGN";
    let verdictTitle = "VERIFIED SAFE / BENIGN NOTIFICATION";
    let verdictBadge = "emerald";
    let primaryThreat = isBenign ? "Legitimate Official Notification" : "No Threat Detected";
    let summaryExplanation = "No known attack patterns, extortion triggers, or malicious payloads were detected in this communication.";

    if (riskScore >= 60) {
        verdict = "CRITICAL_THREAT";
        verdictTitle = "CRITICAL THREAT / DANGEROUS SCAM";
        verdictBadge = "rose";
        primaryThreat = triggered[0] ? triggered[0].category : "Severe Cyber Fraud Attack";
        summaryExplanation = `Critical fraud signals detected (${primaryThreat}). High risk of immediate financial extortion.`;
    } else if (riskScore >= 35) {
        verdict = "HIGH_SUSPICION";
        verdictTitle = "HIGH SUSPICION / LIKELY SCAM";
        verdictBadge = "amber";
        primaryThreat = triggered[0] ? triggered[0].category : "Deceptive Phishing Attempt";
        summaryExplanation = `Multiple red flags identified (${primaryThreat}). Strong probability of fraudulent exploitation.`;
    } else if (riskScore > 0) {
        verdict = "MODERATE_CAUTION";
        verdictTitle = "MODERATE CAUTION / UNVERIFIED";
        verdictBadge = "amber";
        primaryThreat = "Unverified Communication";
        summaryExplanation = "Contains artificial urgency or unverified links. Independent verification advised.";
    }

    const triggeredFlags = triggered.map(t => `${t.category}: ${t.explanation}`);
    const recommendedAction = guidance[0] || "Standard cyber hygiene: Verify sender independently via official website or helpline.";

    return {
        risk_score: riskScore,
        risk_level: riskScore >= 60 ? "CRITICAL" : (riskScore >= 35 ? "HIGH" : (riskScore > 0 ? "MODERATE" : "SAFE")),
        verdict: verdict,
        verdict_title: verdictTitle,
        verdict_badge: verdictBadge,
        risk_badge: verdictBadge,
        primary_threat_vector: primaryThreat,
        summary_explanation: summaryExplanation,
        triggered_flags: triggeredFlags,
        recommended_action: recommendedAction,
        threat_matrix: {
            urgency_coercion: urgencyScore,
            financial_trigger: financialScore,
            authority_impersonation: authorityScore,
            technical_payload: payloadScore
        }
    };
}

/**
 * Robust Client-Side Economic Twin Calculator
 */
function clientSideCalculateEconomy(p) {
    const inc = (Number(p.monthly_take_home_income) || 0) + (Number(p.other_monthly_income) || 0);
    const essential = Number(p.essential_monthly_expenses) || 0;
    const disc = Number(p.discretionary_expenses) || 0;
    const totalExp = essential + disc;
    const savings = Number(p.current_savings) || 0;
    const debt = Number(p.outstanding_debt) || 0;
    const debtRepay = Number(p.monthly_debt_repayments) || 0;

    const surplus = inc - totalExp - debtRepay;
    const savingsRate = inc > 0 ? Math.max(0, (surplus / inc) * 100) : 0;
    const runwayMonths = essential > 0 ? savings / essential : (savings > 0 ? 12 : 0);
    const dtiRatio = inc > 0 ? (debtRepay / inc) * 100 : 0;

    // Composite Resilience Score (0–100)
    let score = 50.0;
    if (runwayMonths >= 6) score += 20;
    else if (runwayMonths >= 3) score += 10;
    else score -= 15;

    if (dtiRatio <= 20) score += 15;
    else if (dtiRatio <= 40) score += 5;
    else score -= 20;

    if (savingsRate >= 20) score += 15;
    else if (savingsRate >= 10) score += 5;
    else score -= 10;

    score = Math.min(100, Math.max(10, Math.round(score)));

    let category = "Vulnerable";
    let badge = "rose";
    if (score >= 75) { category = "Resilient & Stable"; badge = "emerald"; }
    else if (score >= 50) { category = "Moderate Stability"; badge = "amber"; }

    return {
        resilience_score: score,
        resilience_category: category,
        resilience_badge: badge,
        net_monthly_surplus_inr: surplus,
        emergency_runway_months: Number(runwayMonths.toFixed(1)),
        dti_ratio_pct: Number(dtiRatio.toFixed(1)),
        savings_rate_pct: Number(savingsRate.toFixed(1)),
        total_monthly_expenses_inr: totalExp
    };
}

/**
 * Robust Client-Side Shock Trajectory Simulator
 */
function clientSideSimulateScenario(profile, scenarioName, horizonMonths) {
    const inc = Number(profile.monthly_take_home_income) || 35000;
    const essential = Number(profile.essential_monthly_expenses) || 20000;
    const disc = Number(profile.discretionary_expenses) || 6000;
    let savings = Number(profile.current_savings) || 50000;

    let incomeDropPct = 0;
    let lumpLoss = 0;
    let expenseSurgePct = 0;

    if (scenarioName === 'job_loss') {
        incomeDropPct = 100;
    } else if (scenarioName === 'cyber_fraud_loss') {
        lumpLoss = 50000;
    } else if (scenarioName === 'medical_emergency') {
        lumpLoss = 75000;
    } else if (scenarioName === 'inflation_spike') {
        expenseSurgePct = 20;
    } else if (scenarioName === 'dual_shock') {
        lumpLoss = 50000;
        expenseSurgePct = 15;
    }

    savings = Math.max(0, savings - lumpLoss);

    const trajectory = [];
    let depleted = false;
    let depletionMonth = null;

    for (let m = 1; m <= horizonMonths; m++) {
        const curIncome = m <= 4 ? inc * (1 - incomeDropPct / 100) : inc;
        const curExp = (essential * (1 + expenseSurgePct / 100)) + (incomeDropPct > 0 ? disc * 0.4 : disc);
        const monthlyBalance = curIncome - curExp;

        savings += monthlyBalance;
        if (savings <= 0 && !depleted) {
            depleted = true;
            depletionMonth = m;
            savings = 0;
        }

        trajectory.push({
            month: m,
            savings_end: Math.max(0, Math.round(savings)),
            income: Math.round(curIncome),
            expenses: Math.round(curExp)
        });
    }

    return {
        initial_savings: Number(profile.current_savings) || 50000,
        depleted: depleted,
        depletion_month: depletionMonth,
        trajectory: trajectory,
        actionable_guidance: depleted
            ? `Critical: Liquid buffer depletes at Month ${depletionMonth}. Immediate discretionary cost reduction and emergency buffer reinforcement required.`
            : `Resilient: Household maintains emergency solvency across the full ${horizonMonths}-month stress horizon.`
    };
}

// ── 6. DEDICATED CYBERDRISHTI THREAT SCREENING STATION ──

function setCyberSample(key) {
    if (SAMPLES[key]) {
        const input = document.getElementById('cyber_input_text');
        if (input) {
            input.value = SAMPLES[key];
            updateCharCount();
            screenCyberMessage();
        }
    }
}

function clearCyberInput() {
    const input = document.getElementById('cyber_input_text');
    if (input) {
        input.value = '';
        updateCharCount();
    }
    const container = document.getElementById('cyber_result_container');
    if (container) container.style.display = 'none';
}

function updateCharCount() {
    const input = document.getElementById('cyber_input_text');
    const lbl = document.getElementById('charCount');
    if (input && lbl) {
        lbl.innerText = `${input.value.length} characters`;
    }
}

async function screenCyberMessage() {
    const textEl = document.getElementById('cyber_input_text');
    const text = textEl ? textEl.value.trim() : '';
    if (!text) {
        alert('Please paste, type, or drag-and-drop a message to analyze.');
        return;
    }

    let result = null;

    // Attempt backend API, fall back seamlessly to client engine if static/offline
    try {
        const res = await fetch('/api/cyber/assess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                result = data.result;
            }
        }
    } catch (err) {
        console.warn('Backend API unavailable. Using resilient client-side security engine:', err);
    }

    if (!result) {
        result = clientSideAssessCyber(text);
    }

    renderCyberDrishtiResult(result);
}

function renderCyberDrishtiResult(r) {
    const container = document.getElementById('cyber_result_container');
    if (!container) return;
    container.style.display = 'block';

    const matrix = r.threat_matrix || {
        urgency_coercion: 0,
        financial_trigger: 0,
        authority_impersonation: 0,
        technical_payload: 0
    };

    const flagsHtml = (r.triggered_flags && r.triggered_flags.length)
        ? r.triggered_flags.map(f => `<li style="margin-bottom: 6px;">⚠️ <strong>${f}</strong></li>`).join('')
        : '<li style="color: #34D399;">✅ No heuristic threat signatures or coercive triggers detected.</li>';

    container.innerHTML = `
        <!-- Main Verdict Banner -->
        <div style="background: rgba(18, 14, 34, 0.9); border: 1px solid var(--border-card); border-radius: 16px; padding: 24px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: gap; margin-bottom: 14px;">
                <div>
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #94A3B8;">ASSESSMENT VERDICT</span>
                    <h3 style="font-family: var(--font-heading); font-size: 1.45rem; color: #FFFFFF; margin: 4px 0;">${r.primary_threat_vector}</h3>
                </div>
                <div style="text-align: right;">
                    <span class="score-category badge-${r.risk_badge || 'emerald'}" style="font-size: 0.88rem; padding: 6px 14px;">
                        ${r.risk_level} THREAT (${r.risk_score} / 100)
                    </span>
                </div>
            </div>

            <p style="font-size: 0.95rem; color: #E2E8F0; line-height: 1.6; margin-bottom: 18px;">
                ${r.summary_explanation}
            </p>

            <!-- 4-Pillar Threat Matrix -->
            <div style="margin-top: 20px;">
                <div style="font-size: 0.76rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--accent-violet); margin-bottom: 12px;">
                    4-PILLAR EXPLAINABLE THREAT MATRIX
                </div>
                <div class="threat-matrix-grid">
                    <div class="matrix-pillar-card">
                        <div class="pillar-top">
                            <span class="pillar-name">1. Urgency &amp; Fear</span>
                            <span class="pillar-score" style="color: ${matrix.urgency_coercion > 50 ? '#FB7185' : '#34D399'};">${matrix.urgency_coercion}%</span>
                        </div>
                        <div class="pillar-bar-bg">
                            <div class="pillar-bar-fill" style="width: ${matrix.urgency_coercion}%; background: ${matrix.urgency_coercion > 50 ? '#FB7185' : '#34D399'};"></div>
                        </div>
                        <span class="pillar-desc">Same-day disconnection, arrest threats, countdown timers</span>
                    </div>

                    <div class="matrix-pillar-card">
                        <div class="pillar-top">
                            <span class="pillar-name">2. Financial Trap</span>
                            <span class="pillar-score" style="color: ${matrix.financial_trigger > 50 ? '#FB7185' : '#34D399'};">${matrix.financial_trigger}%</span>
                        </div>
                        <div class="pillar-bar-bg">
                            <div class="pillar-bar-fill" style="width: ${matrix.financial_trigger}%; background: ${matrix.financial_trigger > 50 ? '#FB7185' : '#34D399'};"></div>
                        </div>
                        <span class="pillar-desc">Reverse UPI QR, lottery cashbacks, paid task deposits</span>
                    </div>

                    <div class="matrix-pillar-card">
                        <div class="pillar-top">
                            <span class="pillar-name">3. Authority Spoof</span>
                            <span class="pillar-score" style="color: ${matrix.authority_impersonation > 50 ? '#FB7185' : '#34D399'};">${matrix.authority_impersonation}%</span>
                        </div>
                        <div class="pillar-bar-bg">
                            <div class="pillar-bar-fill" style="width: ${matrix.authority_impersonation}%; background: ${matrix.authority_impersonation > 50 ? '#FB7185' : '#34D399'};"></div>
                        </div>
                        <span class="pillar-desc">CBI, Mumbai Police, TRAI, Telecom Department, Court</span>
                    </div>

                    <div class="matrix-pillar-card">
                        <div class="pillar-top">
                            <span class="pillar-name">4. Technical Payload</span>
                            <span class="pillar-score" style="color: ${matrix.technical_payload > 50 ? '#FB7185' : '#34D399'};">${matrix.technical_payload}%</span>
                        </div>
                        <div class="pillar-bar-bg">
                            <div class="pillar-bar-fill" style="width: ${matrix.technical_payload}%; background: ${matrix.technical_payload > 50 ? '#FB7185' : '#34D399'};"></div>
                        </div>
                        <span class="pillar-desc">Malicious APKs, AnyDesk/RAT prompts, OTP harvesting</span>
                    </div>
                </div>
            </div>

            <!-- Identified Red Flags -->
            <div style="margin: 20px 0 16px 0; background: rgba(0, 0, 0, 0.25); border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #F59E0B; text-transform: uppercase; margin-bottom: 8px;">
                    IDENTIFIED ATTACK INDICATORS:
                </div>
                <ul style="padding-left: 20px; font-size: 0.88rem; color: #E2E8F0; line-height: 1.6;">
                    ${flagsHtml}
                </ul>
            </div>

            <!-- Action Guidance & Emergency Quick Jump -->
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px; font-size: 0.9rem; color: #34D399; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <strong>🛡️ Recommended Defense:</strong> ${r.recommended_action}
                </div>
                ${r.risk_score >= 35 ? `
                    <a href="/recovery" class="pill-btn danger-pill" style="text-decoration: none; padding: 6px 16px; font-size: 0.78rem;">
                        <span>GO TO 1930 RECOVERY</span>
                        <span class="pill-icon">🚨</span>
                    </a>
                ` : ''}
            </div>

            <!-- Quick Action Toolbar -->
            <div style="margin-top: 16px; display: flex; gap: 10px; justify-content: flex-end;">
                <button class="pill-btn secondary-pill" onclick="copyThreatReport('${r.risk_level}', '${r.primary_threat_vector}', ${r.risk_score})" style="font-size: 0.78rem; padding: 6px 14px;">
                    <span>Copy Threat Report</span>
                    <span class="pill-icon">📋</span>
                </button>
            </div>
        </div>
    `;

    // Scroll into view gently
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function copyThreatReport(level, threat, score) {
    const text = `AAYAM CYBER THREAT AUDIT REPORT\nStatus: ${level} (${score}/100)\nThreat Vector: ${threat}\nAudit Engine: CyberDrishti Heuristic Matrix\nAction: Do not transfer funds or share credentials. Verify independently via 1930 / cybercrime.gov.in.`;
    navigator.clipboard.writeText(text).then(() => {
        alert('Threat Audit Report copied to clipboard!');
    }).catch(() => {
        alert('Report ready: ' + text);
    });
}

// ── 7. Drag and Drop File Screener Setup ──
function initDropzone() {
    const dropzone = document.getElementById('cyberDropzone');
    const fileInput = document.getElementById('cyberFileInput');
    if (!dropzone) return;

    ['dragenter', 'dragover'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('drag-active');
        });
    });

    ['dragleave', 'drop'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('drag-active');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            handleUploadedFile(files[0]);
        }
    });

    dropzone.addEventListener('click', () => {
        if (fileInput) fileInput.click();
    });

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                handleUploadedFile(e.target.files[0]);
            }
        });
    }
}

function handleUploadedFile(file) {
    const name = file.name;
    const isText = file.type.startsWith('text') || name.endsWith('.txt') || name.endsWith('.eml');

    if (name.toLowerCase().endsWith('.apk')) {
        const fakeMessage = `FILE UPLOADED: ${name} (Android Application Package). Extracted Manifest Package: com.bijli.update.apk. Detected Intent: RECEIVE_SMS, READ_SMS, BIND_ACCESSIBILITY_SERVICE. Remote URL: http://untrusted-c2-server.in/api/rat`;
        const textEl = document.getElementById('cyber_input_text');
        if (textEl) {
            textEl.value = fakeMessage;
            updateCharCount();
            screenCyberMessage();
        }
        return;
    }

    if (isText) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            const textEl = document.getElementById('cyber_input_text');
            if (textEl) {
                textEl.value = content;
                updateCharCount();
                screenCyberMessage();
            }
        };
        reader.readAsText(file);
    } else {
        // Image or document payload mock extraction
        const simulatedText = `Extracted Text from ${name}: Urgent Notice from Electricity Department. Your connection will be disconnected tonight at 9:30 PM. Download the attached bill update app or call 9876543210.`;
        const textEl = document.getElementById('cyber_input_text');
        if (textEl) {
            textEl.value = simulatedText;
            updateCharCount();
            screenCyberMessage();
        }
    }
}

// ── 8. DEDICATED ECONOMIC DIGITAL TWIN ENGINE ──

function setTwinPreset(type) {
    const presets = {
        salaried: { inc: 45000, other: 5000, exp: 24000, disc: 7000, sav: 85000, debt: 50000, repay: 4500 },
        gig: { inc: 22000, other: 3000, exp: 16000, disc: 3000, sav: 15000, debt: 20000, repay: 2000 },
        merchant: { inc: 65000, other: 10000, exp: 35000, disc: 10000, sav: 140000, debt: 150000, repay: 12000 },
        fresh_grad: { inc: 18000, other: 0, exp: 13000, disc: 3000, sav: 8000, debt: 35000, repay: 2500 }
    };

    const p = presets[type];
    if (!p) return;

    if (document.getElementById('twin_income')) document.getElementById('twin_income').value = p.inc;
    if (document.getElementById('twin_other_income')) document.getElementById('twin_other_income').value = p.other;
    if (document.getElementById('twin_expenses')) document.getElementById('twin_expenses').value = p.exp;
    if (document.getElementById('twin_discretionary')) document.getElementById('twin_discretionary').value = p.disc;
    if (document.getElementById('twin_savings')) document.getElementById('twin_savings').value = p.sav;
    if (document.getElementById('twin_debt')) document.getElementById('twin_debt').value = p.debt;
    if (document.getElementById('twin_repayments')) document.getElementById('twin_repayments').value = p.repay;

    calculateTwin();
}

async function calculateTwin() {
    const payload = {
        monthly_take_home_income: parseFloat(document.getElementById('twin_income') ? document.getElementById('twin_income').value : 35000) || 35000,
        other_monthly_income: parseFloat(document.getElementById('twin_other_income') ? document.getElementById('twin_other_income').value : 5000) || 5000,
        essential_monthly_expenses: parseFloat(document.getElementById('twin_expenses') ? document.getElementById('twin_expenses').value : 20000) || 20000,
        discretionary_expenses: parseFloat(document.getElementById('twin_discretionary') ? document.getElementById('twin_discretionary').value : 6000) || 6000,
        current_savings: parseFloat(document.getElementById('twin_savings') ? document.getElementById('twin_savings').value : 50000) || 50000,
        outstanding_debt: parseFloat(document.getElementById('twin_debt') ? document.getElementById('twin_debt').value : 75000) || 75000,
        monthly_debt_repayments: parseFloat(document.getElementById('twin_repayments') ? document.getElementById('twin_repayments').value : 4500) || 4500
    };

    let ind = null;
    try {
        const res = await fetch('/api/economy/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                ind = data.indicators;
            }
        }
    } catch (err) {
        console.warn('Economy API offline, using client calculator');
    }

    if (!ind) {
        ind = clientSideCalculateEconomy(payload);
    }

    renderTwinIndicators(ind);
}

function renderTwinIndicators(ind) {
    const sym = window.currentCurrency === 'USD' ? '$' : '₹';

    if (document.getElementById('kpi_score')) {
        document.getElementById('kpi_score').innerText = ind.resilience_score;
    }
    if (document.getElementById('kpi_score_badge')) {
        const badge = document.getElementById('kpi_score_badge');
        badge.innerText = ind.resilience_category;
        const bColor = ind.resilience_score >= 70 ? 'emerald' : (ind.resilience_score >= 45 ? 'amber' : 'rose');
        badge.className = `score-category badge-${ind.resilience_badge || bColor}`;
    }
    const surplus = ind.net_monthly_surplus_inr ?? ind.monthly_surplus_deficit ?? 0;
    if (document.getElementById('kpi_surplus')) {
        document.getElementById('kpi_surplus').innerText = `${sym}${Math.round(surplus).toLocaleString('en-IN')}`;
    }
    const runway = ind.emergency_runway_months ?? ind.emergency_fund_months ?? 0;
    if (document.getElementById('kpi_runway')) {
        document.getElementById('kpi_runway').innerText = `${runway} Mo`;
    }
    const dti = ind.dti_ratio_pct ?? ind.debt_to_income_ratio_pct ?? 0;
    if (document.getElementById('kpi_dti')) {
        document.getElementById('kpi_dti').innerText = `${dti}%`;
    }
    const savingsRate = ind.savings_rate_pct ?? 0;
    if (document.getElementById('kpi_savings_rate')) {
        document.getElementById('kpi_savings_rate').innerText = `${savingsRate}%`;
    }
}

function exportTwinProfile() {
    const profile = {
        timestamp: new Date().toISOString(),
        monthly_take_home_income: parseFloat(document.getElementById('twin_income')?.value || 35000),
        essential_expenses: parseFloat(document.getElementById('twin_expenses')?.value || 20000),
        savings: parseFloat(document.getElementById('twin_savings')?.value || 50000),
        currency: window.currentCurrency || 'INR'
    };
    const blob = new Blob([JSON.stringify(profile, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AAYAM_Economic_Twin_Profile_${Date.now()}.json`;
    a.click();
}

// ── 9. DEDICATED ARTHSIM SCENARIO SIMULATOR ──

async function runSimulation() {
    const scenario = document.getElementById('arth_scenario') ? document.getElementById('arth_scenario').value : 'job_loss';
    const horizon = parseInt(document.getElementById('arth_horizon') ? document.getElementById('arth_horizon').value : 12) || 12;

    const profile = {
        monthly_take_home_income: parseFloat(document.getElementById('twin_income')?.value || 35000),
        essential_monthly_expenses: parseFloat(document.getElementById('twin_expenses')?.value || 20000),
        discretionary_expenses: parseFloat(document.getElementById('twin_discretionary')?.value || 6000),
        current_savings: parseFloat(document.getElementById('twin_savings')?.value || 50000)
    };

    let sim = null;
    try {
        const res = await fetch('/api/simulator/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ profile, scenario, horizon_months: horizon })
        });
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                sim = data.result;
            }
        }
    } catch (err) {
        console.warn('Simulator API offline, using client simulation');
    }

    if (!sim) {
        sim = clientSideSimulateScenario(profile, scenario, horizon);
    }

    renderSimulationChart(sim.trajectory);

    const kpis = document.getElementById('sim_kpis_container');
    if (kpis) {
        const sym = window.currentCurrency === 'USD' ? '$' : '₹';
        kpis.innerHTML = `
            <div class="kpi-grid-mini" style="margin-top: 16px;">
                <div class="mini-kpi">
                    <span class="kpi-lbl">Starting Savings</span>
                    <span class="kpi-num">${sym}${Math.round(sim.initial_savings).toLocaleString('en-IN')}</span>
                </div>
                <div class="mini-kpi">
                    <span class="kpi-lbl">Survival Status</span>
                    <span class="kpi-num" style="color: ${sim.depleted ? '#FB7185' : '#34D399'};">
                        ${sim.depleted ? `Depletes at Month ${sim.depletion_month}` : 'Survives Full Horizon'}
                    </span>
                </div>
            </div>
            <div style="margin-top: 14px; background: rgba(255,255,255,0.03); border-radius: 8px; padding: 12px 14px; font-size: 0.88rem; color: #CBD5E1;">
                <strong>Strategic Guidance:</strong> ${sim.actionable_guidance}
            </div>
        `;
    }
}

function renderSimulationChart(trajectory) {
    if (!trajectory || !trajectory.length) return;
    const wrapper = document.getElementById('sim_chart_wrapper');
    if (!wrapper) return;

    const width = 760;
    const height = 240;
    const padding = 45;

    const maxVal = Math.max(...trajectory.map(p => p.savings_end), 60000);
    const minVal = 0;

    const points = trajectory.map((p, idx) => {
        const x = padding + (idx / (trajectory.length - 1)) * (width - padding * 2);
        const y = height - padding - ((p.savings_end - minVal) / (maxVal - minVal)) * (height - padding * 2);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');

    const sym = window.currentCurrency === 'USD' ? '$' : '₹';

    wrapper.innerHTML = `
        <svg viewBox="0 0 ${width} ${height}" style="width: 100%; height: 230px; background: rgba(0,0,0,0.35); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
            <defs>
                <linearGradient id="simCurveGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#A855F7" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#A855F7" stop-opacity="0.0"/>
                </linearGradient>
            </defs>
            <!-- Baseline Grid -->
            <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#334155" stroke-width="1"/>
            <line x1="${padding}" y1="${padding}" x2="${width - padding}" y2="${padding}" stroke="#1E293B" stroke-dasharray="4" stroke-width="1"/>

            <!-- Trend Polyline -->
            <polyline fill="none" stroke="#D946EF" stroke-width="3" stroke-linecap="round" points="${points}"/>

            <!-- Node Dots -->
            ${trajectory.map((p, idx) => {
                const x = padding + (idx / (trajectory.length - 1)) * (width - padding * 2);
                const y = height - padding - ((p.savings_end - minVal) / (maxVal - minVal)) * (height - padding * 2);
                return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4.5" fill="#FFFFFF" stroke="#D946EF" stroke-width="2"/>`;
            }).join('')}

            <!-- Axis Labels -->
            <text x="${padding}" y="${height - 12}" fill="#94A3B8" font-size="11">Month 1 (${sym}${trajectory[0].savings_end.toLocaleString('en-IN')})</text>
            <text x="${width - padding - 60}" y="${height - 12}" fill="#94A3B8" font-size="11">Month ${trajectory.length} (${sym}${trajectory[trajectory.length - 1].savings_end.toLocaleString('en-IN')})</text>
        </svg>
    `;
}

// ── 10. RECOVERY CENTRE & GOLDEN HOUR TIMER ──

let goldenCountdown = 7200; // 2 hours = 7200s
let timerInterval = null;

function initGoldenTimer() {
    const display = document.getElementById('goldenTimerDisplay');
    const bar = document.getElementById('goldenTimerBar');
    if (!display) return;

    if (timerInterval) clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if (goldenCountdown > 0) {
            goldenCountdown--;
            const mins = Math.floor(goldenCountdown / 60);
            const secs = goldenCountdown % 60;
            display.innerText = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
            if (bar) {
                const pct = (goldenCountdown / 7200) * 100;
                bar.style.width = `${pct}%`;
            }
        } else {
            display.innerText = "00:00 - Window Expired";
            clearInterval(timerInterval);
        }
    }, 1000);
}

function selectIncidentCategory(cat) {
    document.querySelectorAll('.incident-cat-btn').forEach(b => b.classList.remove('active'));
    if (event && event.currentTarget) event.currentTarget.classList.add('active');

    const protocols = {
        unauthorized_upi: {
            title: "Unauthorized UPI / Payment Gateway Debit",
            step1: "Open your UPI App immediately (GPay / PhonePe / Paytm / BHIM) -> Profile -> Block / Freeze Account or Delink Bank Account.",
            step2: "Call Bank Fraud Hotline: SBI 1800111109 | HDFC 18002026161 | ICICI 18001080 to freeze your account and reverse UPI mandates.",
            step3: "Dial 1930 immediately with UPI UTR Reference Number, beneficiary UPI handle, and transaction timestamp."
        },
        digital_arrest: {
            title: "Digital Arrest & Extortion Coercion",
            step1: "DISCONNECT IMMEDIATELY. Hang up WhatsApp/Skype video calls. Turn on Airplane mode if threatened.",
            step2: "DO NOT TRANSFER ANY 'CLEARANCE' MONEY. Indian courts and CBI do not accept bail bonds via NEFT/UPI.",
            step3: "Dial 1930 and file an extortion report under MHA Digital Arrest guidelines. Keep call recordings & numbers."
        },
        malicious_apk: {
            title: "Installed Suspicious APK / Remote Screen Share App",
            step1: "Turn off Wi-Fi and Mobile Data immediately to sever communication with the attacker's Command & Control server.",
            step2: "Uninstall AnyDesk, TeamViewer, RustDesk, or BijliUpdate.apk from Settings -> Apps.",
            step3: "Log in to your bank portal from a DIFFERENT clean device and change all NetBanking passwords & UPI PINs."
        }
    };

    const p = protocols[cat] || protocols.unauthorized_upi;
    const container = document.getElementById('recovery_protocol_container');
    if (container) {
        container.innerHTML = `
            <div style="background: rgba(18, 14, 34, 0.85); border: 1px solid var(--border-card); border-radius: 16px; padding: 24px;">
                <h4 style="font-family: var(--font-heading); color: #FFFFFF; font-size: 1.2rem; margin-bottom: 14px;">
                    🚨 Immediate Action Protocol: ${p.title}
                </h4>
                <div style="display: flex; flex-direction: column; gap: 14px;">
                    <div style="background: rgba(244, 63, 94, 0.1); border-left: 4px solid #FB7185; padding: 12px 16px; border-radius: 8px;">
                        <strong style="color: #FB7185;">Step 1 (First 5 Mins):</strong>
                        <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #F1F5F9;">${p.step1}</p>
                    </div>
                    <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #F59E0B; padding: 12px 16px; border-radius: 8px;">
                        <strong style="color: #FBBF24;">Step 2 (5-15 Mins):</strong>
                        <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #F1F5F9;">${p.step2}</p>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 8px;">
                        <strong style="color: #34D399;">Step 3 (Within Golden Hour):</strong>
                        <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #F1F5F9;">${p.step3}</p>
                    </div>
                </div>
                <div style="margin-top: 18px; text-align: right;">
                    <a href="https://cybercrime.gov.in" target="_blank" class="pill-btn primary-pill" style="text-decoration: none; display: inline-flex;">
                        <span>Open Official Cybercrime Portal (cybercrime.gov.in) ↗</span>
                    </a>
                </div>
            </div>
        `;
    }
}

// ── 11. INITIAL DOM BOOTSTRAP ──

document.addEventListener('DOMContentLoaded', () => {
    initSettings();
    initDropzone();
    initGoldenTimer();

    // Initialize module-specific components if elements are present on the current page
    if (document.getElementById('twin_income')) calculateTwin();
    if (document.getElementById('arth_scenario')) runSimulation();

    // Landing page interactive suite updates
    if (typeof suiteUpdateTwin === 'function' && document.getElementById('slide_income')) {
        suiteUpdateTwin();
    }
});
