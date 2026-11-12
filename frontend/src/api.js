const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

export const api = {
  health: () => request('/health'),
  listNodes: () => request('/api/nodes'),
  createUser: (payload) =>
    request('/api/users', { method: 'POST', body: JSON.stringify(payload) }),
  createTravelPass: (payload) =>
    request('/api/trips', { method: 'POST', body: JSON.stringify(payload) }),
  triggerSos: (payload) =>
    request('/api/sos', { method: 'POST', body: JSON.stringify(payload) }),
  getIncident: (incidentId) => request(`/api/incidents/${incidentId}`),
  updateIncidentStatus: (incidentId, payload) =>
    request(`/api/incidents/${incidentId}/status`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
};
