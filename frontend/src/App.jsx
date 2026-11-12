import { useEffect, useState } from 'react';
import { api } from './api.js';

const DEMO_USER = {
  name: 'Demo Traveller',
  phone: '+919800000001',
  emergency_contacts: [
    {
      name: 'Family Contact',
      phone: '+919800000002',
      relationship: 'family',
    },
  ],
};

export default function App() {
  const [nodes, setNodes] = useState([]);
  const [user, setUser] = useState(null);
  const [incident, setIncident] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api
      .listNodes()
      .then((data) => setNodes(data.nodes || []))
      .catch(() => setMessage('Unable to load network nodes.'));
  }, []);

  async function registerUser() {
    setLoading(true);
    try {
      const created = await api.createUser(DEMO_USER);
      setUser(created);
      setMessage(`Demo user registered: ${created.id}`);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function triggerSos() {
    if (!user) {
      setMessage('Register the demo user first.');
      return;
    }

    setLoading(true);
    try {
      const result = await api.triggerSos({
        user_id: user.id,
        incident_type: 'medical',
        latitude: 30.1,
        longitude: 78.3,
        description: 'Demo trekking injury requiring first aid',
      });
      setIncident(result);
      setMessage(`SOS created. Nearest node: ${result.assigned_node || 'None available'}.`);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function acknowledgeIncident() {
    if (!incident) return;

    setLoading(true);
    try {
      const updated = await api.updateIncidentStatus(incident.incident_id, {
        status: 'acknowledged',
        note: 'Coordinator acknowledged the incident in the demo console.',
      });
      setIncident((previous) => ({
        ...previous,
        status: updated.status,
      }));
      setMessage('Incident acknowledged.');
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header>
        <h1>Spider Safety Network</h1>
        <p>
          Remote-area emergency coverage: SOS escalation, first-aid coordination, and
          drone-node readiness.
        </p>
      </header>

      <section className="card">
        <h2>Emergency response</h2>
        <p>
          This is a demonstration interface. In a real emergency, call <strong>112</strong>{' '}
          immediately.
        </p>
        <div className="actions">
          <button onClick={registerUser} disabled={loading}>
            Register demo user
          </button>
          <button className="danger" onClick={triggerSos} disabled={loading}>
            Trigger demo SOS
          </button>
          <button onClick={acknowledgeIncident} disabled={loading || !incident}>
            Acknowledge incident
          </button>
        </div>
        {message && <p className="message">{message}</p>}
      </section>

      {incident && (
        <section className="card">
          <h2>Incident</h2>
          <p>
            <strong>ID:</strong> {incident.incident_id}
          </p>
          <p>
            <strong>Status:</strong> {incident.status}
          </p>
          <p>
            <strong>Assigned node:</strong> {incident.assigned_node || 'No node available'}
          </p>
          <p>
            <strong>Estimated response:</strong> {incident.estimated_response_minutes} minutes
          </p>
          <p>
            <strong>Trusted contacts notified:</strong>{' '}
            {incident.trusted_contacts_notified}
          </p>
        </section>
      )}

      <section className="card">
        <h2>Spider network nodes</h2>
        {nodes.length === 0 ? (
          <p>Loading nodes...</p>
        ) : (
          <ul>
            {nodes.map((node) => (
              <li key={node.id}>
                <strong>{node.name}</strong> — {node.node_type} — {node.status}
              </li>
            ))}
          </ul>
        )}
      </section>

      <footer>
        Prototype only. It does not replace 112, police, ambulance, or medical services.
      </footer>
    </main>
  );
}
