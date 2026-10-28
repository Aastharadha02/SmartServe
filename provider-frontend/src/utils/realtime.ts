/**
 * SmartServe Real-Time WebSocket Bridge
 * Connects Kafka event consumer updates to frontend React components without polling.
 *
 * Architecture:
 *   - Per-subscription event_id deduplication (prevents duplicate React state updates
 *     while allowing multiple independent component subscriptions on the same page).
 *   - Race-safe connection lifecycle (gracefully handles React StrictMode / unmount).
 *   - Exponential backoff reconnection with jitter.
 *   - Periodic heartbeat ping keeps the stream active.
 */

type MessageHandler = (data: any) => void;

export function getWebSocketUrl(channels: string[] = []): string {
  const rawApiUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
  const isHttps = rawApiUrl.startsWith('https:') || (typeof window !== 'undefined' && window.location.protocol === 'https:');
  const wsProtocol = isHttps ? 'wss:' : 'ws:';
  const hostDomain = rawApiUrl.replace(/^https?:\/\//, '').replace(/\/api\/v1\/?$/, '');
  const token = typeof window !== 'undefined' ? localStorage.getItem('smartserve_provider_token') : null;
  const params = new URLSearchParams();
  if (channels.length > 0) {
    params.set('channels', channels.join(','));
  }
  if (token) {
    params.set('token', token);
  }
  const queryString = params.toString() ? `?${params.toString()}` : '';
  return `${wsProtocol}//${hostDomain}/ws/stream${queryString}`;
}

export function subscribeToRealtime(
  channels: string[],
  onMessage: MessageHandler
): () => void {
  let ws: WebSocket | null = null;
  let disposed = false;
  let pingInterval: ReturnType<typeof setInterval> | null = null;
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  let retryCount = 0;
  let generation = 0;

  // Per-subscription event_id deduplication
  const seenEventIds = new Set<string>();
  const seenEventOrder: string[] = [];
  const maxSeen = 1000;

  function isDuplicateEvent(eventId: string): boolean {
    if (!eventId) return false;
    if (seenEventIds.has(eventId)) return true;
    seenEventIds.add(eventId);
    seenEventOrder.push(eventId);
    if (seenEventOrder.length > maxSeen) {
      const oldest = seenEventOrder.shift();
      if (oldest) seenEventIds.delete(oldest);
    }
    return false;
  }

  function clearTimers() {
    if (pingInterval !== null) { clearInterval(pingInterval); pingInterval = null; }
    if (reconnectTimer !== null) { clearTimeout(reconnectTimer); reconnectTimer = null; }
  }

  function scheduleReconnect() {
    if (disposed) return;
    const base = Math.min(1000 * Math.pow(1.5, retryCount), 8000);
    const jitter = Math.random() * 500;
    retryCount++;
    reconnectTimer = setTimeout(connect, base + jitter);
  }

  function connect() {
    if (disposed) return;
    clearTimers();

    // Close any lingering socket from a prior attempt
    if (ws) {
      const s = ws;
      ws = null;
      if (s.readyState === WebSocket.CONNECTING) {
        s.onopen = () => { try { s.close(); } catch (_) {} };
      } else {
        try { s.onopen = null; s.onmessage = null; s.onclose = null; s.onerror = null; s.close(); } catch (_) {}
      }
    }

    const gen = ++generation;
    try {
      const url = getWebSocketUrl(channels);
      const socket = new WebSocket(url);
      ws = socket;

        socket.onopen = () => {
          if (gen !== generation || disposed) { socket.close(); return; }
          retryCount = 0;
          const token = typeof window !== 'undefined' ? localStorage.getItem('smartserve_provider_token') : null;
          if (token && socket.readyState === WebSocket.OPEN) {
            try { socket.send(JSON.stringify({ action: 'auth', token })); } catch (_) {}
          }
          pingInterval = setInterval(() => {
            if (socket.readyState === WebSocket.OPEN) {
              try { socket.send(JSON.stringify({ action: 'ping' })); } catch (_) {}
            }
          }, 25000);
        };

      socket.onmessage = (event) => {
        if (gen !== generation || disposed) return;
        try {
          const data = JSON.parse(event.data);
          // Skip control frames
          if (data.type === 'pong' || data.type === 'CONNECTION_ESTABLISHED' || data.type === 'SUBSCRIBED' || data.type === 'UNSUBSCRIBED') return;

          // Event deduplication per subscription using event_id
          const eventId = data.event_id;
          if (eventId && isDuplicateEvent(eventId)) return;

          onMessage(data);
        } catch (_) {
          // ignore malformed payloads
        }
      };

      socket.onclose = () => {
        if (gen !== generation) return;
        clearTimers();
        if (!disposed) scheduleReconnect();
      };

      socket.onerror = () => {
        // let onclose handle cleanup
      };
    } catch (_) {
      if (!disposed) scheduleReconnect();
    }
  }

  connect();

  return () => {
    disposed = true;
    generation++;
    clearTimers();
    if (ws) {
      const s = ws;
      ws = null;
      if (s.readyState === WebSocket.CONNECTING) {
        s.onopen = () => {
          try { s.close(); } catch (_) {}
        };
      } else {
        try { s.onopen = null; s.onmessage = null; s.onclose = null; s.onerror = null; s.close(); } catch (_) {}
      }
    }
  };
}
