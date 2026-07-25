
async function loadDashboard(force){
  const box = $('dashboardContent');
  const centerBox = $('dashboardCenterInfo');
  const target = (box && getComputedStyle(box).display !== 'none') ? box : centerBox;
  
  if(!target) return;
  if(!force && target.dataset.loaded) return;
  
  try {
    const data = await api('/api/status');
    target.dataset.loaded = '1';
    
    const gateway = data.details || {};
    const isAlive = data.alive;
    const statusClass = isAlive ? 'online' : (isAlive === false ? 'offline' : 'unknown');
    const statusText = isAlive ? 'Connected' : (isAlive === false ? 'Disconnected' : 'Not Configured');
    
    let html = '<div class="dashboard-grid">';
    
    // Gateway Card
    html += `<div class="dashboard-card">
      <div class="dashboard-card-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 11 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg></div>
      <div class="dashboard-card-label">${esc(t('dashboard_gateway'))}</div>
      <div class="dashboard-card-value">${statusText}</div>
      <div class="dashboard-card-status"><span class="status-dot ${statusClass}"></span> ${gateway.gateway_state || 'Unknown'}</div>
    </div>`;
    
    // Active Runs Card
    html += `<div class="dashboard-card">
      <div class="dashboard-card-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></div>
      <div class="dashboard-card-label">${esc(t('dashboard_active_agents'))}</div>
      <div class="dashboard-card-value">${gateway.active_agents || 0}</div>
      <div class="dashboard-card-status">Across ${gateway.platform_count || 0} platforms</div>
    </div>`;
    
    // Version Card
    html += `<div class="dashboard-card">
      <div class="dashboard-card-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg></div>
      <div class="dashboard-card-label">${esc(t('dashboard_hermes_version'))}</div>
      <div class="dashboard-card-value">v0.14.0</div>
      <div class="dashboard-card-status">Checked at ${new Date(data.checked_at).toLocaleTimeString()}</div>
    </div>`;
    
    html += '</div>'; // End grid
    
    if (target === box) {
      html += `<div class="dashboard-section-title">${esc(t('dashboard_quick_actions'))}</div>`;
      html += '<div class="dashboard-actions">';
      html += `<button class="dashboard-action-btn" onclick="switchPanel('settings')">${esc(t('dashboard_system_settings'))}</button>`;
      html += `<button class="dashboard-action-btn" onclick="loadLogs(true);switchPanel('logs')">${esc(t('dashboard_view_logs'))}</button>`;
      html += `<button class="dashboard-action-btn" onclick="loadInsights(true);switchPanel('insights')">${esc(t('dashboard_usage_insights'))}</button>`;
      html += '</div>';
    }
    
    target.innerHTML = html;
  } catch(e) {
    target.innerHTML = `<div style="padding:12px;color:var(--error)">Failed to load status: ${e.message}</div>`;
  }
}
