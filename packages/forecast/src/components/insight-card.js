export class InsightCard {
  constructor(data) {
    this.data = data;
  }

  render() {
    const { vegetationHealth, floodRisk, recommendation } = this.data;

    return `
      <div class="card">
        <div class="status-badge status-${vegetationHealth.status}">
          <span class="material-symbols-outlined" style="font-size: 16px; margin-right: 4px;">eco</span>
          Vegetation Health
        </div>
        <div class="card-value">${vegetationHealth.score}/100</div>
        <!-- Trend Bar -->
        <div class="trend-bar-container">
            <div class="trend-bar-fill trend-fill-${vegetationHealth.status}" style="width: ${vegetationHealth.score}%"></div>
        </div>
        <div class="card-desc">${vegetationHealth.description}</div>
      </div>

      <div class="card">
        <div class="status-badge status-${floodRisk.status}">
          <span class="material-symbols-outlined" style="font-size: 16px; margin-right: 4px;">water_drop</span>
          Flood Risk
        </div>
        <div class="card-value">${floodRisk.level}%</div>
        <!-- Trend Bar -->
        <div class="trend-bar-container">
            <div class="trend-bar-fill trend-fill-${floodRisk.status}" style="width: ${floodRisk.level}%"></div>
        </div>
        <div class="card-desc">${floodRisk.description}</div>
      </div>

      <div class="card" style="border-left: 4px solid var(--primary-color);">
        <div class="card-title">Recommended Action(s)</div>
        <div class="card-desc" style="font-weight: 500;">
            <ul style="padding-left: 20px; margin: 8px 0;">
                ${Array.isArray(recommendation) ? recommendation.map(rec => `
                    <li style="margin-bottom: 4px; color: #202124;">
                        ${rec.title} 
                        ${rec.type === 'action' ? '<span style="color:#d93025; font-size:11px; border:1px solid #d93025; border-radius:4px; padding:0 4px; margin-left:4px;">ACTION</span>' : ''}
                    </li>
                `).join('') : recommendation}
            </ul>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 12px;">
            <button class="action-btn" id="btn-pdf">
                <span class="material-symbols-outlined" style="font-size: 18px; margin-right: 6px; vertical-align: middle;">picture_as_pdf</span>
                Download Brief
            </button>
            <button class="action-btn" id="btn-whatsapp" style="background:#25D366; flex:1;">
                <span class="material-symbols-outlined" style="font-size: 18px; margin-right: 6px; vertical-align: middle;">chat</span>
                Alert
            </button>
        </div>
      </div>
    `;
  }
}
