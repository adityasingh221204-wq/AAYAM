/**
 * AAYAM - Interactive Web Application Logic
 * Pure Vanilla JavaScript connecting UI to REST API engines
 */

// ── Modal System ──
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

// Close modal when clicking on overlay background or pressing Escape
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => {
            m.classList.remove('active');
        });
        document.body.style.overflow = 'auto';
    }
});

function scrollToSection(sectionId) {
    const el = document.getElementById(sectionId);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
    }
}

// ── Tab Switching ──
function switchGuideTab(evt, tabId) {
    document.querySelectorAll('#guideModal .modal-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('#guideModal .guide-tab-content').forEach(c => c.classList.remove('active'));
    evt.currentTarget.classList.add('active');
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
}

function switchIntelTab(evt, tabId) {
    document.querySelectorAll('#intelModal .modal-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('#intelModal .intel-tab-content').forEach(c => c.classList.remove('active'));
    evt.currentTarget.classList.add('active');
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
}

// ── 1. Economic Digital Twin Calculator ──
async function calculateTwin() {
    const income = parseFloat(document.getElementById('twin_income').value) || 0;
    const essential = parseFloat(document.getElementById('twin_essential').value) || 0;
    const discretionary = parseFloat(document.getElementById('twin_discretionary').value) || 0;
    const savings = parseFloat(document.getElementById('twin_savings').value) || 0;
    const emi = parseFloat(document.getElementById('twin_emi').value) || 0;

    const payload = {
        monthly_take_home_income: income,
        other_monthly_income: 0,
        essential_monthly_expenses: essential,
        discretionary_expenses: discretionary,
        current_savings: savings,
        outstanding_debt: emi * 12,
        monthly_debt_repayments: emi,
        emergency_expenses_obligations: 0
    };

    try {
        const res = await fetch('/api/economy/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === 'success') {
            const ind = data.indicators;
            document.getElementById('twin_res_score').innerText = `${ind.resilience_score} / 100`;
            const badge = document.getElementById('twin_res_badge');
            badge.innerText = ind.resilience_category;
            badge.className = `score-category badge-${ind.resilience_score >= 70 ? 'emerald' : ind.resilience_score >= 50 ? 'indigo' : ind.resilience_score >= 30 ? 'amber' : 'rose'}`;

            document.getElementById('twin_runway').innerText = `${ind.emergency_fund_months.toFixed(1)} Months`;
            document.getElementById('twin_savings_rate').innerText = `${ind.savings_rate_pct.toFixed(1)}%`;
            document.getElementById('twin_dti').innerText = `${ind.debt_to_income_ratio_pct.toFixed(1)}%`;
            document.getElementById('twin_surplus').innerText = `₹${Math.round(ind.monthly_surplus_deficit).toLocaleString('en-IN')}`;
        }
    } catch (err) {
        console.error('Twin API calculation error:', err);
    }
}

// ── 2. CyberDrishti Message Scanner ──
const SAMPLES = {
    electricity: "Dear consumer your electricity power will be disconnected tonight at 9:30 pm from bijli vibhag because previous month bill was not updated. Please immediately install update apk from link http://bit.ly/bijli-apk to avoid power cut.",
    upi: "Sir I am buying your sofa on OLX. I have sent QR code. Please scan QR code and enter your 6-digit UPI PIN to receive ₹15,000 in your bank account immediately.",
    digital_arrest: "This is CBI Officer Sharma calling via Skype video call. A narcotics parcel addressed in your name was intercepted by Customs. You are placed under digital arrest until you transfer funds to court verification account.",
    fastag: "URGENT FASTag Notice: Your FASTag wallet is blacklisted due to incomplete KYC. Click fastag-kyc-update.com to pay verification fee of Rs 10 and restore service immediately."
};

function loadCyberSample(key) {
    if (SAMPLES[key]) {
        document.getElementById('cyber_input_text').value = SAMPLES[key];
    }
}

async function screenCyberMessage() {
    const text = document.getElementById('cyber_input_text').value.trim();
    if (!text) {
        alert('Please enter or select a sample message to screen.');
        return;
    }

    try {
        const res = await fetch('/api/cyber/assess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (data.status === 'success') {
            const r = data.result;
            const container = document.getElementById('cyber_result_container');
            container.style.display = 'block';

            let flagsHtml = r.triggered_flags.map(f => `<li>⚠️ <strong>${f}</strong></li>`).join('');

            container.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <span style="font-size: 0.78rem; text-transform: uppercase; color: #94A3B8;">ASSESSMENT RESULT</span>
                        <h3 style="margin: 0; color: #FFFFFF;">${r.primary_threat_vector}</h3>
                    </div>
                    <div style="text-align: right;">
                        <span class="score-category badge-${r.risk_badge}">${r.risk_level} (${r.risk_score} / 100)</span>
                    </div>
                </div>
                <div style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 12px;">${r.summary_explanation}</div>
                <div style="margin-bottom: 14px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #F59E0B; margin-bottom: 6px;">IDENTIFIED THREAT SIGNALS:</div>
                    <ul style="padding-left: 20px; font-size: 0.85rem; color: #E2E8F0; line-height: 1.6;">${flagsHtml || '<li>No obvious threat triggers identified.</li>'}</ul>
                </div>
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 12px 16px; font-size: 0.85rem; color: #34D399;">
                    <strong>🛡️ Recommended Defense:</strong> ${r.recommended_action}
                </div>
            `;
        }
    } catch (err) {
        console.error('CyberDrishti assessment error:', err);
    }
}

// ── 3. ArthSim Financial Simulator ──
async function runSimulation() {
    const scenario = document.getElementById('arth_scenario').value;
    const horizon = parseInt(document.getElementById('arth_horizon').value) || 12;

    try {
        const res = await fetch('/api/simulator/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario, horizon_months: horizon })
        });
        const data = await res.json();
        if (data.status === 'success') {
            const sim = data.result;
            renderSimulationChart(sim.trajectory);

            document.getElementById('sim_kpis_container').innerHTML = `
                <div class="kpi-grid-mini" style="margin-top: 16px;">
                    <div class="mini-kpi">
                        <span class="kpi-lbl">Starting Savings</span>
                        <span class="kpi-num">₹${Math.round(sim.initial_savings).toLocaleString('en-IN')}</span>
                    </div>
                    <div class="mini-kpi">
                        <span class="kpi-lbl">Depletion Status</span>
                        <span class="kpi-num" style="color: ${sim.depleted ? '#FB7185' : '#34D399'};">
                            ${sim.depleted ? `Depleted at Month ${sim.depletion_month}` : 'Survives Horizon'}
                        </span>
                    </div>
                </div>
                <div style="margin-top: 12px; font-size: 0.86rem; color: #94A3B8;">
                    <strong>Simulation Note:</strong> ${sim.actionable_guidance}
                </div>
            `;
        }
    } catch (err) {
        console.error('Simulation error:', err);
    }
}

function renderSimulationChart(trajectory) {
    if (!trajectory || !trajectory.length) return;
    const wrapper = document.getElementById('sim_chart_wrapper');
    const width = 760;
    const height = 240;
    const padding = 40;

    const maxVal = Math.max(...trajectory.map(p => p.savings_end), 60000);
    const minVal = 0;

    const points = trajectory.map((p, idx) => {
        const x = padding + (idx / (trajectory.length - 1)) * (width - padding * 2);
        const y = height - padding - ((p.savings_end - minVal) / (maxVal - minVal)) * (height - padding * 2);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');

    let svgHtml = `
        <svg viewBox="0 0 ${width} ${height}" style="width: 100%; height: 220px; background: rgba(0,0,0,0.3); border-radius: 12px;">
            <defs>
                <linearGradient id="curveGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#A855F7" stop-opacity="0.5"/>
                    <stop offset="100%" stop-color="#A855F7" stop-opacity="0.0"/>
                </linearGradient>
            </defs>
            <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#334155" stroke-width="1"/>
            <polyline fill="none" stroke="#D946EF" stroke-width="3" stroke-linecap="round" points="${points}"/>
            ${trajectory.map((p, idx) => {
                const x = padding + (idx / (trajectory.length - 1)) * (width - padding * 2);
                const y = height - padding - ((p.savings_end - minVal) / (maxVal - minVal)) * (height - padding * 2);
                return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="#FFFFFF"/>`;
            }).join('')}
            <text x="${padding}" y="${height - 10}" fill="#94A3B8" font-size="11">Month 1</text>
            <text x="${width - padding - 30}" y="${height - 10}" fill="#94A3B8" font-size="11">Month ${trajectory.length}</text>
        </svg>
    `;
    wrapper.innerHTML = svgHtml;
}

// ── 4. Opportunity Pathways Loader ──
let cachedOpportunities = [];

async function loadOpportunities() {
    try {
        const res = await fetch('/api/data/opportunities');
        const data = await res.json();
        if (data.status === 'success') {
            cachedOpportunities = data.data;
            renderOpportunitiesList(cachedOpportunities);
        }
    } catch (err) {
        console.error('Failed to load opportunities:', err);
    }
}

function filterOpps(evt, track) {
    document.querySelectorAll('.opp-filter-bar .tab-btn').forEach(b => b.classList.remove('active'));
    evt.currentTarget.classList.add('active');
    if (track === 'all') {
        renderOpportunitiesList(cachedOpportunities);
    } else {
        const filtered = cachedOpportunities.filter(o => o.track === track);
        renderOpportunitiesList(filtered);
    }
}

function renderOpportunitiesList(list) {
    const container = document.getElementById('opp_grid_container');
    if (!container) return;

    if (!list || !list.length) {
        container.innerHTML = '<p style="color: #94A3B8;">No pathways found.</p>';
        return;
    }

    container.innerHTML = list.map(o => `
        <div class="opp-item-card">
            <div>
                <div class="opp-title">${o.title}</div>
                <div class="opp-meta">${o.sector} &bull; Required Capital: ₹${Number(o.capital_required_inr || 0).toLocaleString('en-IN')}</div>
                <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 10px;">${o.description || ''}</p>
            </div>
            <div class="opp-badge-row">
                <span class="opp-badge ${o.track === 'Wage Employment' ? 'badge-wage' : 'badge-ent'}">${o.track}</span>
                <span class="opp-badge badge-emerald">₹${Number(o.estimated_monthly_income_min_inr || 0).toLocaleString('en-IN')} - ₹${Number(o.estimated_monthly_income_max_inr || 0).toLocaleString('en-IN')}/mo</span>
                <span class="opp-badge badge-indigo">${o.scheme_linkage || 'PMKVY 4.0'}</span>
            </div>
        </div>
    `).join('');
}

// ── 5. India Intelligence Data Loader ──
async function loadIndiaIntelligence() {
    // 1. UPI Apps
    try {
        const res = await fetch('/api/data/upi_apps');
        const data = await res.json();
        if (data.status === 'success') {
            const table = document.getElementById('upi_table_container');
            table.innerHTML = `
                <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse; color: #E2E8F0;">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #94A3B8; text-align: left;">
                            <th style="padding: 8px;">App / Provider</th>
                            <th style="padding: 8px;">Volume (Cr Txns)</th>
                            <th style="padding: 8px;">Value (₹ Lakh Cr)</th>
                            <th style="padding: 8px;">Market Share (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.data.map(r => `
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                                <td style="padding: 8px; font-weight: 600;">${r.app_name}</td>
                                <td style="padding: 8px;">${r.volume_crore_feb2025}</td>
                                <td style="padding: 8px;">₹${r.value_inr_lakh_crore_feb2025}</td>
                                <td style="padding: 8px; color: #A855F7; font-weight: 700;">${r.market_share_volume_pct}%</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }
    } catch (err) {
        console.error('Error loading UPI apps data:', err);
    }

    // 2. State Cyber Frauds
    try {
        const res = await fetch('/api/data/state_cyber_frauds');
        const data = await res.json();
        if (data.status === 'success') {
            const table = document.getElementById('state_frauds_container');
            const states = data.data.filter(s => s.state_ut !== 'All India').slice(0, 10);
            table.innerHTML = `
                <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse; color: #E2E8F0;">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #94A3B8; text-align: left;">
                            <th style="padding: 8px;">State / UT</th>
                            <th style="padding: 8px;">Complaints (2024)</th>
                            <th style="padding: 8px;">Defrauded (₹ Cr)</th>
                            <th style="padding: 8px;">Recovery Rate</th>
                            <th style="padding: 8px;">Primary Threat Vector</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${states.map(s => `
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                                <td style="padding: 8px; font-weight: 600;">${s.state_ut}</td>
                                <td style="padding: 8px;">${Number(s.complaints_registered_2024).toLocaleString('en-IN')}</td>
                                <td style="padding: 8px; color: #FB7185;">₹${s.amount_defrauded_inr_crore}</td>
                                <td style="padding: 8px; color: #34D399;">${s.recovery_rate_pct}%</td>
                                <td style="padding: 8px; color: #94A3B8;">${s.primary_fraud_vector}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }
    } catch (err) {
        console.error('Error loading state frauds data:', err);
    }

    // 3. Source Register
    try {
        const res = await fetch('/api/source-register');
        const data = await res.json();
        if (data.status === 'success') {
            const container = document.getElementById('sources_table_container');
            container.innerHTML = `
                <div style="font-size: 0.85rem; line-height: 1.6;">
                    ${data.sources.map(s => `
                        <div style="padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <strong>${s.dataset_name}</strong> &bull; <span style="color: #94A3B8;">${s.publisher}</span> (${s.reference_period}) &bull;
                            <a href="${s.official_source_url}" target="_blank" style="color: #A855F7;">[Official Link ↗]</a>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } catch (err) {
        console.error('Error loading source register:', err);
    }
}

// ── Initial Boot ──
document.addEventListener('DOMContentLoaded', () => {
    calculateTwin();
    runSimulation();
    loadOpportunities();
    loadIndiaIntelligence();
});
