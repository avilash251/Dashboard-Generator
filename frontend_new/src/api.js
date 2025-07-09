export async function getMetrics(prompt) {
  const res = await fetch('http://localhost:8080/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });
  if (!res.ok) throw new Error('Failed to fetch');
  const data = await res.json();
  return {
    widgets: data.layout || [],
  };
}
